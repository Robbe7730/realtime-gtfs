"""
test_stop.py: tests for realtime_gtfs/stop.py
"""

import pytz
import pytest

from realtime_gtfs.stop import Stop
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError

MINIMAL_STOP_DICT = {
    "stop_id": "minimal_stop",
    "stop_name": "Comma",
    "stop_lat": "1.234",
    "stop_lon": "5.678"
}

FULL_STOP_DICT = {
    "stop_id": "full_stop",
    "stop_name": "Period",
    "stop_lat": "1.234",
    "stop_lon": "5.678",
    "stop_code": ".",
    "stop_desc": "A nice stop for taking a break",
    "stop_url": "https://period.com/",
    "location_type": "0",
    "stop_timezone": "Europe/Brussels",
    "wheelchair_boarding": "1",
    "platform_code": ".1",
    "zone_id": "123",
    "parent_station": "123",
    "level_id": "123"
}

MINIMAL_STOP = Stop.from_dict(MINIMAL_STOP_DICT)
FULL_STOP = Stop.from_dict(FULL_STOP_DICT)

def test_stop_happyflow_minimal():
    """
    test_stop_happyflow_minimal: minimal, correct example
    """
    stop = Stop.from_gtfs(MINIMAL_STOP_DICT.keys(), MINIMAL_STOP_DICT.values())
    assert stop == MINIMAL_STOP

def test_stop_happyflow_full():
    """
    test_stop_happyflow_full: full, correct example
    """
    stop = Stop.from_gtfs(FULL_STOP_DICT.keys(), FULL_STOP_DICT.values())
    assert stop == FULL_STOP

def test_invalid_timezone():
    """
    test_invalid_timezone: check if it raises UnknownTimeZoneError when given an invalid timezone
    """
    temp_dict = MINIMAL_STOP_DICT.copy()
    temp_dict["stop_timezone"] = "MiddleEarth/Shire"
    with pytest.raises(pytz.exceptions.UnknownTimeZoneError):
        Stop.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_missing_key():
    """
    test_missing_key: check if it errors if a required key is missing
    """
    temp_dict = MINIMAL_STOP_DICT.copy()
    del temp_dict["stop_id"]
    with pytest.raises(MissingKeyError):
        Stop.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_DICT.copy()
    del temp_dict["stop_name"]
    with pytest.raises(MissingKeyError):
        Stop.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_DICT.copy()
    del temp_dict["stop_lat"]
    with pytest.raises(MissingKeyError):
        Stop.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_DICT.copy()
    del temp_dict["stop_lon"]
    with pytest.raises(MissingKeyError):
        Stop.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_DICT.copy()
    temp_dict["location_type"] = 2
    with pytest.raises(MissingKeyError):
        Stop.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_DICT.copy()
    temp_dict["location_type"] = 1
    temp_dict["parent_station"] = 123
    with pytest.raises(InvalidKeyError):
        Stop.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_invalid_values():
    """
    test_invalid_values: test for values out of range, invalid enums, ...
    """
    temp_dict = MINIMAL_STOP_DICT.copy()
    temp_dict["stop_lat"] = "-100"
    with pytest.raises(InvalidKeyError):
        Stop.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_DICT.copy()
    temp_dict["stop_lon"] = "-200"
    with pytest.raises(InvalidKeyError):
        Stop.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_DICT.copy()
    temp_dict["location_type"] = "-1"
    with pytest.raises(InvalidKeyError):
        Stop.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_DICT.copy()
    temp_dict["location_type"] = "5"
    temp_dict["parent_station"] = "456"
    with pytest.raises(InvalidKeyError):
        Stop.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_DICT.copy()
    temp_dict["wheelchair_boarding"] = "-1"
    with pytest.raises(InvalidKeyError):
        Stop.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_DICT.copy()
    temp_dict["wheelchair_boarding"] = "3"
    with pytest.raises(InvalidKeyError):
        Stop.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_default():
    """
    test_default: check for correct default values (wheelchair_boarding and location_type)
    """
    assert MINIMAL_STOP.wheelchair_boarding == 0
    assert MINIMAL_STOP.location_type == 0

def test_invalid_key():
    """
    test_invalid_key: test if it errors if an invalid key is passed
    """
    temp_dict = MINIMAL_STOP_DICT.copy()
    temp_dict["stop_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        Stop.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_representation():
    """
    test_representation: check if __str__ and __repr__ are defined
    """
    assert str(MINIMAL_STOP) != ""
    assert repr(MINIMAL_STOP) != ""

# pylint: disable=comparison-with-itself
def test_equal():
    """
    test_equal: check if __eq__ functions
    """
    assert MINIMAL_STOP == MINIMAL_STOP
    assert MINIMAL_STOP != FULL_STOP
    assert FULL_STOP != MINIMAL_STOP
    assert FULL_STOP == FULL_STOP
    assert MINIMAL_STOP != "MINIMAL_STOP"

    temp_dict = MINIMAL_STOP_DICT.copy()
    temp_dict["platform_code"] = 2
    temp_stop = Stop.from_dict(temp_dict)

    assert temp_stop != MINIMAL_STOP
