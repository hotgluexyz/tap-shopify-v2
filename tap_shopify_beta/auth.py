"""Shopify OAuth authentication."""

from __future__ import annotations

import re
from typing import Any

import requests
from singer import utils
from hotglue_singer_sdk.authenticators import OAuthAuthenticator, _token_lock
from hotglue_singer_sdk.exceptions import RetriableAPIError
from hotglue_etl_exceptions import InvalidCredentialsError

_LEGACY_REFRESH_SKIP_LOGGED = False
# SDK persists expires_in as Unix epoch seconds (~1e9). TTL from Shopify is much smaller.
_EPOCH_EXPIRY_THRESHOLD = 10**9


def get_shop_name_from_config(config: dict) -> str:
    """Return the myshopify shop slug from tap config."""
    shop_no_https = config["shop"].replace("https://", "")
    shop_no_extra_slashes = re.sub(r"/.*", "", shop_no_https)
    if shop_no_extra_slashes.endswith(".myshopify.com"):
        return shop_no_extra_slashes[: -len(".myshopify.com")]
    return shop_no_extra_slashes


def shopify_oauth_token_url(config: dict) -> str:
    """Build the Shopify admin OAuth access token URL for the configured shop."""
    shop = get_shop_name_from_config(config)
    return f"https://{shop}.myshopify.com/admin/oauth/access_token"


def has_refresh_token(config: dict) -> bool:
    """Return True when config has a non-empty refresh_token."""
    refresh_token = config.get("refresh_token")
    if refresh_token is None:
        return False
    if isinstance(refresh_token, str):
        return bool(refresh_token.strip())
    return bool(refresh_token)


class ShopifyOAuthAuthenticator(OAuthAuthenticator):
    """OAuth authenticator for Shopify Admin API (expiring offline tokens)."""

    def _tap_config(self) -> dict[str, Any]:
        """Live tap config (authoritative for tokens); fall back to stream snapshot."""
        tap_cfg = getattr(self._tap, "_config", None)
        if isinstance(tap_cfg, dict):
            return tap_cfg
        return dict(self._config)

    def _mark_legacy_token_valid(self, access_token: str) -> None:
        """Use a permanent offline token without calling Shopify or the HG accesstoken API."""
        global _LEGACY_REFRESH_SKIP_LOGGED
        self.access_token = access_token
        if not _LEGACY_REFRESH_SKIP_LOGGED:
            self.logger.info(
                "Skipping OAuth token refresh: no refresh_token (legacy non-expiring token)."
            )
            _LEGACY_REFRESH_SKIP_LOGGED = True

    def _legacy_permanent_token(self) -> str | None:
        """Access token that should be used as-is when no refresh_token is configured."""
        cfg = self._tap_config()
        access_token = cfg.get("access_token")
        if not access_token:
            return None
        if has_refresh_token(cfg):
            return None
        return str(access_token)

    @property
    def auth_headers(self) -> dict:
        """Return Shopify Admin API auth headers."""
        legacy_token = self._legacy_permanent_token()
        if legacy_token is not None:
            self._mark_legacy_token_valid(legacy_token)
        elif not self.is_token_valid():
            with _token_lock:
                if not self.is_token_valid():
                    self.update_access_token()
        result = super().auth_headers
        result.pop("Authorization", None)
        token = self._tap_config().get("access_token") or self.access_token
        result["X-Shopify-Access-Token"] = f"{token}"
        return result

    def update_access_token(self) -> None:
        """Refresh expiring tokens; never call Shopify refresh for legacy permanent tokens."""
        legacy_token = self._legacy_permanent_token()
        if legacy_token is not None:
            self._mark_legacy_token_valid(legacy_token)
            return
        super().update_access_token()

    @property
    def oauth_request_body(self) -> dict:
        """Build the Shopify token exchange or refresh request body."""
        config = self._tap_config()
        refresh_token = config.get("refresh_token")
        if has_refresh_token(config):
            return {
                "client_id": config["client_id"],
                "client_secret": config["client_secret"],
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }
        raise InvalidCredentialsError(
            "OAuth token refresh requires refresh_token."
        )

    def is_token_valid(self) -> bool:
        """Return whether the configured access token should be used without refresh."""
        legacy_token = self._legacy_permanent_token()
        if legacy_token is not None:
            self._mark_legacy_token_valid(legacy_token)
            return True

        cfg = self._tap_config()
        access_token = cfg.get("access_token")
        if not access_token:
            return False

        if self.expires_in is None and cfg.get("expires_in") is not None:
            self.expires_in = cfg.get("expires_in")
        if self.access_token is None:
            self.access_token = access_token

        raw_expires = cfg.get("expires_in")
        if raw_expires is not None:
            raw_int = int(raw_expires)
            if raw_int >= _EPOCH_EXPIRY_THRESHOLD:
                if raw_int - int(utils.now().timestamp()) > 120:
                    self.access_token = access_token
                    if self.expires_in is None:
                        self.expires_in = raw_int
                    return True
                return False
            if self.last_refreshed is None:
                return False

        return super().is_token_valid()


def invalidate_shopify_oauth_token(authenticator: ShopifyOAuthAuthenticator) -> None:
    """Clear cached expiry state so the authenticator will refresh on the next attempt."""
    authenticator.last_refreshed = None
    authenticator.expires_in = None
    authenticator.access_token = None


def refresh_oauth_token_on_401(stream: Any) -> bool:
    """Refresh OAuth credentials after a 401; return True if the request may be retried."""
    cfg = getattr(getattr(stream, "_tap", None), "_config", None) or stream.config
    if not cfg.get("client_id") or not has_refresh_token(cfg):
        return False
    if getattr(stream, "_oauth_401_refresh_attempted", False):
        return False
    stream._oauth_401_refresh_attempted = True
    auth = stream.authenticator
    if not isinstance(auth, ShopifyOAuthAuthenticator):
        return False
    invalidate_shopify_oauth_token(auth)
    auth.update_access_token()
    return True


class ShopifyOAuthRequestMixin:
    """HTTP helpers for Shopify OAuth token refresh on 401 responses."""

    _oauth_401_refresh_attempted: bool = False

    def prepare_request(self, context, next_page_token=None):
        """Reset OAuth 401 retry state for each new prepared request."""
        self._oauth_401_refresh_attempted = False
        return super().prepare_request(context, next_page_token)

    def _apply_refreshed_token_to_prepared_request(
        self, prepared_request: requests.PreparedRequest
    ) -> None:
        """Update a prepared request with the access token from tap config after refresh."""
        tap_cfg = getattr(self._tap, "_config", self.config)
        token = tap_cfg.get("access_token") if isinstance(tap_cfg, dict) else self.config.get("access_token")
        if token:
            prepared_request.headers["X-Shopify-Access-Token"] = token

    def _request(self, prepared_request, context=None):
        """Delegate to the SDK; patch auth header on 401 refresh before retry."""
        try:
            return super()._request(prepared_request, context)
        except RetriableAPIError as exc:
            if (
                exc.response is not None
                and exc.response.status_code == 401
                and getattr(self, "_oauth_401_refresh_attempted", False)
            ):
                self._apply_refreshed_token_to_prepared_request(prepared_request)
            raise

    def validate_response(self, response: requests.Response) -> None:
        """Refresh OAuth tokens on 401 once, then apply default response validation."""
        if response.status_code == 401 and refresh_oauth_token_on_401(self):
            raise RetriableAPIError(self.response_error_message(response), response)
        super().validate_response(response)


# Backwards-compatible alias
ShopifyAuthenticator = ShopifyOAuthAuthenticator
