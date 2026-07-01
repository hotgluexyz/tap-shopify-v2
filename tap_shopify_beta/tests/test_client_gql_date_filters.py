"""Tests for Shopify GraphQL updated_at search filter bounds."""

import datetime
import importlib
import sys
import types

import pendulum
import pytest


def _empty_jsonpath(*args, **kwargs):
    return iter(())


@pytest.fixture
def client_gql(monkeypatch):
    client_stub = types.ModuleType("tap_shopify_beta.client")
    client_stub.shopifyStream = object

    jsonpath_stub = types.ModuleType("hotglue_singer_sdk.helpers.jsonpath")
    jsonpath_stub.extract_jsonpath = _empty_jsonpath

    exceptions_stub = types.ModuleType("hotglue_singer_sdk.exceptions")
    exceptions_stub.RetriableAPIError = Exception

    monkeypatch.setitem(sys.modules, "tap_shopify_beta.client", client_stub)
    monkeypatch.setitem(sys.modules, "hotglue_singer_sdk", types.ModuleType("hotglue_singer_sdk"))
    monkeypatch.setitem(
        sys.modules,
        "hotglue_singer_sdk.helpers",
        types.ModuleType("hotglue_singer_sdk.helpers"),
    )
    monkeypatch.setitem(sys.modules, "hotglue_singer_sdk.helpers.jsonpath", jsonpath_stub)
    monkeypatch.setitem(sys.modules, "hotglue_singer_sdk.exceptions", exceptions_stub)
    sys.modules.pop("tap_shopify_beta.client_gql", None)
    module = importlib.import_module("tap_shopify_beta.client_gql")
    yield module
    sys.modules.pop("tap_shopify_beta.client_gql", None)


def test_to_shopify_utc_formats_naive_datetime_with_z(client_gql):
    value = datetime.datetime(2026, 7, 1, 2, 58, 8)

    assert client_gql.to_shopify_utc(value) == "2026-07-01T02:58:08Z"


def test_to_shopify_utc_formats_aware_utc_datetime_with_z(client_gql):
    value = datetime.datetime(2026, 7, 1, 2, 58, 8, tzinfo=datetime.timezone.utc)

    assert client_gql.to_shopify_utc(value) == "2026-07-01T02:58:08Z"


def test_to_shopify_utc_converts_offset_datetime_to_utc_z(client_gql):
    value = datetime.datetime(
        2026,
        7,
        1,
        12,
        58,
        8,
        tzinfo=datetime.timezone(datetime.timedelta(hours=10)),
    )

    assert client_gql.to_shopify_utc(value) == "2026-07-01T02:58:08Z"


def test_to_shopify_utc_converts_pendulum_datetime_to_utc_z(client_gql):
    value = pendulum.datetime(2026, 7, 1, 12, 58, 8, tz="Australia/Brisbane")

    assert client_gql.to_shopify_utc(value) == "2026-07-01T02:58:08Z"


def test_get_url_params_date_range_filter_uses_utc_z_bounds(client_gql):
    stream = client_gql.shopifyGqlStream.__new__(client_gql.shopifyGqlStream)
    stream.name = "orders"
    stream.replication_key = "updatedAt"
    stream.config = {}
    context = {
        "date_range": {
            "start_date": datetime.datetime(
                2026, 7, 1, 12, 45, 54, tzinfo=datetime.timezone.utc
            ),
            "end_date": datetime.datetime(
                2026, 7, 1, 15, 33, 17, tzinfo=datetime.timezone.utc
            ),
        }
    }

    params = stream.get_url_params(context, None)

    assert params["filter"] == (
        "updated_at:>'2026-07-01T12:45:54Z' "
        "AND updated_at:<='2026-07-01T15:33:17Z'"
    )
