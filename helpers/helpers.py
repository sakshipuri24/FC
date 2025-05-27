import json
import xmltodict
import os
import random

def read_json_file(file_path):
    """
    Reads a JSON file and returns the data.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def parse_xml_response(response):
    """
    Standardize XML parsing with error handling.

    Args:
        response (str): XML response as a string.

    Returns:
        dict: Parsed XML as a dictionary.

    Raises:
        AssertionError: If the XML cannot be parsed.
    """
    try:
        return xmltodict.parse(response)
    except Exception as e:
        raise AssertionError(f"Invalid XML response: {str(e)}")

def update_file_with_random_size(file_path: str, min_size: int, max_size: int):
    """
    Overwrite the file at file_path with random bytes of the specified size.

    Args:
        file_path (str): Path to the file to update.
        size_bytes (int): Desired file size in bytes.
    """
    size_bytes = random.randint(min_size, max_size * 1024 * 1024)
    with open(file_path, "wb") as f:
        f.write(os.urandom(size_bytes))