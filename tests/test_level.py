"""
test_level: tests for realtime_gtfs/level.py
"""

import pytest

from realtime_gtfs.models import Level
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError

MINIMAL_LEVEL_DICT = {
    "level_id": "Ground",
    "level_index": "0"
}

FULL_LEVEL_DICT = {
    "level_id": "Roof",
    "level_index": "14",
    "level_name": "The Roof"
}

MINIMAL_LEVEL = Level.from_dict(MINIMAL_LEVEL_DICT)
FULL_LEVEL = Level.from_dict(FULL_LEVEL_DICT)

def test_level_happyflow_minimal():
    """
    test_level_happyflow_minimal: minimal, correct example
    """
    level = Level.from_gtfs(MINIMAL_LEVEL_DICT.keys(), MINIMAL_LEVEL_DICT.values())
    assert level == MINIMAL_LEVEL

def test_level_happyflow_full():
    """
    test_level_happyflow_full: full, correct example
    """
    level = Level.from_gtfs(FULL_LEVEL_DICT.keys(), FULL_LEVEL_DICT.values())
    assert level == FULL_LEVEL

def test_missing_key():
    """
    test_missing_key: check if it errors if a required key is missing
    """
    temp_dict = MINIMAL_LEVEL_DICT.copy()
    del temp_dict["level_id"]
    with pytest.raises(MissingKeyError):
        Level.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_LEVEL_DICT.copy()
    del temp_dict["level_index"]
    with pytest.raises(MissingKeyError):
        Level.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_invalid_key():
    """
    test_invalid_key: test if it errors if an invalid key is passed
    """
    temp_dict = MINIMAL_LEVEL_DICT.copy()
    temp_dict["level_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        Level.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_representation():
    """
    test_representation: check if __str__ and __repr__ are defined
    """
    assert str(MINIMAL_LEVEL) != ""
    assert repr(MINIMAL_LEVEL) != ""

def test_empty_value():
    """
    test_empty_value: test if it doesn't overwrite values with empty string
    """
    temp_dict = MINIMAL_LEVEL_DICT.copy()
    temp_dict["level_index"] = ""
    with pytest.raises(MissingKeyError):
        Level.from_gtfs(temp_dict.keys(), temp_dict.values())

# pylint: disable=comparison-with-itself
def test_equal():
    """
    test_equal: check if __eq__ functions
    """
    assert MINIMAL_LEVEL == MINIMAL_LEVEL
    assert MINIMAL_LEVEL != FULL_LEVEL
    assert FULL_LEVEL != MINIMAL_LEVEL
    assert FULL_LEVEL == FULL_LEVEL
    assert MINIMAL_LEVEL != "MINIMAL_LEVEL"
