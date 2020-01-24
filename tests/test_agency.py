"""
test_agency: tests for realtime_gtfs/agency.py
"""

import pytest

from realtime_gtfs.models import Agency
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError, InvalidValueError

MINIMAL_AGENCY_DICT = {
    "agency_id": "Minimal",
    "agency_name": "Minimal inc",
    "agency_url": "https://minimal.com/",
    "agency_timezone": "Europe/Brussels"
}

FULL_AGENCY_DICT = {
    "agency_id": "Full",
    "agency_name": "Full inc",
    "agency_url": "https://full.com/",
    "agency_timezone": "Europe/Brussels",
    "agency_lang": "en",
    "agency_phone": "0123456789",
    "agency_email": "root@full.com",
    "agency_fare_url": "https://full.com/fares",
}

MINIMAL_AGENCY = Agency.from_dict(MINIMAL_AGENCY_DICT)
FULL_AGENCY = Agency.from_dict(FULL_AGENCY_DICT)

def test_agency_happyflow_minimal():
    """
    test_agency_happyflow_minimal: minimal, correct example
    """
    agency = Agency.from_gtfs(MINIMAL_AGENCY_DICT.keys(), MINIMAL_AGENCY_DICT.values())
    assert agency == MINIMAL_AGENCY

def test_agency_happyflow_full():
    """
    test_agency_happyflow_full: full, correct example
    """
    agency = Agency.from_gtfs(FULL_AGENCY_DICT.keys(), FULL_AGENCY_DICT.values())
    assert agency == FULL_AGENCY

def test_invalid_timezone():
    """
    test_invalid_timezone: check if it raises InvalidValueError when given an invalid timezone
    """
    temp_dict = MINIMAL_AGENCY_DICT.copy()
    temp_dict["agency_timezone"] = "MiddleEarth/Shire"
    with pytest.raises(InvalidValueError):
        Agency.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_missing_key():
    """
    test_missing_key: check if it errors if a required key is missing
    """
    temp_dict = MINIMAL_AGENCY_DICT.copy()
    del temp_dict["agency_name"]
    with pytest.raises(MissingKeyError):
        Agency.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_AGENCY_DICT.copy()
    del temp_dict["agency_url"]
    with pytest.raises(MissingKeyError):
        Agency.from_gtfs(temp_dict.keys(), temp_dict.values())
    temp_dict = MINIMAL_AGENCY_DICT.copy()

    del temp_dict["agency_timezone"]
    with pytest.raises(MissingKeyError):
        Agency.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_invalid_key():
    """
    test_invalid_key: test if it errors if an invalid key is passed
    """
    temp_dict = MINIMAL_AGENCY_DICT.copy()
    temp_dict["agency_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        Agency.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_representation():
    """
    test_representation: check if __str__ and __repr__ are defined
    """
    assert str(MINIMAL_AGENCY) != ""
    assert repr(MINIMAL_AGENCY) != ""

def test_empty_value():
    """
    test_empty_value: test if it doesn't overwrite values with empty string
    """
    temp_dict = MINIMAL_AGENCY_DICT.copy()
    temp_dict["agency_name"] = ""
    with pytest.raises(MissingKeyError):
        Agency.from_gtfs(temp_dict.keys(), temp_dict.values())

# pylint: disable=comparison-with-itself
def test_equal():
    """
    test_equal: check if __eq__ functions
    """
    assert MINIMAL_AGENCY == MINIMAL_AGENCY
    assert MINIMAL_AGENCY != FULL_AGENCY
    assert FULL_AGENCY != MINIMAL_AGENCY
    assert FULL_AGENCY == FULL_AGENCY
    assert MINIMAL_AGENCY != "MINIMAL_AGENCY"
