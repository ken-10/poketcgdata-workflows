import requests


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
