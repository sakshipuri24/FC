from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader

class File(BaseService):
    """
    Service for file operations in FileCloud as a guest user.
    """

    def __init__(self, session, user_type, base_url: str):
        """
        Initialize the File service.
        """
        super().__init__(session, base_url)
        self.endpoints = EndpointsLoader(user_type).get_endpoints()["file"]

    def file_exists(self, path: str):
        """
        Check if a file exists at the given path.
        """
        return self.post(self.endpoints["file_exists"], data={"file": path})

    def upload_file(self, params: dict, files: dict):
        """
        Upload a file to FileCloud.
        """
        return self.post(self.endpoints["upload_file"], files=files, data=params) 

    def delete_file(self, path:str, name:str):
        """
        Delete a file from FileCloud.
        """
        return self.post(self.endpoints["delete_file"],
                         data={"path": path,
                                 "name": name})

    def get_file_info(self, params: dict):
        """
        Retrieve information about a file.
        """
        return self.post(self.endpoints["get_file_info"], data=params)