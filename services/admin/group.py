from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader

class Group(BaseService):
    """
    Service for admin group management operations in FileCloud.
    """

    def __init__(self, session, user_type, base_url: str):
        """
        Initialize the Group service.
        """
        super().__init__(session, base_url)
        self.admin_service_info = EndpointsLoader(user_type).get_endpoints()
        self.endpoint = self.admin_service_info['default_endpoint']
        self.group_service = self.admin_service_info['group']
    
    def add_new_group(self, group_name: str):
        """
        Add a new group to FileCloud.
        """
        operation = self.group_service['add_group']['operation']
        params = {"op": operation, "groupname": group_name}
        return self.post(endpoint=self.endpoint, data=params)

    def get_groups(self):
        """
        Retrieve all groups.
        """
        operation = self.group_service['get_groups']['operation']
        return self.get(endpoint=self.endpoint, params={"op": operation})

    def get_group_by_name(self, group_name: str):
        """
        Retrieve a group's details by name.
        """
        operation = self.group_service['get_group_by_name']['operation']
        params = {"op": operation, "groupname": group_name}
        return self.get(endpoint=self.endpoint, params=params)

    def add_member_to_group(self, group_id : str, user_id: str):
        """
        Add a new group to FileCloud.
        """
        operation = self.group_service['add_member_to_group']['operation']
        params = {"op": operation, "groupid": group_id, "userid": user_id}
        return self.post(endpoint=self.endpoint, data=params)