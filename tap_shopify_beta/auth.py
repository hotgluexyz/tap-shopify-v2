"""Unbounce Authentication."""

import json
from datetime import datetime
from typing import Optional
import sys

import requests
from singer_sdk.authenticators import APIAuthenticatorBase
from singer_sdk.streams import Stream as RESTStreamBase


class ShopifyAuthenticator(APIAuthenticatorBase):
    """API Authenticator for OAuth 2.0 flows."""

    def __init__(
        self,
        stream: RESTStreamBase,
        config_file: Optional[str] = None,
        auth_endpoint: Optional[str] = None,
    ) -> None:
        super().__init__(stream=stream)
        self._auth_endpoint = auth_endpoint
        self._config_file = config_file
        self._tap = stream._tap

    @property
    def auth_endpoint(self) -> str:
        """Get the authorization endpoint.

        Returns:
            The API authorization endpoint if it is set.

        Raises:
            ValueError: If the endpoint is not set.
        """
        if not self._auth_endpoint:
            raise ValueError("Authorization endpoint not set.")
        return self._auth_endpoint

    @property
    def auth_headers(self) -> dict:
        """Return a dictionary of auth headers to be applied.

        These will be merged with any `http_headers` specified in the stream.

        Returns:
            HTTP headers for authentication.
        """
        if not self.config.get("access_token"):
            self.update_access_token()
        result = super().auth_headers
        result["X-Shopify-Access-Token"] = f"{self._tap._config.get('access_token')}"
        return result

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the hubspot API."""
        if self._tap._config.get("code"):
            return {
                "client_id": self._tap._config["client_id"],
                "client_secret": self._tap._config["client_secret"],
                "code": self._tap._config["code"]
            }
        else:
            return {
                "client_id": self._tap._config["client_id"],
                "client_secret": self._tap._config["client_secret"],
                "grant_type": "client_credentials"
            }


    @property
    def oauth_request_payload(self) -> dict:
        """Get request body.

        Returns:
            A plain (OAuth) or encrypted (JWT) request body.
        """
        return self.oauth_request_body

    # Authentication and refresh
    def update_access_token(self) -> None:
        """Update `access_token` along with: `last_refreshed` and `expires_in`.

        Raises:
            RuntimeError: When OAuth login fails.
        """
        auth_request_payload = self.oauth_request_payload
        token_response = requests.post(self.auth_endpoint, data={}, params=auth_request_payload)
        try:
            token_response.raise_for_status()
            self.logger.info("OAuth authorization attempt was successful.")
        except Exception as ex:
            raise RuntimeError(
                f"Failed OAuth login, response was '{token_response.json()}'. {ex}"
            )
        token_json = token_response.json()
        access_token = token_json["access_token"]
        self._tap._config["access_token"] = access_token

        # Save the access token to the config file if we're using a code-exchange
        if self._tap._config.get("code"):
            config_path = "config.json"
            for i, arg in enumerate(sys.argv):
                if arg == "--config":
                    if i + 1 < len(sys.argv):
                        config_path = sys.argv[i + 1]
                    break
            with open(config_path) as file:
                config = json.load(file)
            config["access_token"] = access_token
            with open(config_path, "w") as file:
                json.dump(config, file, indent=2)
