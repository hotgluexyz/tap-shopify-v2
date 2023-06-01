from tap_shopify_beta.client import shopifyStream
from singer_sdk.streams.rest import RESTStream
from tap_shopify_beta.auth import ShopifyAuthenticator
from singer_sdk.authenticators import APIKeyAuthenticator
import requests
from typing import Any, Dict, Optional, Union, List, Iterable
from pendulum import parse
import re



class shopifyRestStream(RESTStream):
    """shopify stream class."""

    add_params = None
    limit = 250

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        shop = self.config["shop"]
        return f"https://{shop}.myshopify.com/admin/api/2021-07/"
    
    @property
    def authenticator(self) -> ShopifyAuthenticator:
        """Return a new authenticator object."""
        if self.config.get("client_id") and self.config.get("code"):
            shop = self.config["shop"]
            return ShopifyAuthenticator(
                self, self._tap.config, f"https://{shop}.myshopify.com/admin/oauth/access_token"
            )
        else:
            return APIKeyAuthenticator.create_for_stream(
            self,
            key="X-Shopify-Access-Token",
            value=str(self.config.get("api_key")),
            location="header",
        )
    
    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        if response.headers.get("link"):
            link = response.headers.get("link")
            result = re.search('<(.*); rel="next"', link)
            result1 = result.group(1)
            cursor = re.search('page_info=(.*)>', result1)
            next_page_token = cursor.group(1)
            return next_page_token
        return None
    
    def get_starting_time(self, context):
        start_date = self.config.get("start_date")
        if start_date:
            start_date = parse(self.config.get("start_date"))
        rep_key = self.get_starting_timestamp(context)
        return rep_key or start_date

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        params["limit"] = self.limit
        start_date = self.get_starting_time(context)
        if self.replication_key and start_date:
            start_date = start_date.strftime('%Y-%m-%dT%H:%M:%S.%f')
            params["updated_at_min"] = start_date
        if not self.replication_key and next_page_token:
            params["page_info"] = next_page_token
        if self.add_params:
            params.update(self.add_params)
        return params

    