from helpers.config_load import ConfigLoader


def test_config_load():
    """
    Test that the ConfigLoader loads the configuration for the 'test' environment.

    Asserts:
        - The base_url starts with 'https://'.
        - The userid is not None.
        - The password is not None.
    """
    config_loader = ConfigLoader("test")
    config = config_loader.get_config()
    assert config["base_url"].startswith("https://")
    assert config["userid"] is not None
    assert config["password"] is not None

def test_others():
    # Include other tests that might be relevant for the EndpointsLoader
    pass
