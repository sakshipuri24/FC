import yaml
import os

class EndpointsLoader:
    """
    Loads API endpoints for a given user type from a YAML file.
    """

    def __init__(self, user_type: str):
        """
        Initialize the EndpointsLoader.

        Args:
            user_type (str): The user type (e.g., 'admin', 'guest').
        """
        self.user_type = user_type
        self.endpoint_file_path = f'config/endpoints.yaml'
        self.endpoints = self.load_endpoints()

    def load_endpoints(self):
        """
        Load endpoints from the YAML file.

        Returns:
            dict: Endpoints dictionary.

        Raises:
            FileNotFoundError: If the endpoints file does not exist.
        """
        if not os.path.exists(self.endpoint_file_path):
            raise FileNotFoundError(f"Endpoints file not found: {self.endpoint_file_path}")

        with open(self.endpoint_file_path, 'r') as file:
            endpoints = yaml.safe_load(file)

        return endpoints

    def get_endpoints(self):
        """
        Get the loaded endpoints for the specified user type.

        Returns:
            dict: Endpoints dictionary for the user type.
        """
        return self.endpoints[self.user_type]