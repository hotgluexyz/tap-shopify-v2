"""GraphQL client handling, including shopifyStream base class."""

from time import sleep
from typing import Any, Dict, Iterable, List, Optional, Union

import requests
from backports.cached_property import cached_property
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import GraphQLStream
import math

from tap_shopify_beta.client import shopifyStream


class shopifyGqlStream(shopifyStream):
    """shopify stream class."""

    page_size = 1
    query_cost = None
    available_points = None
    restore_rate = None
    max_points = None
    single_object_params = None
    is_list = True

    @property
    def page_size(self) -> int:
        if not self.available_points:
            return 1
        pages = self.available_points / self.query_cost
        if pages < 5:
            points_to_restore = self.max_points - self.available_points
            sleep(points_to_restore // self.restore_rate - 1)
            pages = (self.max_points - self.restore_rate) / self.query_cost
            pages = pages - 1
        elif self.query_cost and pages>5:
            if self.query_cost * pages >= 1000:
                pages = math.floor(1000/self.query_cost)
            else:
                pages = 250 if pages > 250 else pages
        return int(pages)

    @cached_property
    def query(self) -> str:
        """Set or return the GraphQL query string."""

        if self.single_object_params:
            base_query = """
                query tapShopify($id: ID!) {
                    __query_name__(id: $id) {
                        __selected_fields__
                    }
                }
            """
        elif not self.replication_key and not self.is_list:
            base_query = """
                query {
                    __query_name__ {
                        __selected_fields__
                    }
                }
            """
        else:
            base_query = """
                query tapShopify($first: Int, $after: String, $filter: String) {
                    __query_name__(first: $first, after: $after, query: $filter) {
                        edges {
                            cursor
                            node {
                                __selected_fields__
                            }
                        },
                        pageInfo {
                            hasNextPage
                        }
                    }
                }
            """

        query = base_query.replace("__query_name__", self.query_name)
        query = query.replace("__selected_fields__", self.gql_selected_fields)

        return query

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Any:
        """Return token identifying next page or None if all records have been read."""
        if not self.replication_key:
            return None
        response_json = response.json()
        has_next_json_path = f"$.data.{self.query_name}.pageInfo.hasNextPage"
        has_next = next(extract_jsonpath(has_next_json_path, response_json))
        if has_next:
            cursor_json_path = f"$.data.{self.query_name}.edges[-1].cursor"
            all_matches = extract_jsonpath(cursor_json_path, response_json)
            return next(all_matches, None)
        return None

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params = {}
        params["first"] = self.page_size
        if next_page_token:
            params["after"] = next_page_token
        if self.replication_key:
            start_date = self.get_starting_timestamp(context)
            if start_date:
                date = start_date.strftime("%Y-%m-%dT%H:%M:%S")
                params["filter"] = f"updated_at:>{date}"
        if self.single_object_params:
            params = self.single_object_params
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        self.logger.info(f"Parsing response for stream {self.name}")
        if self.replication_key:
            json_path = f"$.data.{self.query_name}.edges[*].node"
        else:
            json_path = f"$.data.{self.query_name}"
        response = response.json()

        cost = response["extensions"].get("cost")
        if not self.query_cost:
            self.query_cost = cost.get("requestedQueryCost")
        self.available_points = cost["throttleStatus"].get("currentlyAvailable")
        self.restore_rate = cost["throttleStatus"].get("restoreRate")
        self.max_points = cost["throttleStatus"].get("maximumAvailable")

        yield from extract_jsonpath(json_path, input=response)
 
