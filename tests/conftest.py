import pytest
import requests

from helpers.config_load import ConfigLoader

def pytest_addoption(parser):
    """
    Add a custom command-line option '--env' to pytest for selecting the environment.

    Args:
        parser: The pytest parser object.

    This allows running tests with:
        pytest --env=prod
    """
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="Environment to run tests against (e.g. test, dev, sit, uat and prod)"
    )

@pytest.fixture(scope="session")
def config(request):
    """
    Session-scoped fixture to load configuration based on the selected environment.

    Args:
        request: The pytest request object.

    Returns:
        dict: The configuration dictionary for the selected environment.
    """
    env = request.config.getoption("--env")
    config_loader = ConfigLoader(env)
    config = config_loader.get_config()
    return config