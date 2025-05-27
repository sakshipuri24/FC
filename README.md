# filecloud-mvp

A Python-based framework for interacting with FileCloud APIs, supporting user, group, and file management, as well as automated testing and scripting.

## Project Structure
```
filecloud-mvp/
│
├── helpers/ # Utility modules for config, endpoints, and parsing
│ ├── config_load.py
│ ├── endpoints_load.py
│ └── helpers.py
│
├── services/ # Service classes for API interaction
│ ├── base_service.py
│ ├── admin/
│ │ ├──── user.py
│ │ ├──── group.py
│ │ └──── others ...
│ └── guest/
│ └──── login.py
│ └──── others ...
├── scripts/ # Automation scripts
│ └── load_user_by_json_list.py # Example: bulk user/group creation from JSON
│
├── static_data/ # Static files for tests
│ └── new_users.json
│
├── tests/ # Pytest-based test suites
│ ├── admin/
│ │ ├── test_user.py
│ │ ├── test_group.py
│ │ └── conftest.py
│ ├── guest/
│ │ └── test_file_workflow.py
│ └── helpers/
│ └── test_helpers.py
│
├── .vscode/ # VS Code settings and launch configs
│ └── launch.json
│
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Dependencies

- Python >= 3.8
- pip (Python package manager)

---

## Pre-setup

1. Create a virtual environment:
    ```sh
    python -m venv .venv
    ```

2. Activate the virtual environment:
    - **Windows:**
      ```sh
      .venv\Scripts\activate
      ```
    - **Linux/Mac:**
      ```sh
      source .venv/bin/activate
      ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

---

## Pre-setup - CONFIG
Configure your environment:

Option 1:
Create a test.yaml file in the config folder, using the same structure as prod.yaml. Be sure to include your userid and password.

Option 2:
- To run tests and scripts with production settings:
    - Edit prod.yaml and fill in your userid and password.
    - When running, specify the environment with --env=prod (the default is --env=test).
    - If you are running a script that uses ConfigLoader, update the line config_loader = ConfigLoader("test") to config_loader = ConfigLoader("prod") (or use your desired config file name).

## Running Tests

- To run all tests:
    ```sh
    pytest --env='test'
    ```

- To run tests in a specific folder (e.g., admin):
    ```sh
    pytest tests/admin --env=test
    ```

---

## Running Scripts

- To run the user/group loader script:(Windows - PowerShell)
    ```sh
    python -m scripts.load_user_by_json_list
    ```
    or 
    ```sh
    $env:PYTHONPATH = (Get-Location)
    python scripts/load_user_by_json_list.py
    ```

- To run the user/group loader script: (Linux/Mac)
    ```sh
    python -m scripts.load_user_by_json_list
    ```
    or
    ```sh
    export PYTHONPATH=$(pwd)
    python scripts/load_user_by_json_list.py
    ```

---


# Load test - Check the Upload API

- To run the load test:(Windows - PowerShell)
```
locust -f .\performance\load_test\load_test_upload_file.py --users 1000 --spawn-rate 20 --run-time 30m --csv=filecloud_load
```

## Notes

- Update [new_users.json](http://_vscodecontentref_/3) with your user/group data for bulk operations.
- Adjust configuration files in [helpers](http://_vscodecontentref_/4) as needed for your environment.
- VS Code users can use [launch.json](http://_vscodecontentref_/5) for debugging and running scripts.

---
