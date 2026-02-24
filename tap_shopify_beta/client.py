"""GraphQL client handling, including shopifyStream base class."""

import backoff
import requests
import urllib3

from typing import Any, Optional, Callable
from singer_sdk.authenticators import APIKeyAuthenticator
from backports.cached_property import cached_property
from singer_sdk.streams import GraphQLStream
from tap_shopify_beta.auth import ShopifyAuthenticator
from singer_sdk.exceptions import RetriableAPIError
import psutil
import os
import http.client

class shopifyStream(GraphQLStream):
    """shopify stream class."""

    query_name = None

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        shop = self.config["shop"][:-len(".myshopify.com")] if self.config["shop"].endswith(".myshopify.com") else self.config["shop"]
        return f"https://{shop}.myshopify.com/admin/api/2024-07/graphql.json"

    @property
    def authenticator(self) -> ShopifyAuthenticator:
        """Return a new authenticator object."""
        if self.config.get("client_id"):
            shop = self.config["shop"][:-len(".myshopify.com")] if self.config["shop"].endswith(".myshopify.com") else self.config["shop"]
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

    @cached_property
    def selected_properties(self):
        selected_properties = []
        for key, value in self.metadata.items():
            if isinstance(key, tuple) and len(key) == 2 and value.selected:
                field_name = key[-1]
                selected_properties.append(field_name)
        return selected_properties

    @property
    def gql_selected_fields(self):
        schema = self.schema["properties"]
        catalog = {k: v for k, v in schema.items() if k in self.selected_properties}

        output = []
        for key, value in catalog.items():
            if "items" in value:
                value = value["items"]
            if key == "lineItems":
                # Handle lineItems pagination
                if hasattr(self, 'first_line_item'):
                    after_param = f" after:{self.after_line_item}" if hasattr(self, 'after_line_item') and self.after_line_item else ""
                    query = self.get_field_query(key, value["properties"], is_paginated=True, page_size=self.first_line_item)
                else:
                    query = self.get_field_query(key, value["properties"])
                output.append(query)
            elif "properties" in value:
                query = self.get_field_query(key, value["properties"])
                output.append(query)
            else:
                output.append(key)

        return "\n".join(output)

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the GraphQL API request."""
        params = self.get_url_params(context, next_page_token)
        query = self.query.lstrip()
        request_data = {
            "query": (" ".join([line.strip() for line in query.splitlines()])),
            "variables": params,
        }
        # self.logger.info(f"Attempting request with variables {params} and query: {request_data['query']}")
        return request_data

    def get_field_query(self, field_name: str, schema: dict, is_paginated: bool = False, page_size: int = None) -> str:
        """Generate a GraphQL query string for a given field based on its schema."""
        output = []

        if is_paginated:
            pagination = f"(first: {page_size})" if page_size else ""
            output.append(f"{field_name}{pagination} {{")
            output.append("edges {")
            output.append("cursor")
            output.append("node {")
        else:
            output.append(f"{field_name} {{")

        for key, value in schema.items():
            if "items" in value:
                value = value["items"]
            if "properties" in value:
                nested_query = self.get_field_query(key, value["properties"])
                output.append(nested_query)
            else:
                output.append(key)

        if is_paginated:
            output.append("}")  # Close node
            output.append("}")  # Close edges
            output.append("pageInfo { hasNextPage }")
        output.append("}")

        return "\n".join(output)

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
            base=3,
        )(func)
        return decorator
    
    def log_memory_usage(self, tag=""):
        process = psutil.Process(os.getpid())
        mem = process.memory_info().rss / (1024 * 1024)  # In MB
        self.logger.info(f"[MEMORY] {tag}: {mem:.2f} MB")
