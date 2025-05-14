"""GraphQL client handling, including shopifyStream base class."""

from time import sleep
from typing import Any, Dict, Iterable, List, Optional, Union, cast, Callable

import requests
import urllib3
from backports.cached_property import cached_property
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import GraphQLStream
import math

from tap_shopify_beta.client import shopifyStream
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz
import copy
from singer_sdk.exceptions import RetriableAPIError
import backoff
import concurrent.futures
import queue
import threading
from pendulum import parse


class GraphQLInternalServerError(RetriableAPIError):
    """Error raised when Shopify returns an internal server error in the GraphQL response."""
    pass

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
    sort_key = None
    sort_key_type = None

    @property
    def page_size(self) -> int:
        if self.available_points is None:
            return 1
            
        # If we don't have enough points for at least 2 queries, wait
        if self.available_points < self.query_cost * 5:
            points_needed = self.query_cost * 5 - self.available_points
            seconds_to_wait = math.ceil(points_needed / self.restore_rate)
            self.logger.info(f"Waiting {seconds_to_wait} seconds for {points_needed} more points to become available")
            sleep(seconds_to_wait)
            # Update available points after waiting
            self.available_points = min(
                self.available_points + (self.restore_rate * seconds_to_wait),
                self.max_points
            )
            
        # Calculate how many points we'll restore during the next query
        # Assuming average query takes 2 seconds to execute
        points_restored_during_query = self.restore_rate * 2
        # Calculate base pages from available points
        pages = (self.available_points + points_restored_during_query) / self.query_cost
        
        # Calculate maximum pages we can use without exceeding 1000 points
        max_pages = math.floor(1000 / self.query_cost)
            
        # Use a more aggressive page size, but ensure we don't exceed max_pages
        target_pages = min(max_pages, pages)
        
        self.logger.info(f"Thread: {threading.current_thread().name} Using {target_pages * self.query_cost} points, Available points: {self.available_points}")

        # NOTE: this was somehow broken for non-orders streams
        if self.name != "orders":
            return min(int(target_pages), 250)

        # For smaller page counts, still use them but be more conservative
        return int(target_pages)

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
        elif self.sort_key and self.sort_key_type:
            base_query = """
                query tapShopify($first: Int, $after: String, $filter: String, $sortKey: __sort_key_type__) {
                    __query_name__(first: $first, after: $after, query: $filter, sortKey: $sortKey) {
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
            base_query = base_query.replace("__sort_key_type__", self.sort_key_type)
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

        if hasattr(self, "additional_arguments"):
            for key, value in self.additional_arguments.items():
                query = query.replace(key, f"{key} {value}")

        self.logger.info(f"Query: {query}")
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

        self.logger.info(f"URL Params: {params}")
        if self.replication_key:
            # fetch data in monthly chunks
            if self.config.get(f"sync_{self.name}_monthly"):
                start_date = self.start_date or self.get_starting_timestamp(context)
                date = start_date.strftime("%Y-%m-%dT%H:%M:%S")
                date_filter = f"updated_at:>{date}"
                self.start_date = start_date
                self.end_date = start_date + relativedelta(months=1)
                end_date = self.end_date.strftime("%Y-%m-%dT%H:%M:%S")
                date_filter = f"{date_filter} AND updated_at:<={end_date}"
                params["filter"] = date_filter
            elif context and context.get("date_range"):
                date_filter = f"updated_at:>{context['date_range']['start_date']}"
                if context['date_range'].get('end_date'):
                    date_filter = f"{date_filter} AND updated_at:<={context['date_range']['end_date']}"
                params["filter"] = date_filter
        if self.single_object_params:
            params = self.single_object_params
        if self.sort_key:
            params["sortKey"] = self.sort_key
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

        errors = res_json.get("errors")

        cost = res_json["extensions"].get("cost")
        if not self.query_cost:
            self.query_cost = (cost.get("actualQueryCost") + cost.get("requestedQueryCost")) / 2
        self.available_points = cost["throttleStatus"].get("currentlyAvailable")
        self.restore_rate = cost["throttleStatus"].get("restoreRate")
        self.max_points = cost["throttleStatus"].get("maximumAvailable")

        filtered_response = self.filter_response(res_json)
        records = list(extract_jsonpath(json_path, input=filtered_response))
        if errors and not records:
            raise Exception(errors)
        if errors:
            self.logger.info(f"Issue found while fetching {self.name}, response: {errors}")
        yield from records

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

    def validate_response(self, response: requests.Response) -> None:
        """Validate GraphQL response. Will raise RetriableAPIError if internal server error is found."""
        self.logger.info(f"Validating response for stream {self.name}. request: {response.request.body}")
        super().validate_response(response)

        try:
            resp_json = response.json()
            errors = resp_json.get("errors", [])
            if not resp_json.get("data"):
                for error in errors:
                    extensions = error.get("extensions", {})
                    if extensions.get("code") == "INTERNAL_SERVER_ERROR":
                        raise GraphQLInternalServerError(
                            f"Shopify GraphQL Internal Server Error: {error.get('message')}",
                            response
                        )
                    if extensions.get("code") == "THROTTLED":
                        import time
                        time.sleep(5)
                        raise RetriableAPIError(
                            f"Shopify GraphQL Throttled Error: {error.get('message')}",
                            response
                        )
        except ValueError:
            # If response is not JSON, let the parent validator handle it
            pass
    
    def backoff_wait_generator(self):
        # Use exponential backoff between min_wait and 30 seconds
        min_wait = 1000 / self.restore_rate if self.restore_rate else 10
        return backoff.expo(base=2, factor=min_wait, max_value=30)
    

    def request_decorator(self, func: Callable) -> Callable:
        decorator: Callable = backoff.on_exception(
            self.backoff_wait_generator,
            (
                RetriableAPIError,
                GraphQLInternalServerError,
                urllib3.exceptions.HTTPError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError,
                requests.exceptions.RequestException,
                ConnectionError,
            ),
            max_tries=10,
            on_backoff=self.backoff_handler,
        )(func)
        return decorator
    
    def get_earliest_replication_key(self, context: dict) -> Optional[datetime]:
            base_query = """
                query tapShopify($sortKey: __sort_key_type__) {
                    __query_name__(first: 1, sortKey: $sortKey) {
                        edges {
                            node {
                                __replication_key__
                            }
                        }
                    }
                }
            """
            query = base_query.replace("__sort_key_type__", self.sort_key_type)
            query = query.replace("__query_name__", self.query_name)
            query = query.replace("__replication_key__", self.replication_key)

            request_data = {
                "query": (" ".join([line.strip() for line in query.splitlines()])),
                "variables": {"sortKey": self.sort_key}
            }
            headers = self.http_headers
            headers.update(self.authenticator.auth_headers or {})
            request = cast(
                requests.PreparedRequest,
                self.requests_session.prepare_request(
                    requests.Request(
                        method="POST",
                        url=self.url_base,
                        params=None,
                        headers=self.http_headers,
                        json=request_data,
                    ),
                ),
            )
            resp = self._request(request, None)
            resp_json = resp.json()
            earliest_rep_key = resp_json.get("data", {}).get(self.query_name, {}).get("edges", [{}])[0].get("node", {}).get(self.replication_key)
            return parse(earliest_rep_key)

    def get_concurrent_params(self, context):
        """Generate list of date range parameters for concurrent requests.
        
        Args:
            context: Stream context
            max_requests: Maximum number of concurrent requests
            
        Returns:
            List of parameter dicts with start_date and end_date for each partition
        """            
        start_date = self.start_date or self.get_starting_timestamp(context)

        # make a request to get the earliest rep key value
        if self.replication_key and self.sort_key:
            earliest_rep_key = self.get_earliest_replication_key(context)
            if earliest_rep_key > start_date:
                start_date = earliest_rep_key
            
        # Get current time in UTC
        now = datetime.now(pytz.UTC)
        
        # Calculate time range between start_date and now
        total_time_range = now - start_date
        
        # Calculate time interval for each partition
        interval = total_time_range / self.max_requests
        
        params = []
        for i in range(self.max_requests):
            context = copy.deepcopy(context) or {}
            date_range = {}
            date_range["start_date"] = start_date + (interval * i)
            # don't set end_date for the last partition
            if not i == self.max_requests - 1:
                date_range["end_date"] = start_date + (interval * (i + 1))
           
            context["date_range"] = date_range
            params.append(context)
            
        return params

    @cached_property
    def max_requests(self):
        # flag for testing, so new request doesn't break previous tests
        if not self.config.get("apply_concurrency", True):
            return 1
        # check how many points are available
        query = """
            query {
                shop {
                    name
                }
            }
        """
        request_data = {
            "query": (" ".join([line.strip() for line in query.splitlines()])),
            "variables": {}
        }
        headers = self.http_headers
        headers.update(self.authenticator.auth_headers or {})
        request = cast(
            requests.PreparedRequest,
            self.requests_session.prepare_request(
                requests.Request(
                    method="POST",
                    url=self.url_base,
                    params=None,
                    headers=self.http_headers,
                    json=request_data,
                ),
            ),
        )
        resp = self._request(request, None)
        resp_json = resp.json()
        max_available = resp_json.get("extensions", {}).get("cost", {}).get("throttleStatus", {}).get("maximumAvailable", 2000)

        # Calculate number of partitions based on available points
        return math.floor(max_available / 1000)
    
    def safe_put(self, q: queue.Queue, record: dict):
        while True:
            try:
                q.put(record, timeout=1)
                break
            except queue.Full:
                continue
    
    def concurrent_request(self, context: dict, record_queue: queue.Queue):
        try:
            next_page_token = None
            finished = False
            decorated_request = self.request_decorator(self._request)

            while not finished:
                self.logger.info(f"[{threading.current_thread().name}] Fetching next page...")
                prepared = self.prepare_request(context, next_page_token=next_page_token)
                resp = decorated_request(prepared, context)

                for record in self.parse_response(resp):
                    self.safe_put(record_queue, record)

                previous_token = copy.deepcopy(next_page_token)
                next_page_token = self.get_next_page_token(resp, previous_token)

                if next_page_token and next_page_token == previous_token:
                    raise RuntimeError("Pagination loop detected")

                finished = not next_page_token

        except Exception as e:
            self.logger.exception(e)
            record_queue.put(("ERROR", str(e)))
        finally:
            record_queue.put(None)

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        if self.config.get(f"sync_{self.name}_monthly") or self.max_requests < 2 or not self.replication_key:
            yield from super().get_records(context)
            return

        concurrent_params = self.get_concurrent_params(context)
        record_queue = queue.Queue()
        finished_threads = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_requests) as executor:
            futures = []
            for param in concurrent_params:
                future = executor.submit(self.concurrent_request, param, record_queue)
                futures.append(future)

            while finished_threads < len(concurrent_params):
                for future in futures:
                    if future.done():
                        try:
                            future.result()  # Raise errors from within threads
                        except Exception as e:
                            self.logger.exception(f"Error in worker thread: {str(e)}")
                            raise Exception(f"Worker thread error: {str(e)}")

                try:
                    record = record_queue.get(timeout=1)
                    if record is None:
                        finished_threads += 1
                        self.logger.info(f"[{threading.current_thread().name}] Worker finished")
                    elif isinstance(record, tuple) and record[0] == "ERROR":
                        self.logger.exception(f"Error from thread: {record[1]}")
                        raise Exception(f"Thread error: {record[1]}")
                    else:
                        self.logger.debug(f"Yielding record: {record}")
                        transformed = self.post_process(record, context)
                        if transformed:
                            yield transformed
                except queue.Empty:
                    self.logger.debug("Queue is empty, still waiting...")
                    continue

class GqlChildStream(shopifyGqlStream):

    json_path = "$.[*]"

    def filter_response(self, response_json: dict) -> dict:
        return list(response_json.get("data", []).values())

    def query(self, context: dict, context_key: str):
        # Build ID parameters based on page_size
        query_len = len(context.get(context_key, []))
        id_params = ", ".join([f"$id{i}: ID!" for i in range(1, query_len + 1)])

        query_blocks = "".join([
            f"""
                q{i}: __query_name__(id: $id{i}) {{
                    __selected_fields__
                }}
            """
            for i in range(1, query_len + 1)
        ])

        base_query = """query tapShopify(__id_params__) {
            __query_blocks__
        }"""

        query = base_query.replace("__id_params__", id_params)
        query = query.replace("__query_blocks__", query_blocks)
        query = query.replace("__query_name__", self.query_name)
        query = query.replace("__selected_fields__", self.gql_selected_fields)
        return query
    
    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the GraphQL API request."""
        ids = {f"id{i}": id_val for i, id_val in enumerate(context.get(self.context_key, []), start=1)}
        query = self.query(context, self.context_key).lstrip()
        request_data = {
            "query": (" ".join([line.strip() for line in query.splitlines()])),
            "variables": ids,
        }
        # self.logger.info(f"Attempting request with variables {params} and query: {request_data['query']}")
        return request_data