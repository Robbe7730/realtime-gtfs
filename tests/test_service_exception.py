"""
test_service_exception.py: tests for realtime_gtfs/service_exception.py
"""

import pytest

from realtime_gtfs.models import ServiceException
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError, InvalidValueError

SERVICE_EXCEPTION_DICT = {
    "service_id": "123",
    "date": "20190117",
    "exception_type": "1"
}

SERVICE_EXCEPTION = ServiceException.from_dict(SERVICE_EXCEPTION_DICT)


def test_service_exception_happyflow():
    """
    test_service_exception_happyflow: correct example
    """
    service_exception = ServiceException.from_gtfs(SERVICE_EXCEPTION_DICT.keys(),
                                                   SERVICE_EXCEPTION_DICT.values())
    assert service_exception == SERVICE_EXCEPTION


def test_missing_key():
    """
    test_missing_key: check if it errors if a required key is missing
    """
    temp_dict = SERVICE_EXCEPTION_DICT.copy()
    del temp_dict["service_id"]
    with pytest.raises(MissingKeyError):
        ServiceException.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_EXCEPTION_DICT.copy()
    del temp_dict["date"]
    with pytest.raises(MissingKeyError):
        ServiceException.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_EXCEPTION_DICT.copy()
    del temp_dict["exception_type"]
    with pytest.raises(MissingKeyError):
        ServiceException.from_gtfs(temp_dict.keys(), temp_dict.values())


def test_invalid_values():
    """
    test_invalid_values: test for values out of range, invalid enums, ...
    """
    temp_dict = SERVICE_EXCEPTION_DICT.copy()
    temp_dict["exception_type"] = "-1"
    with pytest.raises(InvalidValueError):
        ServiceException.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict["exception_type"] = "0"
    with pytest.raises(InvalidValueError):
        ServiceException.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict["exception_type"] = "3"
    with pytest.raises(InvalidValueError):
        ServiceException.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_invalid_key():
    """
    test_invalid_key: test if it errors if an invalid key is passed
    """
    temp_dict = SERVICE_EXCEPTION_DICT.copy()
    temp_dict["service_exception_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        ServiceException.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_empty_value():
    """
    test_empty_value: test if it doesn't overwrite values with empty string
    """
    temp_dict = SERVICE_EXCEPTION_DICT.copy()
    temp_dict["exception_type"] = ""
    with pytest.raises(MissingKeyError):
        ServiceException.from_gtfs(temp_dict.keys(), temp_dict.values())


def test_representation():
    """
    test_representation: check if __str__ and __repr__ are defined
    """
    assert str(SERVICE_EXCEPTION) != ""
    assert repr(SERVICE_EXCEPTION) != ""

# pylint: disable=comparison-with-itself
def test_equal():
    """
    test_equal: check if __eq__ functions
    """
    assert SERVICE_EXCEPTION != "SERVICE_EXCEPTION"
    assert SERVICE_EXCEPTION == SERVICE_EXCEPTION

    temp_dict = SERVICE_EXCEPTION_DICT.copy()
    temp_dict["exception_type"] = 2
    temp_service_exception = ServiceException.from_dict(temp_dict)

    assert temp_service_exception != SERVICE_EXCEPTION
