"""
test_route.py: tests for realtime_gtfs/route.py
"""

import pytest

from realtime_gtfs.models import Route
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError, InvalidValueError

MINIMAL_ROUTE_DICT = {
    "route_id": "shortcut",
    "route_short_name": "srtct",
    "route_type": "1"

}

FULL_ROUTE_DICT = {
    "route_id": "long_way",
    "agency_id": "123",
    "route_short_name": "Long Way",
    "route_long_name": "The Looooong Way",
    "route_desc": "Take the long way home",
    "route_type": "6",
    "route_url": "https://longway.home/redirect?to=longway.home/index.html",
    "route_color": "FF7F00",
    "route_text_color": "007FFF",
    "route_sort_order": "123"
}

MINIMAL_ROUTE = Route.from_dict(MINIMAL_ROUTE_DICT)
FULL_ROUTE = Route.from_dict(FULL_ROUTE_DICT)

def test_route_happyflow_minimal():
    """
    test_route_happyflow_minimal: minimal, correct example
    """
    route = Route.from_gtfs(MINIMAL_ROUTE_DICT.keys(), MINIMAL_ROUTE_DICT.values())
    assert route == MINIMAL_ROUTE

def test_route_happyflow_full():
    """
    test_route_happyflow_full: full, correct example
    """
    route = Route.from_gtfs(FULL_ROUTE_DICT.keys(), FULL_ROUTE_DICT.values())
    assert route == FULL_ROUTE

def test_missing_key():
    """
    test_missing_key: check if it errors if a required key is missing
    """
    temp_dict = FULL_ROUTE_DICT.copy()
    del temp_dict["route_id"]
    with pytest.raises(MissingKeyError):
        Route.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_ROUTE_DICT.copy()
    del temp_dict["route_short_name"]
    del temp_dict["route_long_name"]
    with pytest.raises(MissingKeyError):
        Route.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_ROUTE_DICT.copy()
    del temp_dict["route_type"]
    with pytest.raises(MissingKeyError):
        Route.from_gtfs(temp_dict.keys(), temp_dict.values())


def test_invalid_values():
    """
    test_invalid_values: test for values out of range, invalid enums, ...
    """
    temp_dict = MINIMAL_ROUTE_DICT.copy()
    temp_dict["route_type"] = "-1"
    with pytest.raises(InvalidValueError):
        Route.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_ROUTE_DICT.copy()
    temp_dict["route_type"] = "8"
    with pytest.raises(InvalidValueError):
        Route.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_ROUTE_DICT.copy()
    temp_dict["route_color"] = "GREEN"
    with pytest.raises(InvalidValueError):
        Route.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_ROUTE_DICT.copy()
    temp_dict["route_color"] = "FFGFFF"
    with pytest.raises(InvalidValueError):
        Route.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_ROUTE_DICT.copy()
    temp_dict["route_color"] = "0xff7f00"
    with pytest.raises(InvalidValueError):
        Route.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_ROUTE_DICT.copy()
    temp_dict["route_text_color"] = "GREEN"
    with pytest.raises(InvalidValueError):
        Route.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_ROUTE_DICT.copy()
    temp_dict["route_text_color"] = "FFGFFF"
    with pytest.raises(InvalidValueError):
        Route.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_ROUTE_DICT.copy()
    temp_dict["route_text_color"] = "0xff7f00"
    with pytest.raises(InvalidValueError):
        Route.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_ROUTE_DICT.copy()
    temp_dict["route_sort_order"] = "-1"
    with pytest.raises(InvalidValueError):
        Route.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_default():
    """
    test_default: check for correct default values (wheelchair_boarding and location_type)
    """
    assert MINIMAL_ROUTE.route_color == "FFFFFF"
    assert MINIMAL_ROUTE.route_text_color == "000000"

def test_invalid_key():
    """
    test_invalid_key: test if it errors if an invalid key is passed
    """
    temp_dict = MINIMAL_ROUTE_DICT.copy()
    temp_dict["route_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        Route.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_representation():
    """
    test_representation: check if __str__ and __repr__ are defined
    """
    assert str(MINIMAL_ROUTE) != ""
    assert repr(MINIMAL_ROUTE) != ""

def test_empty_value():
    """
    test_empty_value: test if it doesn't overwrite values with empty string
    """
    temp_dict = MINIMAL_ROUTE_DICT.copy()
    temp_dict["route_id"] = ""
    with pytest.raises(MissingKeyError):
        Route.from_gtfs(temp_dict.keys(), temp_dict.values())

# pylint: disable=comparison-with-itself
def test_equal():
    """
    test_equal: check if __eq__ functions
    """
    assert MINIMAL_ROUTE == MINIMAL_ROUTE
    assert MINIMAL_ROUTE != FULL_ROUTE
    assert FULL_ROUTE != MINIMAL_ROUTE
    assert FULL_ROUTE == FULL_ROUTE
    assert MINIMAL_ROUTE != "MINIMAL_ROUTE"

    temp_dict = MINIMAL_ROUTE_DICT.copy()
    temp_dict["route_short_name"] = 2
    temp_route = Route.from_dict(temp_dict)

    assert temp_route != MINIMAL_ROUTE
