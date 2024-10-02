"""GraphQL client handling, including shopifyStream base class."""

from time import sleep
from typing import Any, Dict, Iterable, List, Optional, Union, cast

import requests
from backports.cached_property import cached_property
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import GraphQLStream
import math

from tap_shopify_beta.client import shopifyStream
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz
import copy

class shopifyGqlStream(shopifyStream):
    """shopify stream class."""

    page_size = 1
    query_cost = None
    available_points = None
    restore_rate = None
    max_points = None
    single_object_params = None
    is_list = True
    json_path = None
    start_date = None
    end_date = None

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
        elif getattr(self, "is_sortable", None) is False:
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
        else:
            base_query = """
                query tapShopify($first: Int, $after: String, $filter: String) {
                    __query_name__(first: $first, after: $after, query: $filter, sortKey: UPDATED_AT) {
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
        elif self.config.get(f"sync_{self.name}_monthly") and not has_next:
            today = datetime.now().replace(tzinfo=pytz.UTC)
            if self.end_date < today:
                self.start_date = self.start_date + relativedelta(months=1)
                self.logger.info(f"Reached end of data for current month. Moving start date to {self.start_date}")
                # make self.available_points None so page_size calculation is accurate
                self.available_points = None
                return 0
        self.logger.info(f"Finishing sync for stream {self.name}")
        return None

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params = dict()
        params["first"] = self.page_size
        if next_page_token:
            params["after"] = next_page_token
        if self.replication_key:
            start_date = self.start_date or self.get_starting_timestamp(context)
            if start_date:
                date = start_date.strftime("%Y-%m-%dT%H:%M:%S")
                date_filter = f"updated_at:>{date}"
                # fetch data in monthly chunks
                if self.config.get(f"sync_{self.name}_monthly"):
                    self.start_date = start_date
                    self.end_date = start_date + relativedelta(months=1)
                    end_date = self.end_date.strftime("%Y-%m-%dT%H:%M:%S")
                    date_filter = f"{date_filter} AND updated_at:<={end_date}"
                params["filter"] = date_filter
        if self.single_object_params:
            params = self.single_object_params
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        self.logger.info(f"Parsing response for stream {self.name}")
        if self.json_path:
            json_path = self.json_path
        elif self.replication_key:
            json_path = f"$.data.{self.query_name}.edges[*].node"
        else:
            json_path = f"$.data.{self.query_name}"
        res_json = response.json()

        if "errors" in res_json:
            for error in res_json["errors"]:
                self.logger.error(f"Error message: {error['message']}")
                self.logger.error(f"Error locations: {error['locations']}")
                self.logger.error(f"Error path: {error['path']}")
                self.logger.error(f"Error extensions: {error['extensions']}")
            raise Exception(f"Error during parse_response. messages: {res_json['errors']}")

        cost = res_json["extensions"].get("cost")
        if not self.query_cost:
            self.query_cost = cost.get("requestedQueryCost")
        self.available_points = cost["throttleStatus"].get("currentlyAvailable")
        self.restore_rate = cost["throttleStatus"].get("restoreRate")
        self.max_points = cost["throttleStatus"].get("maximumAvailable")

        filtered_response = self.filter_response(res_json)
        yield from extract_jsonpath(json_path, input=filtered_response)

    def filter_response(self, response_json: dict) -> dict:
        return response_json
    
    def prepare_request(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> requests.PreparedRequest:
        http_method = self.rest_method
        url: str = self.get_url(context)
        params: dict = {}
        request_data = self.prepare_request_payload(context, next_page_token)
        headers = self.http_headers

        authenticator = self.authenticator
        if authenticator:
            headers.update(authenticator.auth_headers or {})
            params.update(authenticator.auth_params or {})

        request = cast(
            requests.PreparedRequest,
            self.requests_session.prepare_request(
                requests.Request(
                    method=http_method,
                    url=url,
                    params=params,
                    headers=headers,
                    json=request_data,
                ),
            ),
        )
        return request

    def request_records(self, context: Optional[dict]) -> Iterable[dict]:
        next_page_token: Any = None
        finished = False
        decorated_request = self.request_decorator(self._request)

        while not finished:
            prepared_request = self.prepare_request(
                context, next_page_token=next_page_token
            )
            resp = decorated_request(prepared_request, context)
            yield from self.parse_response(resp)
            previous_token = copy.deepcopy(next_page_token)
            next_page_token = self.get_next_page_token(
                response=resp, previous_token=previous_token
            )
            if next_page_token and next_page_token == previous_token:
                raise RuntimeError(
                    f"Loop detected in pagination. "
                    f"Pagination token {next_page_token} is identical to prior token."
                )
            # Cycle until get_next_page_token() no longer returns a value
            finished = next_page_token is None