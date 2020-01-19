"""
test_service.py: tests for realtime_gtfs/service.py
"""

import pytest

from realtime_gtfs.models import Service
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError, InvalidValueError

SERVICE_DICT = {
    "service_id": "123",
    "monday": "1",
    "tuesday": "1",
    "wednesday": "1",
    "thursday": "1",
    "friday": "1",
    "saturday": "1",
    "sunday": "1",
    "start_date": "19990117",
    "end_date": "20200117"

}

SERVICE = Service.from_dict(SERVICE_DICT)


def test_service_happyflow():
    """
    test_service_happyflow: correct example
    """
    service = Service.from_gtfs(SERVICE_DICT.keys(), SERVICE_DICT.values())
    assert service == SERVICE


def test_missing_key():
    """
    test_missing_key: check if it errors if a required key is missing
    """
    temp_dict = SERVICE_DICT.copy()
    del temp_dict["service_id"]
    with pytest.raises(MissingKeyError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_DICT.copy()
    del temp_dict["monday"]
    with pytest.raises(MissingKeyError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_DICT.copy()
    del temp_dict["tuesday"]
    with pytest.raises(MissingKeyError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_DICT.copy()
    del temp_dict["wednesday"]
    with pytest.raises(MissingKeyError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_DICT.copy()
    del temp_dict["thursday"]
    with pytest.raises(MissingKeyError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_DICT.copy()
    del temp_dict["friday"]
    with pytest.raises(MissingKeyError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_DICT.copy()
    del temp_dict["saturday"]
    with pytest.raises(MissingKeyError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_DICT.copy()
    del temp_dict["sunday"]
    with pytest.raises(MissingKeyError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_DICT.copy()
    del temp_dict["start_date"]
    with pytest.raises(MissingKeyError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_DICT.copy()
    del temp_dict["end_date"]
    with pytest.raises(MissingKeyError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())


def test_invalid_values():
    """
    test_invalid_values: test for values out of range, invalid enums, ...
    """
    temp_dict = SERVICE_DICT.copy()
    temp_dict["monday"] = "-1"
    with pytest.raises(InvalidValueError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict["monday"] = "2"
    with pytest.raises(InvalidValueError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_DICT.copy()
    temp_dict["tuesday"] = "-1"
    with pytest.raises(InvalidValueError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict["tuesday"] = "2"
    with pytest.raises(InvalidValueError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_DICT.copy()
    temp_dict["wednesday"] = "-1"
    with pytest.raises(InvalidValueError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict["wednesday"] = "2"
    with pytest.raises(InvalidValueError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_DICT.copy()
    temp_dict["thursday"] = "-1"
    with pytest.raises(InvalidValueError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict["thursday"] = "2"
    with pytest.raises(InvalidValueError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_DICT.copy()
    temp_dict["friday"] = "-1"
    with pytest.raises(InvalidValueError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict["friday"] = "2"
    with pytest.raises(InvalidValueError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_DICT.copy()
    temp_dict["saturday"] = "-1"
    with pytest.raises(InvalidValueError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict["saturday"] = "2"
    with pytest.raises(InvalidValueError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = SERVICE_DICT.copy()
    temp_dict["sunday"] = "-1"
    with pytest.raises(InvalidValueError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict["sunday"] = "2"
    with pytest.raises(InvalidValueError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())


def test_invalid_key():
    """
    test_invalid_key: test if it errors if an invalid key is passed
    """
    temp_dict = SERVICE_DICT.copy()
    temp_dict["service_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_empty_value():
    """
    test_empty_value: test if it doesn't overwrite values with empty string
    """
    temp_dict = SERVICE_DICT.copy()
    temp_dict["service_id"] = ""
    with pytest.raises(MissingKeyError):
        Service.from_gtfs(temp_dict.keys(), temp_dict.values())


def test_representation():
    """
    test_representation: check if __str__ and __repr__ are defined
    """
    assert str(SERVICE) != ""
    assert repr(SERVICE) != ""

# pylint: disable=comparison-with-itself
def test_equal():
    """
    test_equal: check if __eq__ functions
    """
    assert SERVICE != "SERVICE"
    assert SERVICE == SERVICE

    temp_dict = SERVICE_DICT.copy()
    temp_dict["friday"] = 0
    temp_service = Service.from_dict(temp_dict)

    assert temp_service != SERVICE
