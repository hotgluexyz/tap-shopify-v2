"""GraphQL client handling, including shopifyStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk.streams import GraphQLStream
from singer_sdk.helpers.jsonpath import extract_jsonpath
from backports.cached_property import cached_property


class shopifyStream(GraphQLStream):
    """shopify stream class."""

    query_name = None

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        shop = self.config["shop"]
        return f"https://{shop}.myshopify.com/admin/api/2021-07/graphql.json"

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        headers["X-Shopify-Access-Token"] = self.config.get("api_key")
        headers["Content-Type"] = "application/json"
        return headers
    
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
        catalog = {k:v for k, v in schema.items() if k in self.selected_properties}

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
        self.logger.debug(f"Attempting query:\n{query}")
        return request_data
