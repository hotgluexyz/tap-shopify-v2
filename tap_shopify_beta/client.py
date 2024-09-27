"""GraphQL client handling, including shopifyStream base class."""

from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Union

import requests
from singer_sdk.authenticators import APIKeyAuthenticator
from backports.cached_property import cached_property
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import GraphQLStream
from tap_shopify_beta.auth import ShopifyAuthenticator


class shopifyStream(GraphQLStream):
    """shopify stream class."""

    query_name = None

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        shop = self.config["shop"]
        return f"https://{shop}.myshopify.com/admin/api/2024-01/graphql.json"
    
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

        def denest_schema(schema):
            output = ""
            for key, value in schema.items():
                if "items" in value.keys():
                    value = value["items"]
                if "properties" in value.keys():
                    denested = denest_schema(value["properties"])
                    output = f"{output}\n{key}\n{{{denested}\n}}"
                else:
                    output = f"{output}\n{key}"
            return output

        return denest_schema(catalog)

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
        self.logger.info(f"Attempting request with variables {params} and query:\n{query}")
        return request_data
