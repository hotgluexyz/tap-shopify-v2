"""Tests for Shopify GraphQL updated_at search filter bounds."""

import datetime
import importlib
import json
import sys
import types

import pendulum
import pytest

from tap_shopify_beta.shopify_dates import to_shopify_utc


def _empty_jsonpath(*args, **kwargs):
    return iter(())


@pytest.fixture
def hotglue_sdk_stubs(monkeypatch):
    client_stub = types.ModuleType("tap_shopify_beta.client")
    client_stub.shopifyStream = object

    jsonpath_stub = types.ModuleType("hotglue_singer_sdk.helpers.jsonpath")
    jsonpath_stub.extract_jsonpath = _empty_jsonpath

    exceptions_stub = types.ModuleType("hotglue_singer_sdk.exceptions")
    exceptions_stub.RetriableAPIError = Exception

    streams_stub = types.ModuleType("hotglue_singer_sdk.streams")
    streams_rest_stub = types.ModuleType("hotglue_singer_sdk.streams.rest")
    streams_rest_stub.RESTStream = object

    authenticators_stub = types.ModuleType("hotglue_singer_sdk.authenticators")

    class APIKeyAuthenticator:
        @classmethod
        def create_for_stream(cls, *args, **kwargs):
            return cls()

    authenticators_stub.APIKeyAuthenticator = APIKeyAuthenticator

    auth_stub = types.ModuleType("tap_shopify_beta.auth")
    auth_stub.ShopifyAuthenticator = object
    simplejson_stub = types.ModuleType("simplejson")
    simplejson_stub.JSONDecodeError = json.JSONDecodeError
    simplejson_stub.loads = json.loads

    monkeypatch.setitem(sys.modules, "tap_shopify_beta.client", client_stub)
    monkeypatch.setitem(sys.modules, "hotglue_singer_sdk", types.ModuleType("hotglue_singer_sdk"))
    monkeypatch.setitem(
        sys.modules,
        "hotglue_singer_sdk.helpers",
        types.ModuleType("hotglue_singer_sdk.helpers"),
    )
    monkeypatch.setitem(sys.modules, "hotglue_singer_sdk.helpers.jsonpath", jsonpath_stub)
    monkeypatch.setitem(sys.modules, "hotglue_singer_sdk.exceptions", exceptions_stub)
    monkeypatch.setitem(sys.modules, "hotglue_singer_sdk.streams", streams_stub)
    monkeypatch.setitem(sys.modules, "hotglue_singer_sdk.streams.rest", streams_rest_stub)
    monkeypatch.setitem(sys.modules, "hotglue_singer_sdk.authenticators", authenticators_stub)
    monkeypatch.setitem(sys.modules, "tap_shopify_beta.auth", auth_stub)
    monkeypatch.setitem(sys.modules, "simplejson", simplejson_stub)
    yield
    for module_name in (
        "tap_shopify_beta.client_bulk",
        "tap_shopify_beta.client_gql",
        "tap_shopify_beta.client_rest",
    ):
        sys.modules.pop(module_name, None)


@pytest.fixture
def client_gql(hotglue_sdk_stubs):
    sys.modules.pop("tap_shopify_beta.client_gql", None)
    module = importlib.import_module("tap_shopify_beta.client_gql")
    yield module
    sys.modules.pop("tap_shopify_beta.client_gql", None)


@pytest.fixture
def client_bulk(hotglue_sdk_stubs):
    sys.modules.pop("tap_shopify_beta.client_bulk", None)
    module = importlib.import_module("tap_shopify_beta.client_bulk")
    yield module
    sys.modules.pop("tap_shopify_beta.client_bulk", None)


@pytest.fixture
def client_rest(hotglue_sdk_stubs):
    sys.modules.pop("tap_shopify_beta.client_rest", None)
    module = importlib.import_module("tap_shopify_beta.client_rest")
    yield module
    sys.modules.pop("tap_shopify_beta.client_rest", None)


def test_to_shopify_utc_formats_naive_datetime_with_z():
    value = datetime.datetime(2026, 7, 1, 2, 58, 8)

    assert to_shopify_utc(value) == "2026-07-01T02:58:08Z"


def test_to_shopify_utc_formats_aware_utc_datetime_with_z():
    value = datetime.datetime(2026, 7, 1, 2, 58, 8, tzinfo=datetime.timezone.utc)

    assert to_shopify_utc(value) == "2026-07-01T02:58:08Z"


def test_to_shopify_utc_converts_offset_datetime_to_utc_z():
    value = datetime.datetime(
        2026,
        7,
        1,
        12,
        58,
        8,
        tzinfo=datetime.timezone(datetime.timedelta(hours=10)),
    )

    assert to_shopify_utc(value) == "2026-07-01T02:58:08Z"


def test_to_shopify_utc_converts_pendulum_datetime_to_utc_z():
    value = pendulum.datetime(2026, 7, 1, 12, 58, 8, tz="Australia/Brisbane")

    assert to_shopify_utc(value) == "2026-07-01T02:58:08Z"


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


def test_get_url_params_monthly_filter_uses_utc_z_bounds(client_gql):
    stream = client_gql.shopifyGqlStream.__new__(client_gql.shopifyGqlStream)
    stream.name = "orders"
    stream.replication_key = "updatedAt"
    stream.config = {"sync_orders_monthly": True}
    stream.start_date = None
    stream.get_starting_timestamp = lambda context: pendulum.datetime(
        2026, 7, 1, 12, 45, 54, tz="Australia/Brisbane"
    )

    params = stream.get_url_params({}, None)

    assert params["filter"] == (
        "updated_at:>'2026-07-01T02:45:54Z' "
        "AND updated_at:<='2026-08-01T02:45:54Z'"
    )


def test_get_url_params_plain_incremental_filter_uses_utc_z_bounds(client_gql):
    stream = client_gql.shopifyGqlStream.__new__(client_gql.shopifyGqlStream)
    stream.name = "orders"
    stream.replication_key = "updatedAt"
    stream.config = {"end_date": "2026-07-01T15:33:17+10:00"}
    stream.start_date = pendulum.datetime(2026, 7, 1, 12, 45, 54, tz="Australia/Brisbane")

    params = stream.get_url_params({}, None)

    assert params["filter"] == (
        "updated_at:>'2026-07-01T02:45:54Z' "
        "AND updated_at:<='2026-07-01T05:33:17Z'"
    )


def test_bulk_filter_uses_utc_z_bounds(client_bulk):
    stream = client_bulk.shopifyBulkStream.__new__(client_bulk.shopifyBulkStream)
    stream.replication_key = "updatedAt"
    stream.start_date = None
    stream.config = {}
    stream.get_starting_timestamp = lambda context: pendulum.datetime(
        2026, 7, 1, 12, 58, 8, tz="Australia/Brisbane"
    )

    assert stream.filters == (
        "(query: \"updated_at:>'2026-07-01T02:58:08Z' "
        "AND updated_at:<='2026-07-02T02:58:08Z'\")"
    )


def test_rest_params_use_utc_z_bounds(client_rest):
    stream = client_rest.shopifyRestStream.__new__(client_rest.shopifyRestStream)
    stream.replication_key = "updated_at"
    stream.config = {"end_date": "2026-07-01T15:33:17+10:00"}
    stream.add_params = None
    stream.get_starting_time = lambda context: pendulum.datetime(
        2026, 7, 1, 12, 45, 54, tz="Australia/Brisbane"
    )

    params = stream.get_url_params({}, None)

    assert params["updated_at_min"] == "2026-07-01T02:45:54Z"
    assert params["updated_at_max"] == "2026-07-01T05:33:17Z"
