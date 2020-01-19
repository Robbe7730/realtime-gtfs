"""
conftest.py: set up pytest
"""
import pytest

def pytest_addoption(parser):
    """
    pytest_addoption: add option to pytest command line arguments
    """
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )

def pytest_configure(config):
    """
    pytest_configure: add marker to mark slow tests
    """
    config.addinivalue_line("markers", "slow: mark test as slow to run")

def pytest_collection_modifyitems(config, items):
    """
    pytest_configure: skip slow functions
    """
    if config.getoption("--runslow"):
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
