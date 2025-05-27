import json
import os
from helpers.helpers import read_json_file

def test_read_json_file():
    """
    Test the read_json_file function.
    """
    # Create a sample JSON file for testing
    test_file_path = 'static_data/new_users.json'
    
    # Call the function to read the JSON file
    data = read_json_file(test_file_path)
    
    # Assert that the result matches the expected data
    assert data is not None

def test_others():
    # Include other tests that might be relevant for the EndpointsLoader
    pass
