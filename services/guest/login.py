from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader

class Login(BaseService):
    """
    Service for guest user login operations in FileCloud.
    """

    def __init__(self, session, user_type: str, base_url: str):
        """
        Initialize the Login service.
        """
        super().__init__(session, base_url)
        self.endpoints = EndpointsLoader(user_type).get_endpoints()["login"]

    def login(self, username: str, password: str, headers: dict):
        """
        Log in as a guest user.
        """
        params = {"userid": username, "password": password}
        return self.post(self.endpoints["login"], data=params, headers=headers)

    def logout(self):
        """
        Log out the current guest user session.
        """
        return self.post(self.endpoints["logout"])