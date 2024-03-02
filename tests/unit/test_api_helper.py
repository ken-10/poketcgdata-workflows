import pytest
from common_packages.api_helper import RestApiClient
from common_packages import api_helper


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


@pytest.mark.parametrize("input_params", [
    ({"api_key": "API_KEY", "api_url": "API_URL", "timeout_in_seconds": 10, "resource": "APIResource"})])
def test_get_all_failure(input_params):
    with pytest.raises(TypeError):
        api_helper.get_all(api_key=input_params["api_key"], api_url=input_params["api_url"],
                           timeout_in_seconds=input_params["timeout_in_seconds"], resource=input_params["resource"])
