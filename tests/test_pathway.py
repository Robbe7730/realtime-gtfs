"""
test_pathway.py: tests for realtime_gtfs/pathway.py
"""

import pytest

from realtime_gtfs.models import Pathway
from realtime_gtfs.exceptions import MissingKeyError, InvalidKeyError, InvalidValueError

MINIMAL_PATHWAY_DICT = {
    "pathway_id": "123",
    "from_stop_id": "123",
    "to_stop_id": "123",
    "pathway_mode": "6",
    "is_bidirectional": "0"
}

FULL_PATHWAY_DICT = {
    "pathway_id": "123",
    "from_stop_id": "123",
    "to_stop_id": "123",
    "pathway_mode": "2",
    "is_bidirectional": "1",
    "length": "100",
    "traversal_time": "10",
    "stair_count": "97",
    "min_width": "0.5",
    "signposted_as": "This Way",
    "reversed_signposted_as": "Not This Way"
}

MINIMAL_PATHWAY = Pathway.from_dict(MINIMAL_PATHWAY_DICT)
FULL_PATHWAY = Pathway.from_dict(FULL_PATHWAY_DICT)

def test_pathway_happyflow_minimal():
    """
    test_pathway_happyflow_minimal: minimal, correct example
    """
    pathway = Pathway.from_gtfs(MINIMAL_PATHWAY_DICT.keys(), MINIMAL_PATHWAY_DICT.values())
    assert pathway == MINIMAL_PATHWAY

def test_pathway_happyflow_full():
    """
    test_pathway_happyflow_full: full, correct example
    """
    pathway = Pathway.from_gtfs(FULL_PATHWAY_DICT.keys(), FULL_PATHWAY_DICT.values())
    assert pathway == FULL_PATHWAY

def test_missing_key():
    """
    test_missing_key: check if it errors if a required key is missing
    """
    temp_dict = FULL_PATHWAY_DICT.copy()
    del temp_dict["pathway_id"]
    with pytest.raises(MissingKeyError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_PATHWAY_DICT.copy()
    del temp_dict["from_stop_id"]
    with pytest.raises(MissingKeyError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_PATHWAY_DICT.copy()
    del temp_dict["to_stop_id"]
    with pytest.raises(MissingKeyError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_PATHWAY_DICT.copy()
    del temp_dict["pathway_mode"]
    with pytest.raises(MissingKeyError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_PATHWAY_DICT.copy()
    del temp_dict["is_bidirectional"]
    with pytest.raises(MissingKeyError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_invalid_values():
    """
    test_invalid_values: test for values out of range, invalid enums, ...
    """
    # TODO: test pathway_id, from_stop_id, to_stop_id

    temp_dict = FULL_PATHWAY_DICT.copy()
    temp_dict["pathway_mode"] = "-1"
    with pytest.raises(InvalidValueError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())
    temp_dict["pathway_mode"] = "8"
    with pytest.raises(InvalidValueError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = FULL_PATHWAY_DICT.copy()
    temp_dict["is_bidirectional"] = "-1"
    with pytest.raises(InvalidValueError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())
    temp_dict["is_bidirectional"] = "2"
    with pytest.raises(InvalidValueError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_PATHWAY_DICT.copy()
    temp_dict["length"] = "-1"
    with pytest.raises(InvalidValueError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_PATHWAY_DICT.copy()
    temp_dict["traversal_time"] = "-1"
    with pytest.raises(InvalidValueError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_PATHWAY_DICT.copy()
    temp_dict["stair_count"] = "1"
    Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())
    temp_dict["stair_count"] = "-1"
    Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())
    temp_dict["stair_count"] = "0"
    with pytest.raises(InvalidValueError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_PATHWAY_DICT.copy()
    temp_dict["pathway_mode"] = "3"
    temp_dict["max_slope"] = "10"
    with pytest.raises(InvalidValueError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())
    temp_dict["max_slope"] = "-1"
    temp_dict["pathway_mode"] = "1"
    with pytest.raises(InvalidValueError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_PATHWAY_DICT.copy()
    temp_dict["min_width"] = "-10"
    with pytest.raises(InvalidValueError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())

    temp_dict = MINIMAL_PATHWAY_DICT.copy()
    temp_dict["is_bidirectional"] = "1"
    temp_dict["pathway_mode"] = "6"
    with pytest.raises(InvalidValueError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_invalid_key():
    """
    test_invalid_key: test if it errors if an invalid key is passed
    """
    temp_dict = MINIMAL_PATHWAY_DICT.copy()
    temp_dict["pathway_favorite_food"] = "Pizza"
    with pytest.raises(InvalidKeyError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())

def test_representation():
    """
    test_representation: check if __str__ and __repr__ are defined
    """
    assert str(MINIMAL_PATHWAY) != ""
    assert repr(MINIMAL_PATHWAY) != ""

def test_empty_value():
    """
    test_empty_value: test if it doesn't overwrite values with empty string
    """
    temp_dict = MINIMAL_PATHWAY_DICT.copy()
    temp_dict["to_stop_id"] = ""
    with pytest.raises(MissingKeyError):
        Pathway.from_gtfs(temp_dict.keys(), temp_dict.values())

# pylint: disable=comparison-with-itself
def test_equal():
    """
    test_equal: check if __eq__ functions
    """
    assert MINIMAL_PATHWAY == MINIMAL_PATHWAY
    assert MINIMAL_PATHWAY != FULL_PATHWAY
    assert FULL_PATHWAY != MINIMAL_PATHWAY
    assert FULL_PATHWAY == FULL_PATHWAY
    assert MINIMAL_PATHWAY != "MINIMAL_PATHWAY"

    temp_dict = MINIMAL_PATHWAY_DICT.copy()
    temp_dict["length"] = 2
    temp_pathway = Pathway.from_dict(temp_dict)

    assert temp_pathway != MINIMAL_PATHWAY
