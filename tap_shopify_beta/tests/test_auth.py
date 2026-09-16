"""Tests for Shopify OAuth authentication."""

import logging
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
import requests
from hotglue_etl_exceptions import InvalidCredentialsError

import tap_shopify_beta.auth as auth_module
from tap_shopify_beta.auth import (
    ShopifyOAuthAuthenticator,
    get_shop_name_from_config,
    refresh_oauth_token_on_401,
    shopify_oauth_token_url,
)


@pytest.fixture(autouse=True)
def reset_legacy_log_flag():
    """Isolate legacy refresh log state between tests."""
    auth_module._LEGACY_REFRESH_SKIP_LOGGED = False
    yield
    auth_module._LEGACY_REFRESH_SKIP_LOGGED = False


def _make_authenticator(config, logger=None):
    """Build a ShopifyOAuthAuthenticator with a minimal fake stream."""
    log = logger or logging.getLogger("tap-shopify-beta.tests.auth")
    tap = SimpleNamespace(_config=config, config=config, config_file=None, logger=log)
    stream = SimpleNamespace(
        _tap=tap,
        config=config,
        logger=log,
        tap_name="tap-shopify-beta",
    )
    return ShopifyOAuthAuthenticator(
        stream=stream,
        auth_endpoint=shopify_oauth_token_url(config),
    )


def test_get_shop_name_from_config_strips_domain():
    """Shop slug is parsed from config shop values."""
    assert get_shop_name_from_config({"shop": "acme"}) == "acme"
    assert get_shop_name_from_config({"shop": "acme.myshopify.com"}) == "acme"
    assert get_shop_name_from_config({"shop": "https://acme.myshopify.com/admin"}) == "acme"


def test_oauth_request_body_refresh_grant():
    """Refresh uses grant_type refresh_token."""
    config = {
        "shop": "acme",
        "client_id": "cid",
        "client_secret": "sec",
        "refresh_token": "rt-fake",
    }
    body = _make_authenticator(config).oauth_request_body
    assert body["grant_type"] == "refresh_token"
    assert body["refresh_token"] == "rt-fake"


def test_oauth_request_body_requires_refresh_token():
    """Sync-time refresh only uses refresh_token grant."""
    config = {
        "shop": "acme",
        "client_id": "cid",
        "client_secret": "sec",
    }
    with pytest.raises(InvalidCredentialsError, match="refresh_token"):
        _make_authenticator(config).oauth_request_body


def test_legacy_config_skips_refresh_and_logs(caplog):
    """Permanent-token configs do not trigger refresh when access_token is set."""
    config = {
        "shop": "acme",
        "client_id": "cid",
        "client_secret": "sec",
        "access_token": "shpat-fake-token",
    }
    logger = logging.getLogger("tap-shopify-beta.tests.legacy")
    with caplog.at_level(logging.INFO, logger=logger.name):
        authenticator = _make_authenticator(config, logger=logger)
        assert authenticator.is_token_valid() is True
    assert "Skipping OAuth token refresh" in caplog.text


def test_expiring_config_invalid_until_refreshed():
    """TTL-only expires_in with refresh_token forces refresh on first use."""
    config = {
        "shop": "acme",
        "client_id": "cid",
        "client_secret": "sec",
        "access_token": "shpat-fake-token",
        "refresh_token": "shprt-fake",
        "expires_in": 3600,
    }
    authenticator = _make_authenticator(config)
    assert authenticator.is_token_valid() is False


def test_absolute_expiry_valid_without_in_memory_refresh_state():
    """Persisted epoch expires_in is honored across new authenticator instances."""
    config = {
        "shop": "acme",
        "client_id": "cid",
        "client_secret": "sec",
        "access_token": "shpat-fake-token",
        "refresh_token": "shprt-fake",
        "expires_in": 2_000_000_000,
    }
    authenticator = _make_authenticator(config)
    assert authenticator.is_token_valid() is True


@patch.object(ShopifyOAuthAuthenticator, "update_access_token")
def test_refresh_oauth_token_on_401(mock_update):
    """401 with refresh_token invalidates cached state and refreshes once."""
    config = {
        "shop": "acme",
        "client_id": "cid",
        "client_secret": "sec",
        "access_token": "shpat-fake",
        "refresh_token": "shprt-fake",
    }
    tap = SimpleNamespace(
        _config=config,
        config=config,
        config_file=None,
        logger=MagicMock(),
        confirm_fetch_access_token_support=lambda: False,
    )
    stream = SimpleNamespace(
        _tap=tap,
        config=config,
        logger=MagicMock(),
        _oauth_401_refresh_attempted=False,
        authenticator=_make_authenticator(config),
    )
    response = requests.Response()
    response.status_code = 401
    assert refresh_oauth_token_on_401(stream) is True
    mock_update.assert_called_once()
    assert refresh_oauth_token_on_401(stream) is False


def test_auth_headers_use_shopify_header_not_bearer():
    """Shopify Admin API uses X-Shopify-Access-Token."""
    config = {
        "shop": "acme",
        "client_id": "cid",
        "client_secret": "sec",
        "access_token": "shpat-fake-token",
    }
    authenticator = _make_authenticator(config)
    headers = authenticator.auth_headers
    assert headers["X-Shopify-Access-Token"] == "shpat-fake-token"
    assert "Authorization" not in headers
