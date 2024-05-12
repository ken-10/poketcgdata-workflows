import pytest
from dags.common_packages.api_helper import RestApiClient


@pytest.mark.parametrize("input_params", [({"api_key": "API_KEY", "api_url": "API_URL", "timeout_in_seconds": 10}),
                                          ({"api_key": "API_KEY", "api_url": "API_URL"})])
def test_rest_api_client_initialization(input_params):
    expected_attributes = input_params
    if "timeout_in_seconds" not in input_params:
        rest_client = RestApiClient(api_url=input_params["api_url"], api_key=input_params["api_key"])
        expected_attributes["timeout_in_seconds"] = 30
    else:
        rest_client = RestApiClient(api_url=input_params["api_url"], api_key=input_params["api_key"],
                                    timeout_in_seconds=input_params["timeout_in_seconds"])

    assert rest_client.__dict__ == expected_attributes
    