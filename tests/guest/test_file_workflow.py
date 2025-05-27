from services.guest.file import File
from services.guest.versioning import Versioning
import logging
from helpers.helpers import parse_xml_response

remote_fileclound_path = "/diogoaugustodourado"
file_name = "docx_for_test_file.docx"
full_remote_path = f"{remote_fileclound_path}/{file_name}"
file_path_to_upload = "static_data/v{version}/docx_for_test_file.docx"

def file_exists(config_and_login_session):
    """
    Check that a specific file exists in FileCloud.
    """
    config, session = config_and_login_session
    file = File(session=session, user_type=config['user_type'], base_url=config["base_url"])
    file_path = "/diogoaugustodourado/FileCloud Overview.pdf"
    response = file.file_exists(path=file_path)
    dict_response = parse_xml_response(response.text)
    assert dict_response['commands']['command']['result'] == '1'

def upload_file(file_session, remote_path, file_path):
    """
    Upload a file to FileCloud and assert success.
    """
    file_to_upload = {'file': (open(file_path, 'rb'))}
    params = {
        "appname": "explorer",
        "path": remote_path,
        "offset": 0
    }
    response = file_session.upload_file(params=params, files=file_to_upload)
    assert response.status_code == 200, "Failed to upload file"

def delete_file(file_session, remote_path, file_name):
    """
    Delete a file from FileCloud and assert success.
    """
    response = file_session.delete_file(path=remote_path, name=file_name)
    dict_response = parse_xml_response(response.text)
    assert response.status_code == 200, "Failed to delete file"
    assert dict_response['commands']['command']['result'] == '1', "Failed to delete file"

def exists_file(file_session, full_remote_path):
    """
    Check if a file exists in FileCloud.
    """
    response = file_session.file_exists(path=full_remote_path)
    dict_response = parse_xml_response(response.text)
    assert response.status_code == 200, "Failed to check if file exists"
    assert 'result' in response.text, "Failed to check if file exists"
    return dict_response['commands']['command']['result'] == '1'

def asset_file_properties(entry, expected_name, expected_path, expected_type, expected_size, expected_dirpath, expected_extension):
    """
    Assert file properties match expected values.
    """
    assert entry['name'] == expected_name
    assert entry['path'] == expected_path
    assert entry['type'] == expected_type
    assert entry['size'] == expected_size
    assert entry['dirpath'] == expected_dirpath
    assert entry['ext'] == expected_extension

def test_file_workflow(config_and_login_session):
    """
    End-to-end test: upload, update, and version a file in FileCloud.
    """
    config, session = config_and_login_session
    file_session = File(session=session, user_type=config['user_type'], base_url=config["base_url"])
    versioning_session = Versioning(session=session, user_type=config['user_type'], base_url=config["base_url"])

    # Remove file if it exists
    if exists_file(file_session, full_remote_path):
        delete_file(file_session, remote_fileclound_path, file_name)
    else:
        logging.info(f"File {full_remote_path} does not exist.")

    # Upload version 1
    upload_file(file_session, remote_fileclound_path, file_path_to_upload.format(version='1'))
    assert exists_file(file_session, full_remote_path)

    # Get file info after first upload
    response = file_session.get_file_info(params={"file": full_remote_path, "includeextrafields": "1", "includelockinfo": "1"})
    dict_response_v1 = parse_xml_response(response.text)
    assert response.status_code == 200, "Failed to get file info"
    dict_file_info_v1 = dict_response_v1['fileinfo']['entry']
    asset_file_properties(
        entry=dict_file_info_v1,
        expected_name=file_name,
        expected_path=full_remote_path,
        expected_type='file',
        expected_size='0 B',
        expected_dirpath=remote_fileclound_path,
        expected_extension='docx'
    )

    # Upload version 2 (update)
    upload_file(file_session, remote_fileclound_path, file_path_to_upload.format(version='2'))
    assert exists_file(file_session, full_remote_path)

    # Get file info after update
    response = file_session.get_file_info(params={"file": full_remote_path, "includeextrafields": "1", "includelockinfo": "1"})
    dict_response_v2 = parse_xml_response(response.text)
    dict_file_info_v2 = dict_response_v2['fileinfo']['entry']
    asset_file_properties(
        entry=dict_file_info_v2,
        expected_name=file_name,
        expected_path=full_remote_path,
        expected_type='file',
        expected_size='4 KB',
        expected_dirpath=remote_fileclound_path,
        expected_extension='docx'
    )

    # Ensure the file was updated
    v1_epoch = int(dict_file_info_v1['modifiedepoch'])
    v2_epoch = int(dict_file_info_v2['modifiedepoch'])
    assert v1_epoch < v2_epoch, "File was not updated: v1 is not older than v2"

    # Check file versions
    response_get_versions = versioning_session.get_versions(params={"filepath": remote_fileclound_path, "filename": file_name})
    dict_response_get_versions = parse_xml_response(response_get_versions.text)
    dict_versions_info = dict_response_get_versions['versions']['version']
    assert response_get_versions.status_code == 200, "Failed to get file versions"
    assert int(dict_response_get_versions['versions']['meta']['total']) >= 2, "File versions count does not match"

    # Version 1 validation (older version is second in the list)
    v1_version = dict_versions_info[1]
    assert v1_version['versionnumber'] == 'Version 1'
    assert v1_version['size'] == dict_file_info_v1['size']
    assert v1_version['filename'] == dict_file_info_v1['name']
    assert v1_version['createdby'] == dict_file_info_v1.get('createdby', 'diogoaugustodourado')

    # Version 2 validation (newest version is first)
    v2_version = dict_versions_info[0]
    assert v2_version['versionnumber'] == 'Version 2'
    assert v2_version['size'] == dict_file_info_v2['size']

    # Cross-version checks
    assert v1_version['createdby'] == v2_version['createdby']
    assert v1_version['date'] < v2_version['date']