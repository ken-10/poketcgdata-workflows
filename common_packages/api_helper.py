import logging
import requests
from enums.APIResource import APIResource


def get_all(api_url: str, api_key: str, resource: APIResource, timeout_in_seconds: float = 30):
    """
    Visit following link for supported resources - https://docs.pokemontcg.io/
    """
    if not isinstance(resource,APIResource):
        raise TypeError("Incorrect resource parameter provided!")

    params = {'page': 1}
    results = []
    logging.info(f"Getting all {resource.value}")
    retrieved_count = 0
    while True:
        url = f'{api_url}/{resource.value}'
        rest_client = RestApiClient(url, api_key, timeout_in_seconds)
        response = rest_client.get(params).json()
        response_data = response['data']
        if len(response_data) <= 0:
            break
        results.extend(response_data)
        retrieved_count += len(response_data)
        logging.info(f'Retrieved {retrieved_count} {resource.value}')

        # Types, subtypes, supertypes, and rarities do not have pages
        if 'page' in response:
            params['page'] += 1
        else:
            break
    return results


class RestApiClient:
    def __init__(self, api_url: str, api_key: str, timeout_in_seconds: float = 30):
        self.api_url = api_url
        self.api_key = api_key
        self.timeout_in_seconds = timeout_in_seconds

    def get(self, params: dict = None):
        headers = {'Content-Type': 'applications/json'}
        try:
            if self.api_key:
                headers['x-api-key'] = self.api_key
            if params is not None:
                response = requests.get(url=self.api_url, headers=headers, params=params,
                                        timeout=self.timeout_in_seconds)
            else:
                response = requests.get(url=self.api_url, headers=headers, timeout=self.timeout_in_seconds)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as http_err:
            raise
        except requests.exceptions.ConnectionError as conn_err:
            raise
        except requests.exceptions.Timeout as timeout_err:
            raise
        except requests.exceptions.RequestException as req_err:
            raise
