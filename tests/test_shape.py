"""
test_shape: tests for realtime_gtfs/shape.py
"""
import pytest

from realtime_gtfs.models import Shape
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError, InvalidValueError

MINIMAL_SHAPE_DICT = {
    "shape_id": "123",
    "shape_pt_lat": "4.5",
    "shape_pt_lon": "6.7",
    "shape_pt_sequence": "8"
}

FULL_SHAPE_DICT = {
    "shape_id": "123",
    "shape_pt_lat": "7.6",
    "shape_pt_lon": "6.5",
    "shape_pt_sequence": "7",
    "shape_dist_traveled": "13.37"
}

MINIMAL_SHAPE = Shape.from_dict(MINIMAL_SHAPE_DICT)
FULL_SHAPE = Shape.from_dict(FULL_SHAPE_DICT)

def test_shape_happyflow_minimal():
    """
    test_shape_happyflow_minimal: minimal, correct example
    """
    shape = Shape.from_gtfs(MINIMAL_SHAPE_DICT.keys(), MINIMAL_SHAPE_DICT.values())
    assert shape == MINIMAL_SHAPE

def test_shape_happyflow_full():
    """
    test_shape_happyflow_full: full, correct example
    """
    shape = Shape.from_gtfs(FULL_SHAPE_DICT.keys(), FULL_SHAPE_DICT.values())
    assert shape == FULL_SHAPE

def test_missing_key():
    """
    test_missing_key: check if it errors if a required key is missing
    """
    temp_dict = MINIMAL_SHAPE_DICT.copy()
    del temp_dict["shape_id"]
    with pytest.raises(MissingKeyError):
        Shape.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_SHAPE_DICT.copy()
    del temp_dict["shape_pt_lat"]
    with pytest.raises(MissingKeyError):
        Shape.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_SHAPE_DICT.copy()
    del temp_dict["shape_pt_lon"]
    with pytest.raises(MissingKeyError):
        Shape.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_SHAPE_DICT.copy()
    del temp_dict["shape_pt_sequence"]
    with pytest.raises(MissingKeyError):
        Shape.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_SHAPE_DICT.copy()
    temp_dict["shape_pt_lat"] = "-100"
    with pytest.raises(InvalidValueError):
        Shape.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_SHAPE_DICT.copy()
    temp_dict["shape_pt_lon"] = "-200"
    with pytest.raises(InvalidValueError):
        Shape.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_SHAPE_DICT.copy()
    temp_dict["shape_pt_sequence"] = "-2"
    with pytest.raises(InvalidValueError):
        Shape.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_SHAPE_DICT.copy()
    temp_dict["shape_dist_traveled"] = "-2"
    with pytest.raises(InvalidValueError):
        Shape.from_gtfs(temp_dict.keys(), temp_dict.values())


def test_invalid_key():
    """
    test_invalid_key: test if it errors if an invalid key is passed
    """
    temp_dict = MINIMAL_SHAPE_DICT.copy()
    temp_dict["shape_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        Shape.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_representation():
    """
    test_representation: check if __str__ and __repr__ are defined
    """
    assert str(MINIMAL_SHAPE) != ""
    assert repr(MINIMAL_SHAPE) != ""

def test_empty_value():
    """
    test_empty_value: test if it doesn't overwrite values with empty string
    """
    temp_dict = MINIMAL_SHAPE_DICT.copy()
    temp_dict["shape_id"] = ""
    with pytest.raises(MissingKeyError):
        Shape.from_gtfs(temp_dict.keys(), temp_dict.values())

# pylint: disable=comparison-with-itself
def test_equal():
    """
    test_equal: check if __eq__ functions
    """
    assert MINIMAL_SHAPE == MINIMAL_SHAPE
    assert MINIMAL_SHAPE != FULL_SHAPE
    assert FULL_SHAPE != MINIMAL_SHAPE
    assert FULL_SHAPE == FULL_SHAPE
    assert MINIMAL_SHAPE != "MINIMAL_SHAPE"
