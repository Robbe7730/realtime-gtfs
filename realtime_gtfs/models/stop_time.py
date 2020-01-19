"""
stop_time.py: contains data relevant to stop_times.txt
"""

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError, InvalidValueError

ENUM_PICKUP_TYPE = [
    "Regular pickup",
    "No pickup",
    "Must phone agency to arrange pickup",
    "Must contact driver to arrange pickup"
]

ENUM_DROP_OFF_TYPE = [
    "Regular drop off",
    "No drop off",
    "Must phone agency to arrange drop off",
    "Must contact driver to arrange drop off"
]

ENUM_TIMEPOINT_TYPE = [
    "Approximate times",
    "Exact times"
]

class StopTime():
    """
    stop_time: class for stop_times
    """
    def __init__(self):
        self.trip_id = None
        self.arrival_time = None
        self.departure_time = None
        self.stop_id = None
        self.stop_sequence = None
        self.stop_headsign = None
        self.pickup_type = 0
        self.drop_off_type = 0
        self.shape_dist_traveled = None
        self.timepoint = 1

    @staticmethod
    def from_dict(data):
        """
        Creates a StopTime from a dict. Checks correctness after
        creation.

        Arguments:
        data: dict containing the data
        """
        ret = StopTime()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        """
        Creates an StopTime from a list of keys and a list of
        corresponding values. Checks correctness after creation

        Arguments:
        keys: list of keys (strings)
        data: list of values (strings)
        """
        ret = StopTime()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret

    def verify(self):
        """
        Verify that the StopTime has at least the required keys, lat and lon are correct
        """
        # TODO: verify stop_id, trip_id, arrival_time and departure_time

        if self.trip_id is None:
            raise MissingKeyError("trip_id")

        if self.arrival_time is None and self.departure_time is None:
            raise MissingKeyError("arrival_time or departure_timee")

        if self.stop_id is None:
            raise MissingKeyError("stop_id")

        if self.stop_sequence is None:
            raise MissingKeyError("stop_sequence")

        if self.stop_sequence < 0:
            raise InvalidValueError("stop_sequence")

        if self.pickup_type < 0 or self.pickup_type >= len(ENUM_PICKUP_TYPE):
            raise InvalidValueError("pickup_type")

        if self.drop_off_type < 0 or self.drop_off_type >= len(ENUM_DROP_OFF_TYPE):
            raise InvalidValueError("drop_off_type")

        if self.shape_dist_traveled is not None and self.shape_dist_traveled < 0:
            raise InvalidValueError("shape_dist_traveled")

        if self.timepoint < 0 or self.timepoint >= len(ENUM_TIMEPOINT_TYPE):
            raise InvalidValueError("timepoint")

        return True

    def setkey(self, key, value):
        """
        Sets a class attribute depending on `key`, raising
        InvalidKeyError if the key does not belong on stop_time

        Arguments:
        key, value: the key and value
        """
        if value == "":
            return

        if key == "trip_id":
            self.trip_id = value
        elif key == "arrival_time":
            self.arrival_time = value
        elif key == "departure_time":
            self.departure_time = value
        elif key == "stop_id":
            self.stop_id = value
        elif key == "stop_sequence":
            self.stop_sequence = int(value)
        elif key == "stop_headsign":
            self.stop_headsign = value
        elif key == "pickup_type":
            self.pickup_type = int(value)
        elif key == "drop_off_type":
            self.drop_off_type = int(value)
        elif key == "shape_dist_traveled":
            self.shape_dist_traveled = float(value)
        elif key == "timepoint":
            self.timepoint = int(value)
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[StopTime {self.trip_id} #{self.stop_sequence}]"

    def __eq__(self, other):
        if not isinstance(other, StopTime):
            return False
        return (
            self.trip_id == other.trip_id and
            self.arrival_time == other.arrival_time and
            self.departure_time == other.departure_time and
            self.stop_id == other.stop_id and
            self.stop_sequence == other.stop_sequence and
            self.stop_headsign == other.stop_headsign and
            self.pickup_type == other.pickup_type and
            self.drop_off_type == other.drop_off_type and
            self.shape_dist_traveled == other.shape_dist_traveled and
            self.timepoint == other.timepoint
        )
