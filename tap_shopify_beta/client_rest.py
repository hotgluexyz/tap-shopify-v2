from tap_shopify_beta.client import shopifyStream
from singer_sdk.streams.rest import RESTStream
from tap_shopify_beta.auth import ShopifyAuthenticator
from singer_sdk.authenticators import APIKeyAuthenticator
import requests
from typing import Any, Dict, Optional, Callable, Generator
from pendulum import parse
import re
import backoff
from singer_sdk.exceptions import RetriableAPIError
import urllib3
import http.client
import random



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
            result = re.search(r'page_info=([^>;]+)>\; rel="next"', link)
            if result:
                next_page_token = result.group(1)
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
        rep_key_param = f"{self.replication_key}_min"
        if self.replication_key and start_date:
            start_date = start_date.strftime('%Y-%m-%dT%H:%M:%S.%f')
            params[rep_key_param] = start_date
        if self.add_params:
            params.update(self.add_params)
        if next_page_token:
            params = {}
            # if there is page_info other filtering params are not allowed
            params["limit"] = self.limit
            params["page_info"] = next_page_token
        return params

    def request_decorator(self, func: Callable) -> Callable:
        decorator: Callable = backoff.on_exception(
            self.backoff_wait_generator,
            (
                RetriableAPIError,
                urllib3.exceptions.HTTPError,
                http.client.HTTPException,
                requests.exceptions.RequestException,
            ),
            max_tries=self.backoff_max_tries,
            on_backoff=self.backoff_handler,
            jitter=self.half_jitter,
        )(func)
        return decorator

    def half_jitter(self, wait_time: float) -> float:
        return wait_time / 2 + random.uniform(0, wait_time / 2)

    def backoff_wait_generator(self) -> Callable[..., Generator[int, Any, None]]:
        """
        Example:
            - 1st retry: 10 seconds
            - 2nd retry: 20 seconds
            - 3rd retry: 40 seconds
            - 4th retry: 80 seconds
            - 5th retry: 160 seconds
            - 6th retry: 320 seconds (capped at 5 minutes)
        """
        return backoff.expo(base=2, factor=10, max_value=300)

    def backoff_max_tries(self) -> int:
        return 8
    