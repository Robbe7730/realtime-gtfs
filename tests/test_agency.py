from realtime_gtfs.agency import Agency
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError
import pytz
import pytest

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
    agency = Agency.from_gtfs(MINIMAL_AGENCY_DICT.keys(), MINIMAL_AGENCY_DICT.values())
    assert(agency == MINIMAL_AGENCY)

def test_agency_happyflow_full():
    agency = Agency.from_gtfs(FULL_AGENCY_DICT.keys(), FULL_AGENCY_DICT.values())
    assert(agency == FULL_AGENCY)

def test_invalid_timezone():
    temp_dict = MINIMAL_AGENCY_DICT.copy()
    temp_dict["agency_timezone"] = "MiddleEarth/Shire"
    with pytest.raises(pytz.exceptions.UnknownTimeZoneError):
        Agency.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_missing_key():
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
    temp_dict = MINIMAL_AGENCY_DICT.copy()
    temp_dict["agency_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        Agency.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_representation():
    assert(str(MINIMAL_AGENCY) != "")
    assert(repr(MINIMAL_AGENCY) != "")

def test_equal():
    assert(MINIMAL_AGENCY == MINIMAL_AGENCY)
    assert(MINIMAL_AGENCY != FULL_AGENCY)
    assert(FULL_AGENCY != MINIMAL_AGENCY)
    assert(FULL_AGENCY == FULL_AGENCY)
    assert(MINIMAL_AGENCY != "MINIMAL_AGENCY")