"""GraphQL client handling, including shopify-betaStream base class."""

from datetime import datetime
from time import sleep
from typing import Any, Dict, Iterable, List, Optional, Union, cast

import requests
import simplejson
from backports.cached_property import cached_property
from singer_sdk.helpers.jsonpath import extract_jsonpath

from tap_shopify_beta.client import shopifyStream


class InvalidOperation(requests.RequestException, ValueError):
    """Invalid job id."""


class OperationFailed(requests.RequestException, ValueError):
    """Operation Failed."""


class shopifyBulkStream(shopifyStream):
    """shopify stream class."""

    @cached_property
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
            start_date = self.get_starting_timestamp({})
            if start_date:
                date = start_date.strftime("%Y-%m-%dT%H:%M:%S")
                return f'(query: "updated_at:>{date}")'
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

    def check_status(self, operation_id, sleep_time=10, timeout=1800):

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
            if status["url"]:
                return status["url"]
            if status["status"] == "FAILED":
                raise InvalidOperation(f"Job failed: {status['errorCode']}")
            sleep(sleep_time)
        raise OperationFailed("Job Timeout")

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        operation_id_jsonpath = "$.data.bulkOperationRunQuery.bulkOperation.id"
        request_response = response.json()
        operation_id = next(
            extract_jsonpath(operation_id_jsonpath, input=request_response)
        )

        url = self.check_status(operation_id)

        output = requests.get(url, stream=True)

        for line in output.iter_lines():
            yield simplejson.loads(line)
