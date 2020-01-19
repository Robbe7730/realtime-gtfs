"""
test_stop_time.py: tests for realtime_gtfs/stop_time.py
"""

import pytest

from realtime_gtfs.models import StopTime
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError, InvalidValueError

MINIMAL_STOP_TIME_DICT = {
    "trip_id": "123",
    "arrival_time": "01:23:45",
    "stop_id": "123",
    "stop_sequence": "5"
}

FULL_STOP_TIME_DICT = {
    "trip_id": "123",
    "arrival_time": "1:23:45",
    "departure_time": "25:23:45",
    "stop_id": "123",
    "stop_sequence": "5",
    "stop_headsign": "I'm a sign",
    "pickup_type": "3",
    "drop_off_type": "2",
    "shape_dist_traveled": "5.25",
    "timepoint": "0"
}

MINIMAL_STOP_TIME = StopTime.from_dict(MINIMAL_STOP_TIME_DICT)
FULL_STOP_TIME = StopTime.from_dict(FULL_STOP_TIME_DICT)

def test_stop_time_happyflow_minimal():
    """
    test_stop_time_happyflow_minimal: minimal, correct example
    """
    stop_time = StopTime.from_gtfs(MINIMAL_STOP_TIME_DICT.keys(), MINIMAL_STOP_TIME_DICT.values())
    assert stop_time == MINIMAL_STOP_TIME

def test_stop_time_happyflow_full():
    """
    test_stop_time_happyflow_full: full, correct example
    """
    stop_time = StopTime.from_gtfs(FULL_STOP_TIME_DICT.keys(), FULL_STOP_TIME_DICT.values())
    assert stop_time == FULL_STOP_TIME

def test_missing_key():
    """
    test_missing_key: check if it errors if a required key is missing
    """
    temp_dict = FULL_STOP_TIME_DICT.copy()
    del temp_dict["trip_id"]
    with pytest.raises(MissingKeyError):
        StopTime.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_STOP_TIME_DICT.copy()
    del temp_dict["departure_time"]
    del temp_dict["arrival_time"]
    with pytest.raises(MissingKeyError):
        StopTime.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_STOP_TIME_DICT.copy()
    del temp_dict["stop_id"]
    with pytest.raises(MissingKeyError):
        StopTime.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_STOP_TIME_DICT.copy()
    del temp_dict["stop_sequence"]
    with pytest.raises(MissingKeyError):
        StopTime.from_gtfs(temp_dict.keys(), temp_dict.values())


def test_invalid_values():
    """
    test_invalid_values: test for values out of range, invalid enums, ...
    """
    # TODO: test times

    temp_dict = MINIMAL_STOP_TIME_DICT.copy()
    temp_dict["stop_sequence"] = "-1"
    with pytest.raises(InvalidValueError):
        StopTime.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_TIME_DICT.copy()
    temp_dict["pickup_type"] = "-1"
    with pytest.raises(InvalidValueError):
        StopTime.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_TIME_DICT.copy()
    temp_dict["pickup_type"] = "4"
    with pytest.raises(InvalidValueError):
        StopTime.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_TIME_DICT.copy()
    temp_dict["drop_off_type"] = "-1"
    with pytest.raises(InvalidValueError):
        StopTime.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_TIME_DICT.copy()
    temp_dict["drop_off_type"] = "4"
    with pytest.raises(InvalidValueError):
        StopTime.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_TIME_DICT.copy()
    temp_dict["shape_dist_traveled"] = "-1"
    with pytest.raises(InvalidValueError):
        StopTime.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_TIME_DICT.copy()
    temp_dict["timepoint"] = "-1"
    with pytest.raises(InvalidValueError):
        StopTime.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_STOP_TIME_DICT.copy()
    temp_dict["timepoint"] = "2"
    with pytest.raises(InvalidValueError):
        StopTime.from_gtfs(temp_dict.keys(), temp_dict.values())


def test_default():
    """
    test_default: check for correct default values (wheelchair_boarding and location_type)
    """
    assert MINIMAL_STOP_TIME.pickup_type == 0
    assert MINIMAL_STOP_TIME.drop_off_type == 0
    assert MINIMAL_STOP_TIME.timepoint == 1

def test_invalid_key():
    """
    test_invalid_key: test if it errors if an invalid key is passed
    """
    temp_dict = MINIMAL_STOP_TIME_DICT.copy()
    temp_dict["stop_time_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        StopTime.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_representation():
    """
    test_representation: check if __str__ and __repr__ are defined
    """
    assert str(MINIMAL_STOP_TIME) != ""
    assert repr(MINIMAL_STOP_TIME) != ""

# pylint: disable=comparison-with-itself
def test_equal():
    """
    test_equal: check if __eq__ functions
    """
    assert MINIMAL_STOP_TIME == MINIMAL_STOP_TIME
    assert MINIMAL_STOP_TIME != FULL_STOP_TIME
    assert FULL_STOP_TIME != MINIMAL_STOP_TIME
    assert FULL_STOP_TIME == FULL_STOP_TIME
    assert MINIMAL_STOP_TIME != "MINIMAL_STOP_TIME"

    temp_dict = MINIMAL_STOP_TIME_DICT.copy()
    temp_dict["drop_off_type"] = "1"
    temp_stop_time = StopTime.from_dict(temp_dict)

    assert temp_stop_time != MINIMAL_STOP_TIME
