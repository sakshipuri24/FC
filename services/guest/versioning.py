from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader

class Versioning(BaseService):
    """
    Service for handling file versioning operations in FileCloud as a guest user.
    """

    def __init__(self, session, user_type, base_url: str):
        """
        Initialize the Versioning service.
        """
        super().__init__(session, base_url)
        self.endpoints = EndpointsLoader(user_type).get_endpoints()["versioning"]

    def get_versions(self, params: dict):
        """
        Retrieve file versions for a given file.
        """
        return self.post(self.endpoints["get_versions"], data=params)