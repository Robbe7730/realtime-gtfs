"""
shape.py: contains data relevant to shapes.txt
"""

import sqlalchemy as sa

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError, InvalidValueError

class Shape():
    """
    shape: class for shapes
    """
    def __init__(self):
        self.shape_id = None
        self.shape_pt_lat = None
        self.shape_pt_lon = None
        self.shape_pt_sequence = None
        self.shape_dist_traveled = None

    @staticmethod
    def create_table(meta):
        """
        Create the SQLAlchemy table
        """
        sa.Table(
            'shapes', meta,
            sa.Column('shape_id', sa.String(length=255), primary_key=True),
            sa.Column('shape_pt_lat', sa.Float()),
            sa.Column('shape_pt_lon', sa.Float()),
            sa.Column('shape_pt_sequence', sa.Integer()),
            sa.Column('shape_dist_traveled', sa.Float()),
        )

    @staticmethod
    def from_dict(data):
        """
        Creates a Shape from a dict. Checks correctness after
        creation.

        Arguments:
        data: dict containing the data
        """
        ret = Shape()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        """
        Creates an Shape from a list of keys and a list of
        corresponding values. Checks correctness after creation

        Arguments:
        keys: list of keys (strings)
        data: list of values (strings)
        """
        ret = Shape()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret

    def verify(self):
        """
        Verify that the Shape has at least the required keys, lat and lon are correct
        """
        # TODO: verify zone_id, level_id, parent_station
        if self.shape_id is None:
            raise MissingKeyError("shape_id")
        if self.shape_pt_lat is None:
            raise MissingKeyError("shape_pt_lat")
        if self.shape_pt_lon is None:
            raise MissingKeyError("shape_pt_lon")
        if self.shape_pt_sequence is None:
            raise MissingKeyError("shape_pt_sequence")

        if self.shape_pt_lon < -180 or self.shape_pt_lon > 180:
            raise InvalidValueError("shape_pt_lon")
        if self.shape_pt_lat < -90 or self.shape_pt_lat > 90:
            raise InvalidValueError("shape_pt_lat")
        if self.shape_pt_sequence < 0:
            raise InvalidValueError("shape_pt_sequence")
        if self.shape_dist_traveled is not None and self.shape_dist_traveled < 0:
            raise InvalidValueError("shape_dist_traveled")

        return True

    def setkey(self, key, value):
        """
        Sets a class attribute depending on `key`, raising
        InvalidKeyError if the key does not belong on shape

        Arguments:
        key, value: the key and value
        """
        if value == "":
            return
        if key == "shape_id":
            self.shape_id = value
        elif key == "shape_pt_lat":
            self.shape_pt_lat = float(value)
        elif key == "shape_pt_lon":
            self.shape_pt_lon = float(value)
        elif key == "shape_pt_sequence":
            self.shape_pt_sequence = int(value)
        elif key == "shape_dist_traveled":
            self.shape_dist_traveled = float(value)
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[Shape {self.shape_id} #{self.shape_pt_sequence}"

    def __eq__(self, other):
        if not isinstance(other, Shape):
            return False
        return (
            self.shape_id == other.shape_id and
            self.shape_pt_lat == other.shape_pt_lat and
            self.shape_pt_lon == other.shape_pt_lon and
            self.shape_pt_sequence == other.shape_pt_sequence and
            self.shape_dist_traveled == other.shape_dist_traveled
        )
