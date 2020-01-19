"""
test_trip.py: tests for realtime_gtfs/trip.py
"""

import pytest

from realtime_gtfs.models import Trip
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError, InvalidValueError

MINIMAL_TRIP_DICT = {
    "route_id": "123",
    "service_id": "123",
    "trip_id": "bad_trip"
}

FULL_TRIP_DICT = {
    "route_id": "123",
    "service_id": "123",
    "trip_id": "good_trip",
    "trip_headsign": "Good Trip",
    "trip_short_name": "good trip",
    "direction_id": "1",
    "block_id": "123",
    "shape_id": "123",
    "wheelchair_accessible": "1",
    "bikes_allowed": "2"
}

MINIMAL_TRIP = Trip.from_dict(MINIMAL_TRIP_DICT)
FULL_TRIP = Trip.from_dict(FULL_TRIP_DICT)

def test_trip_happyflow_minimal():
    """
    test_trip_happyflow_minimal: minimal, correct example
    """
    trip = Trip.from_gtfs(MINIMAL_TRIP_DICT.keys(), MINIMAL_TRIP_DICT.values())
    assert trip == MINIMAL_TRIP

def test_trip_happyflow_full():
    """
    test_trip_happyflow_full: full, correct example
    """
    trip = Trip.from_gtfs(FULL_TRIP_DICT.keys(), FULL_TRIP_DICT.values())
    assert trip == FULL_TRIP

def test_missing_key():
    """
    test_missing_key: check if it errors if a required key is missing
    """
    temp_dict = FULL_TRIP_DICT.copy()
    del temp_dict["route_id"]
    with pytest.raises(MissingKeyError):
        Trip.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_TRIP_DICT.copy()
    del temp_dict["service_id"]
    with pytest.raises(MissingKeyError):
        Trip.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_TRIP_DICT.copy()
    del temp_dict["trip_id"]
    with pytest.raises(MissingKeyError):
        Trip.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_invalid_values():
    """
    test_invalid_values: test for values out of range, invalid enums, ...
    """
    temp_dict = MINIMAL_TRIP_DICT.copy()
    temp_dict["direction_id"] = "-1"
    with pytest.raises(InvalidValueError):
        Trip.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_TRIP_DICT.copy()
    temp_dict["direction_id"] = "2"
    with pytest.raises(InvalidValueError):
        Trip.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_TRIP_DICT.copy()
    temp_dict["wheelchair_accessible"] = "-1"
    with pytest.raises(InvalidValueError):
        Trip.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_TRIP_DICT.copy()
    temp_dict["wheelchair_accessible"] = "3"
    with pytest.raises(InvalidValueError):
        Trip.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_TRIP_DICT.copy()
    temp_dict["bikes_allowed"] = "-1"
    with pytest.raises(InvalidValueError):
        Trip.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_TRIP_DICT.copy()
    temp_dict["bikes_allowed"] = "3"
    with pytest.raises(InvalidValueError):
        Trip.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_default():
    """
    test_default: check for correct default values (wheelchair_boarding and location_type)
    """
    assert MINIMAL_TRIP.direction_id == 0
    assert MINIMAL_TRIP.wheelchair_accessible == 0
    assert MINIMAL_TRIP.bikes_allowed == 0

def test_invalid_key():
    """
    test_invalid_key: test if it errors if an invalid key is passed
    """
    temp_dict = MINIMAL_TRIP_DICT.copy()
    temp_dict["trip_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        Trip.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_representation():
    """
    test_representation: check if __str__ and __repr__ are defined
    """
    assert str(MINIMAL_TRIP) != ""
    assert repr(MINIMAL_TRIP) != ""

def test_empty_value():
    """
    test_empty_value: test if it doesn't overwrite values with empty string
    """
    temp_dict = MINIMAL_TRIP_DICT.copy()
    temp_dict["route_id"] = ""
    with pytest.raises(MissingKeyError):
        Trip.from_gtfs(temp_dict.keys(), temp_dict.values())

# pylint: disable=comparison-with-itself
def test_equal():
    """
    test_equal: check if __eq__ functions
    """
    assert MINIMAL_TRIP == MINIMAL_TRIP
    assert MINIMAL_TRIP != FULL_TRIP
    assert FULL_TRIP != MINIMAL_TRIP
    assert FULL_TRIP == FULL_TRIP
    assert MINIMAL_TRIP != "MINIMAL_TRIP"

    temp_dict = FULL_TRIP_DICT.copy()
    temp_dict["direction_id"] = "0"
    temp_trip = Trip.from_dict(temp_dict)

    assert temp_trip != FULL_TRIP
