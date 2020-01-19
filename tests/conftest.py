"""
conftest.py: set up pytest
"""
import pytest

def pytest_addoption(parser):
    """
    pytest_addoption: add options to pytest command line arguments
    """
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )
    parser.addoption(
        "--no-integration", action="store_true", default=False, help="don't run integration tests"
    )

def pytest_configure(config):
    """
    pytest_configure: add markerz
    """
    config.addinivalue_line("markers", "slow: mark test as slow to run")
    config.addinivalue_line("markers", "integration: mark test as an integration test")

def pytest_collection_modifyitems(config, items):
    """
    pytest_configure: skip functions
    """
    if not config.getoption("--runslow"):
        skip_slow = pytest.mark.skip(reason="need --runslow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)

    if config.getoption("--no-integration"):
        skip_integration = pytest.mark.skip(reason="--no-integration is set")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)
