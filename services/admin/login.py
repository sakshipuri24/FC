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
        self.admin_service_info = EndpointsLoader(user_type).get_endpoints()
        self.endpoint = self.admin_service_info['default_endpoint']
        self.login_service = self.admin_service_info['login']

    def admin_login(self, username: str, password: str, headers: dict):
        """
        Log in as a guest user.
        """
        operation = self.login_service['login']['operation']
        params = {"op": operation,"adminuser": username, "adminpassword": password}
        return self.post(self.endpoint, data=params, headers=headers)

    def admin_logout(self):
        """
        Log out the current guest user session.
        """
        operation = self.login_service['logout']['operation']
        return self.post(self.endpoint, data={"op": operation})