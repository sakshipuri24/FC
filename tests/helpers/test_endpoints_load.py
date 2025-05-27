from helpers.endpoints_load import EndpointsLoader


def test_endpoints_loader_helper():
    """
    Test that the EndpointsLoader correctly loads endpoints for the given user type.

    Asserts:
        - The returned endpoints dictionary is not None.
        - The 'login' key exists in the endpoints dictionary.
    """
    endpoints_loader = EndpointsLoader('admin')
    endpoints = endpoints_loader.get_endpoints()
    assert endpoints is not None
    assert "login" in endpoints

def test_others():
    # Include other tests that might be relevant for the EndpointsLoader
    pass
