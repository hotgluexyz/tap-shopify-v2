"""GraphQL client handling, including shopify-betaStream base class."""

from datetime import datetime, timedelta, timezone
from time import sleep
from typing import Any, Dict, Iterable, List, Optional, Union, cast

import requests
import simplejson
from backports.cached_property import cached_property
from singer_sdk.helpers.jsonpath import extract_jsonpath

from tap_shopify_beta.client import shopifyStream
import re


class InvalidOperation(requests.RequestException, ValueError):
    """Invalid job id."""


class OperationFailed(requests.RequestException, ValueError):
    """Operation Failed."""


class shopifyBulkStream(shopifyStream):
    """shopify stream class."""

    start_date = None
    end_date = None

    @property
    def query(self) -> str:
        """Set or return the GraphQL query string."""
        if self.name == "shop":
            base_query = """
                query {
                    __query_name__ {
                        __selected_fields__
                    }
                }
                """
        else:
            base_query = '''
                mutation {
                bulkOperationRunQuery(
                    query:"""
                        {
                            __query_name____filters__ {
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
                ) 
                    {
                        bulkOperation {
                            id
                            status
                        }
                        userErrors {
                            field
                            message
                        }
                    }
                }
                '''

        query = base_query.replace("__query_name__", self.query_name)
        query = query.replace("__selected_fields__", self.gql_selected_fields)
        query = query.replace("__filters__", self.filters)

        return query

    @property
    def filters(self):
        """Return a dictionary of values to be used in URL parameterization."""
        if self.replication_key:
            self.start_date = self.start_date or self.get_starting_timestamp({})
            if self.start_date:
                date = self.start_date.strftime("%Y-%m-%dT%H:%M:%S")
                self.end_date = self.start_date + timedelta(days=1)
                query = f'(query: "updated_at:>{date} AND updated_at:<={self.end_date.strftime("%Y-%m-%dT%H:%M:%S")}")'
            return query
        return ""

    def get_operation_status(self):

        query = """
            query {
                currentBulkOperation {
                    id
                    status
                    errorCode
                    createdAt
                    completedAt
                    objectCount
                    fileSize
                    url
                    partialDataUrl
                }
            }
        """

        headers = self.http_headers
        authenticator = self.authenticator
        if authenticator:
            headers.update(authenticator.auth_headers or {})

        request = cast(
            requests.PreparedRequest,
            self.requests_session.prepare_request(
                requests.Request(
                    method=self.rest_method,
                    url=self.get_url({}),
                    headers=headers,
                    json=dict(query=query, variables={}),
                ),
            ),
        )

        decorated_request = self.request_decorator(self._request)
        response = decorated_request(request, {})

        return response

    def check_status(self, operation_id, sleep_time=20, timeout=7200):

        status_jsonpath = "$.data.currentBulkOperation"
        start = datetime.now().timestamp()

        while datetime.now().timestamp() < (start + timeout):
            status_response = self.get_operation_status()
            status = next(
                extract_jsonpath(status_jsonpath, input=status_response.json())
            )
            if status["id"] != operation_id:
                raise InvalidOperation(
                    "The current job was not triggered by the process, check if other service is using the Bulk API"
                )
            if status["status"] == "FAILED":
                raise InvalidOperation(f"Job failed: {status['errorCode']}")
            if status["status"] == "COMPLETED":
                return status["url"]
            sleep(sleep_time)
        raise OperationFailed("Job Timeout")
    
    def get_line_type(self, id):
        match = re.search(r"gid://shopify/([^/]+)/", id)
        if match:
            return match.group(1)

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        operation_id_jsonpath = "$.data.bulkOperationRunQuery.bulkOperation.id"
        request_response = response.json()
        operation_id =  next(
            extract_jsonpath(operation_id_jsonpath, input=request_response), None
        )

        if not operation_id:
            raise Exception(response.json())

        url = self.check_status(operation_id)

        if url:
            output = requests.get(url, stream=True)

            parent_line = None
            for line in output.iter_lines():
                line = simplejson.loads(line)
                if hasattr(self, "bulk_process_fields"):
                    if parent_line and not line.get("__parentId"):
                        yield parent_line
                        parent_line = None
                    if not parent_line and not line.get("__parentId"):
                        parent_line = line
                    if line.get("__parentId"):
                        line_type = self.get_line_type(line["id"])
                        if line_type in self.bulk_process_fields:
                            line_field_name = self.bulk_process_fields[line_type]
                            if not parent_line.get(line_field_name):
                                parent_line[line_field_name] = {"edges": [{"node": line}]}
                            else:
                                parent_line[line_field_name]["edges"].append({"node": line}) 
                            continue
                else:
                    yield line
            # yield final record
            if parent_line:
                yield parent_line

    def get_next_page_token(self, response, previous_token) -> Any:
        if self.end_date <= datetime.now(timezone.utc):
            self.start_date = self.end_date
            return self.start_date

