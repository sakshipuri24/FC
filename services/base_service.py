import requests

class BaseService:
    """
    Base service for making HTTP requests to the FileCloud API.
    """

    def __init__(self, session, base_url: str):
        """
        Initialize with a requests.Session and base URL.
        """
        self.base_url = base_url
        self.session = session

    def get(self, endpoint: str, cookies: dict = None, headers: dict = None, params: dict = None):
        """
        Send a GET request to the given endpoint.
        """
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, cookies=cookies, headers=headers, params=params)

    def post(self, endpoint: str, files=None, cookies: dict = None, headers: dict = None, data: dict = None):
        """
        Send a POST request to the given endpoint.
        """
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, cookies=cookies, headers=headers, data=data, files=files)

    def put(self, endpoint: str, data: dict = None):
        """
        Send a PUT request to the given endpoint.
        """
        url = f"{self.base_url}{endpoint}"
        return self.session.put(url, data=data)

    def delete(self, endpoint: str):
        """
        Send a DELETE request to the given endpoint.
        """
        url = f"{self.base_url}{endpoint}"
        return self.session.delete(url)