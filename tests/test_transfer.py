"""
test_transfer.py: tests for realtime_gtfs/transfer.py
"""

import pytest

from realtime_gtfs.models import Transfer
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError, InvalidValueError

MINIMAL_TRANSFER_DICT = {
    "from_stop_id": "123",
    "to_stop_id": "123",
    "transfer_type": "2"
}

FULL_TRANSFER_DICT = {
    "from_stop_id": "124",
    "to_stop_id": "124",
    "transfer_type": "1",
    "min_transfer_time": "12",
    "from_route_id": "abc",
    "to_route_id": "abc",
    "from_trip_id": "abc",
    "to_trip_id": "abc"
}

MINIMAL_TRANSFER = Transfer.from_dict(MINIMAL_TRANSFER_DICT)
FULL_TRANSFER = Transfer.from_dict(FULL_TRANSFER_DICT)

def test_transfer_happyflow_minimal():
    """
    test_transfer_happyflow_minimal: minimal, correct example
    """
    transfer = Transfer.from_gtfs(MINIMAL_TRANSFER_DICT.keys(), MINIMAL_TRANSFER_DICT.values())
    assert transfer == MINIMAL_TRANSFER

def test_transfer_happyflow_full():
    """
    test_transfer_happyflow_full: full, correct example
    """
    transfer = Transfer.from_gtfs(FULL_TRANSFER_DICT.keys(), FULL_TRANSFER_DICT.values())
    assert transfer == FULL_TRANSFER

def test_missing_key():
    """
    test_missing_key: check if it errors if a required key is missing
    """
    temp_dict = MINIMAL_TRANSFER_DICT.copy()
    del temp_dict["from_stop_id"]
    with pytest.raises(MissingKeyError):
        Transfer.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_TRANSFER_DICT.copy()
    del temp_dict["to_stop_id"]
    with pytest.raises(MissingKeyError):
        Transfer.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_invalid_values():
    """
    test_invalid_values: test for values out of range, invalid enums, ...
    """
    temp_dict = MINIMAL_TRANSFER_DICT.copy()
    temp_dict["transfer_type"] = "-1"
    with pytest.raises(InvalidValueError):
        Transfer.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_TRANSFER_DICT.copy()
    temp_dict["transfer_type"] = "4"
    with pytest.raises(InvalidValueError):
        Transfer.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_TRANSFER_DICT.copy()
    temp_dict["min_transfer_time"] = "-1"
    with pytest.raises(InvalidValueError):
        Transfer.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_default():
    """
    test_default: check for correct default values (wheelchair_boarding and location_type)
    """
    temp_dict = MINIMAL_TRANSFER_DICT.copy()
    del temp_dict["transfer_type"]
    temp_transfer = Transfer.from_gtfs(temp_dict.keys(), temp_dict.values())
    assert temp_transfer.transfer_type == 0

def test_invalid_key():
    """
    test_invalid_key: test if it errors if an invalid key is passed
    """
    temp_dict = MINIMAL_TRANSFER_DICT.copy()
    temp_dict["transfer_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        Transfer.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_representation():
    """
    test_representation: check if __str__ and __repr__ are defined
    """
    assert str(MINIMAL_TRANSFER) != ""
    assert repr(MINIMAL_TRANSFER) != ""

def test_empty_value():
    """
    test_empty_value: test if it doesn't overwrite values with empty string
    """
    temp_dict = MINIMAL_TRANSFER_DICT.copy()
    temp_dict["to_stop_id"] = ""
    with pytest.raises(MissingKeyError):
        Transfer.from_gtfs(temp_dict.keys(), temp_dict.values())

# pylint: disable=comparison-with-itself
def test_equal():
    """
    test_equal: check if __eq__ functions
    """
    assert MINIMAL_TRANSFER == MINIMAL_TRANSFER
    assert MINIMAL_TRANSFER != FULL_TRANSFER
    assert FULL_TRANSFER != MINIMAL_TRANSFER
    assert FULL_TRANSFER == FULL_TRANSFER
    assert MINIMAL_TRANSFER != "MINIMAL_TRANSFER"

    temp_dict = MINIMAL_TRANSFER_DICT.copy()
    temp_dict["to_stop_id"] = "124"
    temp_transfer = Transfer.from_dict(temp_dict)

    assert temp_transfer != MINIMAL_TRANSFER
