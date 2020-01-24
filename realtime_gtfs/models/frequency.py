"""
freqency.py: contains data relevant to freqencies.txt
"""

import sqlalchemy as sa

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError, InvalidValueError

ENUM_EXACT_TIMES = [
    "Frequency-based",
    "Schedule-based"
]

class Frequency():
    """
    Frequency: class for freqencies
    """
    def __init__(self):
        self.trip_id = None
        self.start_time = None
        self.end_time = None
        self.headway_secs = None
        self.exact_times = 0

    @staticmethod
    def create_table(meta):
        """
        Create the SQLAlchemy table
        """
        return sa.Table(
            'frequencies', meta,
            sa.Column('trip_id', sa.String(length=255), sa.ForeignKey("trips.trip_id")),
            sa.Column('start_time', sa.String(length=255)),
            sa.Column('end_time', sa.String(length=255)),
            sa.Column('headway_secs', sa.Integer()),
            sa.Column('exact_times', sa.Integer())
        )

    @staticmethod
    def from_dict(data):
        """
        Creates a Frequency from a dict. Checks correctness after
        creation.

        Arguments:
        data: dict containing the data
        """
        ret = Frequency()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        """
        Creates an Frequency from a list of keys and a list of
        corresponding values. Checks correctness after creation

        Arguments:
        keys: list of keys (strings)
        data: list of values (strings)
        """
        ret = Frequency()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret

    def verify(self):
        """
        Verify that the Frequency has at least the required keys, lat and lon are correct
        """
        # TODO: verify trip_id
        if self.trip_id is None:
            raise MissingKeyError("trip_id")
        if self.start_time is None:
            raise MissingKeyError("start_time")
        if self.end_time is None:
            raise MissingKeyError("end_time")
        if self.headway_secs is None:
            raise MissingKeyError("headway_secs")

        if self.headway_secs < 0:
            raise InvalidValueError("headway_secs")

        if self.exact_times < 0 or self.exact_times >= len(ENUM_EXACT_TIMES):
            raise InvalidValueError("exact_times")

        return True

    def setkey(self, key, value):
        """
        Sets a class attribute depending on `key`, raising
        InvalidKeyError if the key does not belong on freqency

        Arguments:
        key, value: the key and value
        """
        if value == "":
            return

        if key == "trip_id":
            self.trip_id = value
        elif key == "start_time":
            self.start_time = value
        elif key == "end_time":
            self.end_time = value
        elif key == "headway_secs":
            self.headway_secs = int(value)
        elif key == "exact_times":
            self.exact_times = int(value)
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[Frequency {self.trip_id}]"

    def __eq__(self, other):
        if not isinstance(other, Frequency):
            return False
        return (
            self.trip_id == other.trip_id and
            self.start_time == other.start_time and
            self.end_time == other.end_time and
            self.headway_secs == other.headway_secs and
            self.exact_times == other.exact_times
        )
