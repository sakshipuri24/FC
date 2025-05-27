from services.admin.group import Group
from services.admin.user import User
from services.admin.login import Login
from helpers.helpers import read_json_file, parse_xml_response
from helpers.config_load import ConfigLoader
import logging
import requests
import copy

def get_user_id(session, user_data):
    """
    Retrieve the user ID (username) from the user service.

    Args:
        session: The requests.Session object.
        user_data: Dictionary with user information.

    Returns:
        str or None: The username if found, else None.
    """
    user_service = User(session, config['user_type'], config["base_url"])
    user_service_response = user_service.get_user(user_data['username'])
    if user_service_response.status_code == 200:
        user_id = parse_xml_response(user_service_response.text)['users']['user']['username']
        return user_id
    else:
        logging.warning(f"User {user_data['username']} not found, skipping test.\n"
                        f"user info: {user_data}")
        return None

def get_group_id(session, group_name):
    """
    Retrieve the group ID from the group service.

    Args:
        session: The requests.Session object.
        group_name: Name of the group.

    Returns:
        str or None: The group ID if found, else None.
    """
    group_service = Group(session, config['user_type'], config['base_url'])
    group_service_response = group_service.get_group_by_name(group_name)
    if group_service_response.status_code == 200:
        group_id = parse_xml_response(group_service_response.text)['groups']['group']['groupid']
        return group_id
    else:
        logging.warning(f"Group {group_name} not found, skipping test.\n"
                        f"group name: {group_name}")
        return None

def create_groups(session, config, group_list):
    """
    Create groups in the system based on a JSON file.

    Args:
        session: The requests.Session object.
        config: Configuration dictionary.
        group_list: List of group names to create.
    """
    group_service = Group(session, config['user_type'], config['base_url'])
    response = group_service.get_groups()
    list_of_the_groups_to_be_created = []
    for group in group_list:
        if f'<groupname>{group}</groupname>' not in response.text:
            list_of_the_groups_to_be_created.append(group)
    for group in list_of_the_groups_to_be_created:
        response = group_service.add_new_group(group)
        if response.status_code == 200:
            logging.info(f"Group {group} created successfully.")
        else:
            logging.warning(f"Failed to create group {group}. Status code: {response.status_code}, status text: {response.text}")

def add_users(session, config, user_list):
    """
    Add users to the system based on a JSON file.

    Args:
        session: The requests.Session object.
        config: Configuration dictionary.
        user_list: List of user dictionaries.
    """
    user_list_copy = copy.deepcopy(user_list)
    user_service = User(session=session, user_type=config['user_type'], base_url=config["base_url"])
    for user_data in user_list_copy:
        user_data.pop('groups', None)
        print(f"Adding user {user_data['username']} to the system.")
        response = user_service.add_new_user(user_data=user_data)
        if response.status_code == 200:
            logging.info(f"User {user_data['username']} created successfully.")
        elif response.status_code == 400:
            xml_response = parse_xml_response(response.text)
            logging.warning(f"User not added, maybe this user is already in the sistem!\n"
                            f"User not added, because: {xml_response['commands']['command']['message']}\n"
                            f"user info: {user_data}")
        else:
            logging.warning(f"Error to add this user: {user_data}\n Response text: {response.text}, status code: {response.status_code}")

def add_members_to_the_groups(session, config, user_list):
    """
    Add users to their respective groups.

    Args:
        session: The requests.Session object.
        config: Configuration dictionary.
        user_list: List of user dictionaries (with 'groups' key).
    """
    group_service = Group(session, config['user_type'], config['base_url'])
    for user_data in user_list:
        user_name = get_user_id(session, user_data)
        for group in user_data['groups']:
            group_id = get_group_id(session, group)
            response = group_service.add_member_to_group(group_id=group_id, user_id=user_name)
            if response.status_code == 200:
                logging.info(f"User {user_data['username']} added to group {group} successfully.")
            elif response.status_code == 400:
                logging.warning(f"User is already a member of the group. username: {user_name} and groupid: {group_id}")
            else:
                logging.warning(f"Error to add this user: {user_data}\n Response text: {response.text}")

def login():
    """
    Log in as an admin user and return config and session.

    Returns:
        tuple: (config, session)
    """
    session = requests.session()
    config_loader = ConfigLoader("test")
    config = config_loader.get_config()
    config['user_type'] = "admin"
    login = Login(session, config['user_type'], config["base_url"])
    if not config["userid"] or not config["password"]:
        raise ValueError("Admin user ID and password must be set in the config file. In this case, in the config/prod.yaml file.")
    response = login.admin_login(
        username=config["userid"],
        password=config["password"],
        headers={'Accept': 'application/json'}
    )

    assert response.status_code == 200
    if not response.json()['command'][0]['result'] == 1:
        raise Exception("Login failed!")
    return config, session

if __name__ == "__main__":
    """
    Main script execution:
        - Loads users and groups from JSON.
        - Logs in as admin.
        - Creates groups.
        - Adds users.
        - Adds users to groups.
    """
    json_file_path = 'static_data/new_users.json'
    json_data = read_json_file(json_file_path)
    config, session = login()
    create_groups(session, config, group_list=json_data['groups'])
    add_users(session, config, user_list=json_data['users'])
    add_members_to_the_groups(session, config, user_list=json_data['users'])