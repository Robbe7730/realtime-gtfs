"""
test_feed_info: tests for realtime_gtfs/feed_info.py
"""

import pytest

from realtime_gtfs.models import FeedInfo
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError

MINIMAL_FEED_INFO_DICT = {
    "feed_publisher_name": "Publish Inc",
    "feed_publisher_url": "https://publi.sh/",
    "feed_lang": "NL"
}

FULL_FEED_INFO_DICT = {
    "feed_publisher_name": "Printer Inc",
    "feed_publisher_url": "https://print.er/inc",
    "feed_lang": "EN",
    "feed_start_date": "20111111",
    "feed_end_date": "20211111",
    "feed_version": "3.1",
    "feed_contact_email": "info@print.er",
    "feed_contact_url": "https://print.er/help"
}

MINIMAL_FEED_INFO = FeedInfo.from_dict(MINIMAL_FEED_INFO_DICT)
FULL_FEED_INFO = FeedInfo.from_dict(FULL_FEED_INFO_DICT)

def test_feed_info_happyflow_minimal():
    """
    test_feed_info_happyflow_minimal: minimal, correct example
    """
    feed_info = FeedInfo.from_gtfs(MINIMAL_FEED_INFO_DICT.keys(), MINIMAL_FEED_INFO_DICT.values())
    assert feed_info == MINIMAL_FEED_INFO

def test_feed_info_happyflow_full():
    """
    test_feed_info_happyflow_full: full, correct example
    """
    feed_info = FeedInfo.from_gtfs(FULL_FEED_INFO_DICT.keys(), FULL_FEED_INFO_DICT.values())
    assert feed_info == FULL_FEED_INFO

def test_missing_key():
    """
    test_missing_key: check if it errors if a required key is missing
    """
    temp_dict = MINIMAL_FEED_INFO_DICT.copy()
    del temp_dict["feed_publisher_name"]
    with pytest.raises(MissingKeyError):
        FeedInfo.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_FEED_INFO_DICT.copy()
    del temp_dict["feed_publisher_url"]
    with pytest.raises(MissingKeyError):
        FeedInfo.from_gtfs(temp_dict.keys(), temp_dict.values())
    temp_dict = MINIMAL_FEED_INFO_DICT.copy()

    del temp_dict["feed_lang"]
    with pytest.raises(MissingKeyError):
        FeedInfo.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_invalid_key():
    """
    test_invalid_key: test if it errors if an invalid key is passed
    """
    temp_dict = MINIMAL_FEED_INFO_DICT.copy()
    temp_dict["feed_info_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        FeedInfo.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_representation():
    """
    test_representation: check if __str__ and __repr__ are defined
    """
    assert str(MINIMAL_FEED_INFO) != ""
    assert repr(MINIMAL_FEED_INFO) != ""

def test_empty_value():
    """
    test_empty_value: test if it doesn't overwrite values with empty string
    """
    temp_dict = MINIMAL_FEED_INFO_DICT.copy()
    temp_dict["feed_publisher_name"] = ""
    with pytest.raises(MissingKeyError):
        FeedInfo.from_gtfs(temp_dict.keys(), temp_dict.values())

# pylint: disable=comparison-with-itself
def test_equal():
    """
    test_equal: check if __eq__ functions
    """
    assert MINIMAL_FEED_INFO == MINIMAL_FEED_INFO
    assert MINIMAL_FEED_INFO != FULL_FEED_INFO
    assert FULL_FEED_INFO != MINIMAL_FEED_INFO
    assert FULL_FEED_INFO == FULL_FEED_INFO
    assert MINIMAL_FEED_INFO != "MINIMAL_FEED_INFO"
