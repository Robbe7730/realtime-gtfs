"""
test_frequency.py: tests for realtime_gtfs/frequency.py
"""

import pytest

from realtime_gtfs.models import Frequency
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError, InvalidValueError

MINIMAL_FREQUENCY_DICT = {
    "trip_id": "123",
    "start_time": "9:00:00",
    "end_time": "10:00:00",
    "headway_secs": "3600"
}

FULL_FREQUENCY_DICT = {
    "trip_id": "123",
    "start_time": "9:00:00",
    "end_time": "10:00:00",
    "headway_secs": "3600",
    "exact_times": "1"
}

MINIMAL_FREQUENCY = Frequency.from_dict(MINIMAL_FREQUENCY_DICT)
FULL_FREQUENCY = Frequency.from_dict(FULL_FREQUENCY_DICT)

def test_frequency_happyflow_minimal():
    """
    test_frequency_happyflow_minimal: minimal, correct example
    """
    frequency = Frequency.from_gtfs(MINIMAL_FREQUENCY_DICT.keys(), MINIMAL_FREQUENCY_DICT.values())
    assert frequency == MINIMAL_FREQUENCY

def test_frequency_happyflow_full():
    """
    test_frequency_happyflow_full: full, correct example
    """
    frequency = Frequency.from_gtfs(FULL_FREQUENCY_DICT.keys(), FULL_FREQUENCY_DICT.values())
    assert frequency == FULL_FREQUENCY

def test_missing_key():
    """
    test_missing_key: check if it errors if a required key is missing
    """
    temp_dict = FULL_FREQUENCY_DICT.copy()
    del temp_dict["trip_id"]
    with pytest.raises(MissingKeyError):
        Frequency.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_FREQUENCY_DICT.copy()
    del temp_dict["start_time"]
    with pytest.raises(MissingKeyError):
        Frequency.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_FREQUENCY_DICT.copy()
    del temp_dict["end_time"]
    with pytest.raises(MissingKeyError):
        Frequency.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_FREQUENCY_DICT.copy()
    del temp_dict["headway_secs"]
    with pytest.raises(MissingKeyError):
        Frequency.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_invalid_values():
    """
    test_invalid_values: test for values out of range, invalid enums, ...
    """
    # TODO: test trip_id, start_time and end_time
    temp_dict = FULL_FREQUENCY_DICT.copy()
    temp_dict["headway_secs"] = "-1"
    with pytest.raises(InvalidValueError):
        Frequency.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_FREQUENCY_DICT.copy()
    temp_dict["exact_times"] = "-1"
    with pytest.raises(InvalidValueError):
        Frequency.from_gtfs(temp_dict.keys(), temp_dict.values())
    temp_dict["exact_times"] = "2"
    with pytest.raises(InvalidValueError):
        Frequency.from_gtfs(temp_dict.keys(), temp_dict.values())


def test_invalid_key():
    """
    test_invalid_key: test if it errors if an invalid key is passed
    """
    temp_dict = MINIMAL_FREQUENCY_DICT.copy()
    temp_dict["frequency_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        Frequency.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_representation():
    """
    test_representation: check if __str__ and __repr__ are defined
    """
    assert str(MINIMAL_FREQUENCY) != ""
    assert repr(MINIMAL_FREQUENCY) != ""

def test_empty_value():
    """
    test_empty_value: test if it doesn't overwrite values with empty string
    """
    temp_dict = MINIMAL_FREQUENCY_DICT.copy()
    temp_dict["trip_id"] = ""
    with pytest.raises(MissingKeyError):
        Frequency.from_gtfs(temp_dict.keys(), temp_dict.values())

# pylint: disable=comparison-with-itself
def test_equal():
    """
    test_equal: check if __eq__ functions
    """
    assert MINIMAL_FREQUENCY == MINIMAL_FREQUENCY
    assert MINIMAL_FREQUENCY != FULL_FREQUENCY
    assert FULL_FREQUENCY != MINIMAL_FREQUENCY
    assert FULL_FREQUENCY == FULL_FREQUENCY
    assert MINIMAL_FREQUENCY != "MINIMAL_FREQUENCY"

    temp_dict = MINIMAL_FREQUENCY_DICT.copy()
    temp_dict["end_time"] = "5:01:01"
    temp_frequency = Frequency.from_dict(temp_dict)

    assert temp_frequency != MINIMAL_FREQUENCY
