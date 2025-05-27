from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader

class User(BaseService):
    """
    Service for admin user management operations in FileCloud.
    """

    def __init__(self, session, user_type: str, base_url: str):
        """
        Initialize the User service.
        """
        super().__init__(session, base_url)
        self.admin_service_info = EndpointsLoader(user_type).get_endpoints()
        self.endpoint = self.admin_service_info['default_endpoint']
        self.user_service = self.admin_service_info['user']

    def add_new_user(self, user_data: dict):
        """
        Retrieve a user's details by username.
        """
        operation = self.user_service['add_user']['operation']
        params = {**{"op": operation}, **user_data}
        return self.post(endpoint=self.endpoint, data=params)
    
    def get_user(self, user_id: dict):
        """
        Add a new user to FileCloud.
        """
        operation = self.user_service['get_user']['operation']
        return self.post(endpoint=self.endpoint, data={"op": operation,"username": user_id})