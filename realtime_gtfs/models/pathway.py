"""
pathway.py: contains data relevant to pathways.txt
"""

import sqlalchemy as sa

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError, InvalidValueError

ENUM_PATHWAY_MODE = [
    "Walkway",
    "Stairs",
    "Moving sidewalk",
    "Escalator",
    "Elevator",
    "Payment gate",
    "Exit gate"
]

ENUM_IS_BIDIRECTIONAL = [
    "Unidirectional",
    "Bidirectional"
]

class Pathway():
    """
    Pathway: class for pathways
    """
    def __init__(self):
        self.pathway_id = None
        self.from_stop_id = None
        self.to_stop_id = None
        self.pathway_mode = None
        self.is_bidirectional = None
        self.length = None
        self.traversal_time = None
        self.stair_count = None
        self.max_slope = None
        self.min_width = None
        self.signposted_as = None
        self.reversed_signposted_as = None

    @staticmethod
    def create_table(meta):
        """
        Create the SQLAlchemy table
        """
        return sa.Table(
            'pathways', meta,
            sa.Column('pathway_id', sa.String(length=255), primary_key=True),
            sa.Column('from_stop_id', sa.String(length=255), sa.ForeignKey("stops.stop_id"),
                      nullable=False),
            sa.Column('to_stop_id', sa.String(length=255), sa.ForeignKey("stops.stop_id"),
                      nullable=False),
            sa.Column('pathway_mode', sa.Integer(), nullable=False),
            sa.Column('is_bidirectional', sa.Integer(), nullable=False),
            sa.Column('length', sa.Float()),
            sa.Column('traversal_time', sa.Integer()),
            sa.Column('stair_count', sa.Integer()),
            sa.Column('max_slope', sa.Float()),
            sa.Column('min_width', sa.Float()),
            sa.Column('signposted_as', sa.String(length=255)),
            sa.Column('reversed_signposted_as', sa.String(length=255)),
        )

    @staticmethod
    def from_dict(data):
        """
        Creates a Pathway from a dict. Checks correctness after
        creation.

        Arguments:
        data: dict containing the data
        """
        ret = Pathway()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    def to_dict(self):
        """
        to_dict: turn the class into a dict
        """
        ret = {}
        ret["pathway_id"] = self.pathway_id
        ret["from_stop_id"] = self.from_stop_id
        ret["to_stop_id"] = self.to_stop_id
        ret["pathway_mode"] = self.pathway_mode
        ret["is_bidirectional"] = self.is_bidirectional
        ret["length"] = self.length
        ret["traversal_time"] = self.traversal_time
        ret["stair_count"] = self.stair_count
        ret["max_slope"] = self.max_slope
        ret["min_width"] = self.min_width
        ret["signposted_as"] = self.signposted_as
        ret["reversed_signposted_as"] = self.reversed_signposted_as
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        """
        Creates an Pathway from a list of keys and a list of
        corresponding values. Checks correctness after creation

        Arguments:
        keys: list of keys (strings)
        data: list of values (strings)
        """
        ret = Pathway()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret

    def verify(self):
        """
        Verify that the Pathway has at least the required keys, lat and lon are correct
        """
        # TODO: verify pathway_id, from_stop_id and to_stop_id
        if self.pathway_id is None:
            raise MissingKeyError("pathway_id")
        if self.from_stop_id is None:
            raise MissingKeyError("from_stop_id")
        if self.to_stop_id is None:
            raise MissingKeyError("to_stop_id")
        if self.pathway_mode is None:
            raise MissingKeyError("pathway_mode")
        if self.is_bidirectional is None:
            raise MissingKeyError("is_bidirectional")

        if self.pathway_mode < 0 or self.pathway_mode >= len(ENUM_PATHWAY_MODE):
            raise InvalidValueError("pathway_mode")

        if self.is_bidirectional < 0 or self.is_bidirectional >= len(ENUM_IS_BIDIRECTIONAL):
            raise InvalidValueError("is_bidirectional")

        if self.length is not None and self.length < 0:
            raise InvalidValueError("length")

        if self.traversal_time is not None and self.traversal_time < 0:
            raise InvalidValueError("traversal_time")

        if self.stair_count is not None and self.stair_count == 0:
            raise InvalidValueError("stair_count")

        if self.is_bidirectional == 1 and (self.pathway_mode == 6 or self.pathway_mode == 7):
            raise InvalidValueError("is_bidirectional: fare/exit gates cannot be bidirectional")

        if self.max_slope is not None and (self.pathway_mode == 1 or self.pathway_mode == 3):
            raise InvalidValueError("max_slope: slope should only be used on (moving) walkways")

        if self.min_width is not None and self.min_width <= 0:
            raise InvalidValueError("min_width")

        return True

    def setkey(self, key, value):
        """
        Sets a class attribute depending on `key`, raising
        InvalidKeyError if the key does not belong on pathway

        Arguments:
        key, value: the key and value
        """
        if value == "":
            return


        if key == "pathway_id":
            self.pathway_id = value
        elif key == "from_stop_id":
            self.from_stop_id = value
        elif key == "to_stop_id":
            self.to_stop_id = value
        elif key == "pathway_mode":
            self.pathway_mode = int(value)
        elif key == "is_bidirectional":
            self.is_bidirectional = int(value)
        elif key == "length":
            self.length = float(value)
        elif key == "traversal_time":
            self.traversal_time = int(value)
        elif key == "stair_count":
            self.stair_count = int(value)
        elif key == "max_slope":
            self.max_slope = float(value)
        elif key == "min_width":
            self.min_width = float(value)
        elif key == "signposted_as":
            self.signposted_as = value
        elif key == "reversed_signposted_as":
            self.reversed_signposted_as = value
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[Pathway {self.from_stop_id} - {self.to_stop_id}]"

    def __eq__(self, other):
        if not isinstance(other, Pathway):
            return False
        return (
            self.pathway_id == other.pathway_id and
            self.from_stop_id == other.from_stop_id and
            self.to_stop_id == other.to_stop_id and
            self.pathway_mode == other.pathway_mode and
            self.is_bidirectional == other.is_bidirectional and
            self.length == other.length and
            self.traversal_time == other.traversal_time and
            self.stair_count == other.stair_count and
            self.max_slope == other.max_slope and
            self.min_width == other.min_width and
            self.signposted_as == other.signposted_as and
            self.reversed_signposted_as == other.reversed_signposted_as
        )
