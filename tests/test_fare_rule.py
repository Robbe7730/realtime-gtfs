"""
test_fare_rule.py: tests for realtime_gtfs/fare_rule.py
"""

import pytest

from realtime_gtfs.models import FareRule
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError

MINIMAL_FR_DICT = {
    "fare_id": "123"
}

FULL_FR_DICT = {
    "fare_id": "132",
    "route_id": "123",
    "origin_id": "123",
    "destination_id": "123",
    "contains_id": "123"
}

MINIMAL_FR = FareRule.from_dict(MINIMAL_FR_DICT)
FULL_FR = FareRule.from_dict(FULL_FR_DICT)

def test_fare_rule_happyflow_minimal():
    """
    test_fare_rule_happyflow_minimal: minimal, correct example
    """
    fare_rule = FareRule.from_gtfs(MINIMAL_FR_DICT.keys(), MINIMAL_FR_DICT.values())
    assert fare_rule == MINIMAL_FR

def test_fare_rule_happyflow_full():
    """
    test_fare_rule_happyflow_full: full, correct example
    """
    fare_rule = FareRule.from_gtfs(FULL_FR_DICT.keys(), FULL_FR_DICT.values())
    assert fare_rule == FULL_FR

def test_missing_key():
    """
    test_missing_key: check if it errors if a required key is missing
    """
    temp_dict = FULL_FR_DICT.copy()
    del temp_dict["fare_id"]
    with pytest.raises(MissingKeyError):
        FareRule.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_invalid_values():
    """
    test_invalid_values: test for values out of range, invalid enums, ...
    """
    # TODO: test ids

def test_invalid_key():
    """
    test_invalid_key: test if it errors if an invalid key is passed
    """
    temp_dict = MINIMAL_FR_DICT.copy()
    temp_dict["fare_rule_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        FareRule.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_representation():
    """
    test_representation: check if __str__ and __repr__ are defined
    """
    assert str(MINIMAL_FR) != ""
    assert repr(MINIMAL_FR) != ""

def test_empty_value():
    """
    test_empty_value: test if it doesn't overwrite values with empty string
    """
    temp_dict = MINIMAL_FR_DICT.copy()
    temp_dict["fare_id"] = ""
    with pytest.raises(MissingKeyError):
        FareRule.from_gtfs(temp_dict.keys(), temp_dict.values())

# pylint: disable=comparison-with-itself
def test_equal():
    """
    test_equal: check if __eq__ functions
    """
    assert MINIMAL_FR == MINIMAL_FR
    assert MINIMAL_FR != FULL_FR
    assert FULL_FR != MINIMAL_FR
    assert FULL_FR == FULL_FR
    assert MINIMAL_FR != "MINIMAL_FR"

    temp_dict = MINIMAL_FR_DICT.copy()
    temp_dict["fare_id"] = 2
    temp_fare_rule = FareRule.from_dict(temp_dict)

    assert temp_fare_rule != MINIMAL_FR
