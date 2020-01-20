"""
test_translation.py: tests for realtime_gtfs/translation.py
"""

import pytest

from realtime_gtfs.models import Translation
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError, InvalidValueError

RECORD_TRANSLATION_DICT = {
    "table_name": "stop_times",
    "field_name": "stop_name",
    "language": "NL",
    "translation": "Halte 1",
    "record_id": "1",
    "record_sub_id": "12"
}

VALUE_TRANSLATION_DICT = {
    "table_name": "trips",
    "field_name": "trip_headsign",
    "language": "FR",
    "translation": "Le Train",
    "field_value": "The Train"
}

RECORD_TRANSLATION = Translation.from_dict(RECORD_TRANSLATION_DICT)
VALUE_TRANSLATION = Translation.from_dict(VALUE_TRANSLATION_DICT)

def test_translation_happyflow_record():
    """
    test_translation_happyflow_record: correct example by record_id
    """
    translation = Translation.from_gtfs(RECORD_TRANSLATION_DICT.keys(),
                                        RECORD_TRANSLATION_DICT.values())
    assert translation == RECORD_TRANSLATION

def test_translation_happyflow_value():
    """
    test_translation_happyflow_value: correct example by value
    """
    translation = Translation.from_gtfs(VALUE_TRANSLATION_DICT.keys(),
                                        VALUE_TRANSLATION_DICT.values())
    assert translation == VALUE_TRANSLATION

def test_missing_key():
    """
    test_missing_key: check if it errors if a required key is missing
    """
    temp_dict = VALUE_TRANSLATION_DICT.copy()
    del temp_dict["table_name"]
    with pytest.raises(MissingKeyError):
        Translation.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = RECORD_TRANSLATION_DICT.copy()
    del temp_dict["field_name"]
    with pytest.raises(MissingKeyError):
        Translation.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = RECORD_TRANSLATION_DICT.copy()
    del temp_dict["language"]
    with pytest.raises(MissingKeyError):
        Translation.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = RECORD_TRANSLATION_DICT.copy()
    del temp_dict["translation"]
    with pytest.raises(MissingKeyError):
        Translation.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = VALUE_TRANSLATION_DICT.copy()
    del temp_dict["field_value"]
    with pytest.raises(MissingKeyError):
        Translation.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_invalid_values():
    """
    test_invalid_values: test for values out of range, invalid enums, ...
    """
    # TODO: test language_code
    temp_dict = VALUE_TRANSLATION_DICT.copy()
    temp_dict["table_name"] = "no_such_table"
    with pytest.raises(InvalidValueError):
        Translation.from_gtfs(temp_dict.keys(), temp_dict.values())
    temp_dict["table_name"] = "feed_info"
    with pytest.raises(InvalidValueError):
        Translation.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = RECORD_TRANSLATION_DICT.copy()
    temp_dict["table_name"] = "feed_info"
    del temp_dict["record_sub_id"]
    with pytest.raises(InvalidValueError):
        Translation.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = RECORD_TRANSLATION_DICT.copy()
    temp_dict["field_value"] = "abc"
    with pytest.raises(InvalidValueError):
        Translation.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = RECORD_TRANSLATION_DICT.copy()
    temp_dict["table_name"] = "feed_info"
    del temp_dict["record_sub_id"]
    with pytest.raises(InvalidValueError):
        Translation.from_gtfs(temp_dict.keys(), temp_dict.values())
    del temp_dict["record_id"]
    temp_dict["record_sub_id"] = "2"
    with pytest.raises(MissingKeyError):
        Translation.from_gtfs(temp_dict.keys(), temp_dict.values())
    temp_dict["table_name"] = "stop_times"
    del temp_dict["record_sub_id"]
    with pytest.raises(MissingKeyError):
        Translation.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = RECORD_TRANSLATION_DICT.copy()
    temp_dict["table_name"] = "agency"
    temp_dict["record_sub_id"] = "123"
    with pytest.raises(InvalidValueError):
        Translation.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = RECORD_TRANSLATION_DICT.copy()
    del temp_dict["record_sub_id"]
    with pytest.raises(MissingKeyError):
        Translation.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_invalid_key():
    """
    test_invalid_key: test if it errors if an invalid key is passed
    """
    temp_dict = VALUE_TRANSLATION_DICT.copy()
    temp_dict["translation_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        Translation.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_representation():
    """
    test_representation: check if __str__ and __repr__ are defined
    """
    assert str(VALUE_TRANSLATION) != ""
    assert repr(RECORD_TRANSLATION) != ""

def test_empty_value():
    """
    test_empty_value: test if it doesn't overwrite values with empty string
    """
    temp_dict = VALUE_TRANSLATION_DICT.copy()
    temp_dict["table_name"] = ""
    with pytest.raises(MissingKeyError):
        Translation.from_gtfs(temp_dict.keys(), temp_dict.values())

# pylint: disable=comparison-with-itself
def test_equal():
    """
    test_equal: check if __eq__ functions
    """
    assert RECORD_TRANSLATION == RECORD_TRANSLATION
    assert RECORD_TRANSLATION != VALUE_TRANSLATION
    assert VALUE_TRANSLATION != RECORD_TRANSLATION
    assert VALUE_TRANSLATION == VALUE_TRANSLATION
    assert RECORD_TRANSLATION != "RECORD_TRANSLATION"

    temp_dict = VALUE_TRANSLATION_DICT.copy()
    temp_dict["table_name"] = "routes"
    temp_translation = Translation.from_dict(temp_dict)

    assert temp_translation != VALUE_TRANSLATION
