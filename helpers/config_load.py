import yaml
import os

class ConfigLoader:
    """
    Loads configuration for a given environment from a YAML file.
    """

    def __init__(self, env):
        """
        Initialize the ConfigLoader.

        Args:
            env (str): Environment name (e.g., 'test', 'prod').
        """
        self.config_path = f'config/{env}.yaml'
        self.config = self.load_config()

    def load_config(self):
        """
        Load configuration from the YAML file.

        Returns:
            dict: Configuration dictionary.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r') as file:
            config = yaml.safe_load(file)

        return config

    def get_config(self):
        """
        Get the loaded configuration.

        Returns:
            dict: Configuration dictionary.
        """
        return self.config