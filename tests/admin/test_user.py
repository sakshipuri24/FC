from services.admin.user import User
from helpers.helpers import parse_xml_response
import logging

def test_get_user(config_and_login_session):
    """
    Test that a specific user can be retrieved from FileCloud.

    Asserts:
        - The response status code is 200.
        - The username in the response matches the expected username.
        - The email in the response matches the expected email.
    """
    config, session = config_and_login_session
    user = User(session=session, user_type=config['user_type'], base_url=config["base_url"])
    user_name = "diogoaugustodourado"
    response = user.get_user(user_name)
    dict_data = parse_xml_response(response.text)

    assert response.status_code == 200
    assert user_name == dict_data['users']['user']['username']
    assert 'diogo.augusto.dourado@gmail.com' == dict_data['users']['user']['email']

def test_add_new_user(config_and_login_session):
    """
    Test that a new user can be added to FileCloud.

    Asserts:
        - If the user does not already exist, the response status code is 200 and the result is successful.
        - If the user already exists, a warning is logged and the test is skipped.
    """
    config, session = config_and_login_session
    user = User(session=session, user_type=config['user_type'], base_url=config["base_url"])
    params = {
        "username": "John Doe",
        "displayname": "John Doe",
        "email": "john_doe@gmail.com",
        "password": "John$Doe",
        "authtype": "0",
        "status": 1
    }
    response = user.add_new_user(user_data=params)
    if 'Username already exists and is not available' in response.text:
        logging.warning("User already exists, skipping test.\n"
                        f"user info: {params}")
        pass
    else:
        assert response.status_code == 200
        assert '<result>1</result>' in response.text
        assert response.reason == "OK"