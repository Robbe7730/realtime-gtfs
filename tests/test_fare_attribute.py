"""
test_fare_attribute.py: tests for realtime_gtfs/fare_attribute.py
"""

import pytest

from realtime_gtfs.models import FareAttribute
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError, InvalidValueError

MINIMAL_FA_DICT = {
    "fare_id": "123",
    "price": "0.50",
    "currency_type": "EUR",
    "payment_method": "1",
    "transfers": "4"
}

FULL_FA_DICT = {
    "fare_id": "132",
    "price": "0.51",
    "currency_type": "USD",
    "payment_method": "0",
    "transfers": "0",
    "agency_id": "123",
    "transfer_duration": "3600"
}

MINIMAL_FA = FareAttribute.from_dict(MINIMAL_FA_DICT)
FULL_FA = FareAttribute.from_dict(FULL_FA_DICT)

def test_fare_attribute_happyflow_minimal():
    """
    test_fare_attribute_happyflow_minimal: minimal, correct example
    """
    fare_attribute = FareAttribute.from_gtfs(MINIMAL_FA_DICT.keys(), MINIMAL_FA_DICT.values())
    assert fare_attribute == MINIMAL_FA

def test_fare_attribute_happyflow_full():
    """
    test_fare_attribute_happyflow_full: full, correct example
    """
    fare_attribute = FareAttribute.from_gtfs(FULL_FA_DICT.keys(), FULL_FA_DICT.values())
    assert fare_attribute == FULL_FA

def test_missing_key():
    """
    test_missing_key: check if it errors if a required key is missing
    """
    temp_dict = FULL_FA_DICT.copy()
    del temp_dict["fare_id"]
    with pytest.raises(MissingKeyError):
        FareAttribute.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_FA_DICT.copy()
    del temp_dict["price"]
    with pytest.raises(MissingKeyError):
        FareAttribute.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_FA_DICT.copy()
    del temp_dict["currency_type"]
    with pytest.raises(MissingKeyError):
        FareAttribute.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_FA_DICT.copy()
    del temp_dict["payment_method"]
    with pytest.raises(MissingKeyError):
        FareAttribute.from_gtfs(temp_dict.keys(), temp_dict.values())



def test_invalid_values():
    """
    test_invalid_values: test for values out of range, invalid enums, ...
    """
    # TODO: test currency_type
    temp_dict = FULL_FA_DICT.copy()
    temp_dict["price"] = "-0.5"
    with pytest.raises(InvalidValueError):
        FareAttribute.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_FA_DICT.copy()
    temp_dict["payment_method"] = "-1"
    with pytest.raises(InvalidValueError):
        FareAttribute.from_gtfs(temp_dict.keys(), temp_dict.values())
    temp_dict["payment_method"] = "2"
    with pytest.raises(InvalidValueError):
        FareAttribute.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_FA_DICT.copy()
    temp_dict["transfers"] = "-1"
    with pytest.raises(InvalidValueError):
        FareAttribute.from_gtfs(temp_dict.keys(), temp_dict.values())
    temp_dict["transfers"] = "6"
    with pytest.raises(InvalidValueError):
        FareAttribute.from_gtfs(temp_dict.keys(), temp_dict.values())
    del temp_dict["transfers"]
    FareAttribute.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_FA_DICT.copy()
    temp_dict["transfer_duration"] = "-2"
    with pytest.raises(InvalidValueError):
        FareAttribute.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_invalid_key():
    """
    test_invalid_key: test if it errors if an invalid key is passed
    """
    temp_dict = MINIMAL_FA_DICT.copy()
    temp_dict["fare_attribute_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        FareAttribute.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_representation():
    """
    test_representation: check if __str__ and __repr__ are defined
    """
    assert str(MINIMAL_FA) != ""
    assert repr(MINIMAL_FA) != ""

def test_empty_value():
    """
    test_empty_value: test if it doesn't overwrite values with empty string
    """
    temp_dict = MINIMAL_FA_DICT.copy()
    temp_dict["fare_id"] = ""
    with pytest.raises(MissingKeyError):
        FareAttribute.from_gtfs(temp_dict.keys(), temp_dict.values())

# pylint: disable=comparison-with-itself
def test_equal():
    """
    test_equal: check if __eq__ functions
    """
    assert MINIMAL_FA == MINIMAL_FA
    assert MINIMAL_FA != FULL_FA
    assert FULL_FA != MINIMAL_FA
    assert FULL_FA == FULL_FA
    assert MINIMAL_FA != "MINIMAL_FA"

    temp_dict = MINIMAL_FA_DICT.copy()
    temp_dict["fare_id"] = 2
    temp_fare_attribute = FareAttribute.from_dict(temp_dict)

    assert temp_fare_attribute != MINIMAL_FA
