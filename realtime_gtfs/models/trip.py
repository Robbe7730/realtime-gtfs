"""
trip.py: contains data relevant to trips.txt
"""

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError, InvalidValueError

ENUM_DIRECTION_ID = [
    "One Direction",
    "Opposite Direction"
]

ENUM_WHEELCHAIR_ACCESSIBLE = [
    "No accessibility information",
    "Some wheelchair accessibility",
    "No wheelchair accessibility"
]

ENUM_BIKES_ALLOWED = [
    "No bike infomation",
    "Bikes allowed",
    "No bikes allowed"
]

ENUM_EXCEPTIONAL = [
    "Regular Schedule",
    "Exception"
]

class Trip():
    """
    Trip: class for trips
    """
    def __init__(self):
        self.route_id = None
        self.service_id = None
        self.trip_id = None
        self.trip_headsign = None
        self.trip_short_name = None
        self.direction_id = 0
        self.block_id = None
        self.shape_id = None
        self.wheelchair_accessible = 0
        self.bikes_allowed = 0
        self.exceptional = None

    @staticmethod
    def from_dict(data):
        """
        Creates a Trip from a dict. Checks correctness after
        creation.

        Arguments:
        data: dict containing the data
        """
        ret = Trip()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        """
        Creates an Trip from a list of keys and a list of
        corresponding values. Checks correctness after creation

        Arguments:
        keys: list of keys (strings)
        data: list of values (strings)
        """
        ret = Trip()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret

    def verify(self):
        """
        Verify that the Route has at least the required keys and correct values
        """
        # TODO: verify route_id, service_id, block_id, shape_id

        if self.route_id is None:
            raise MissingKeyError("route_id")

        if self.service_id is None:
            raise MissingKeyError("service_id")

        if self.trip_id is None:
            raise MissingKeyError("trip_id")

        if self.direction_id < 0 or self.direction_id >= len(ENUM_DIRECTION_ID):
            raise InvalidValueError("direction_id")

        if (self.wheelchair_accessible < 0 or
                self.wheelchair_accessible >= len(ENUM_WHEELCHAIR_ACCESSIBLE)):
            raise InvalidValueError("wheelchair_accessible")

        if self.bikes_allowed < 0 or self.bikes_allowed >= len(ENUM_BIKES_ALLOWED):
            raise InvalidValueError("bikes_allowed")

        if self.exceptional is not None and (self.exceptional < 0 or
                                             self.exceptional >= len(ENUM_EXCEPTIONAL)):
            raise InvalidValueError("exceptional")

        return True

    def setkey(self, key, value):
        """
        Sets a class attribute depending on `key`, raising
        InvalidKeyError if the key does not belong on trip

        Arguments:
        key, value: the key and value
        """
        if value == "":
            return

        if key == "route_id":
            self.route_id = value
        elif key == "service_id":
            self.service_id = value
        elif key == "trip_id":
            self.trip_id = value
        elif key == "trip_headsign":
            self.trip_headsign = value
        elif key == "trip_short_name":
            self.trip_short_name = value
        elif key == "direction_id":
            self.direction_id = int(value)
        elif key == "block_id":
            self.block_id = value
        elif key == "shape_id":
            self.shape_id = value
        elif key == "wheelchair_accessible":
            self.wheelchair_accessible = int(value)
        elif key == "bikes_allowed":
            self.bikes_allowed = int(value)
        elif key == "exceptional":
            self.exceptional = int(value)
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[Trip {self.trip_id}]"

    def __eq__(self, other):
        if not isinstance(other, Trip):
            return False
        return (
            self.route_id == other.route_id and
            self.service_id == other.service_id and
            self.trip_id == other.trip_id and
            self.trip_headsign == other.trip_headsign and
            self.trip_short_name == other.trip_short_name and
            self.direction_id == other.direction_id and
            self.block_id == other.block_id and
            self.shape_id == other.shape_id and
            self.wheelchair_accessible == other.wheelchair_accessible and
            self.bikes_allowed == other.bikes_allowed and
            self.exceptional == other.exceptional
        )
