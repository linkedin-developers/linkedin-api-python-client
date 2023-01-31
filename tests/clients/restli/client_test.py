from linkedin_api.clients.restli.client import RestliClient
import pytest
import responses
from linkedin_api.common.constants import NON_VERSIONED_BASE_URL, RESTLI_METHOD_TO_HTTP_METHOD_MAP

ACCESS_TOKEN = "ABC123"

"""
Tests for basic functionality of the RestliClient methods, providing
the input request options and method type and expected response.
"""


@pytest.mark.parametrize(
    "restli_method,request_args,input_response,expected_request",
    [
        (
            "get",
            {
                # request_args
                "resource_path": "/adAccounts/{id}",
                "path_keys": { "id": 123 },
                "access_token": ACCESS_TOKEN
            },
            {
                # input_response
                "json": {"name": "TestAdAccount"},
                "status": 200
            },
            {
                # expected_request
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/adAccounts/123"
            }
        ),
        (
            "get",
            {
                # request_args
                "resource_path": "/adAccounts/{id}",
                "path_keys": { "id": 123 },
                "query_params": {
                  "param1": "foobar"
                },
                "access_token": ACCESS_TOKEN
            },
            {
                # input_response
                "json": {"name": "TestAdAccount"},
                "status": 200
            },
            {
                # expected_request
                "base_url": NON_VERSIONED_BASE_URL,
                "path": "/adAccounts/123?param1=foobar"
            }
        )
    ]
)
@responses.activate
def test_restliclient(
        restli_method, request_args, input_response, expected_request):
    restli_client = RestliClient()

    # Create the expected url based on restli method and path
    http_method = RESTLI_METHOD_TO_HTTP_METHOD_MAP[restli_method.upper()].lower()
    expected_full_url = expected_request["base_url"] + expected_request["path"]
    expected_url_no_params = expected_full_url.split('?')[0]

    # Mock the requests method according to expected_request
    getattr(responses, http_method)(
      url=expected_url_no_params,
      json=input_response["json"],
      status=input_response["status"]
    )

    # Run RestliClient method with provided request args
    response = getattr(restli_client, restli_method)(**request_args)

    # Verify
    responses.assert_call_count(expected_full_url, 1)
    assert response.status_code == input_response["status"]
    assert response.entity == input_response["json"]