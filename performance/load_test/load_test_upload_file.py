from locust import HttpUser, task, between
from helpers.config_load import ConfigLoader
from helpers.helpers import update_file_with_random_size
# 
def config():
    """
    Load configuration for the locust test.
    
    Returns:
        dict: Configuration dictionary with user credentials and base URL.
    """
    config_loader = ConfigLoader("test")
    return config_loader.get_config()

class FileCloudUser(HttpUser):
    wait_time = between(1, 5)
    host =config()['base_url']

    def on_start(self):
        """Login and store session cookies, load config."""
        self.client.post("/core/loginguest", data={
            "userid": config()['userid'],
            "password": config()['password']
        })

    @task
    def upload_file(self):
        """Simulate file upload with random sizes"""
        file_path = 'static_data/load_test/random_file.bin'
        update_file_with_random_size(file_path, min_size=1, max_size=10)
        files = {'file': (open(file_path, 'rb'))}
        self.client.post("/core/upload", files=files, data={
            "appname": "explorer",
            "path": "/diogoaugustodourado",
            "offset": 0
        })
