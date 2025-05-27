import pytest
import requests
from services.guest.login import Login


@pytest.fixture(scope="session")
def config_and_login_session(config):
    """
    Session-scoped fixture to log in as a guest user and provide the config and session.

    Steps:
        - Sets user_type to 'guest' in the config.
        - Logs in using the guest credentials and checks for a successful login.
        - Yields the config and session for use in tests.
        - Logs out after all tests in the session are complete.

    Asserts:
        - Login response status code is 200.
        - Login response JSON contains a successful result.
    """
    session = requests.session()
    config['user_type'] = "guest"
    login = Login(session, config['user_type'], config["base_url"])
    response = login.login(config["userid"], config["password"], headers={'Accept': 'application/json'})
    assert response.status_code == 200
    assert response.json()['command'][0]['result'] == 1

    yield config, session

    login.logout()

    
    