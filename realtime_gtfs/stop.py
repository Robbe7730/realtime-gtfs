"""
stop.py: contains data relevant to stop.txt
"""

import pytz

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError


ENUM_LOCATION_TYPE = [
    "Stop/Platform",
    "Station",
    "Entrance/Exit",
    "Generic Node",
    "Boarding Area"
]
ENUM_WHEELCHAIR_BOARDING = [
    "No accessibility information",
    "Some wheelchair accessibility",
    "No wheelchair accessibility"
]

class Stop():
    """
    stop: class for stops
    """
    def __init__(self):
        self.stop_id = None
        self.stop_code = None
        self.stop_name = None
        self.stop_desc = None
        self.stop_lat = None
        self.stop_lon = None
        self.zone_id = None
        self.stop_url = None
        self.location_type = 0
        self.parent_station = None
        self.stop_timezone = None
        self.wheelchair_boarding = 0
        self.level_id = None
        self.platform_code = None

    @staticmethod
    def from_dict(data):
        """
        Creates a Stop from a dict. Checks correctness after
        creation.

        Arguments:
        data: dict containing the data
        """
        ret = Stop()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        """
        Creates an Stop from a list of keys and a list of
        corresponding values. Checks correctness after creation

        Arguments:
        keys: list of keys (strings)
        data: list of values (strings)
        """
        ret = Stop()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret

    def verify(self):
        """
        Verify that the Stop has at least the required keys, lat and lon are correct
        """
        # TODO: verify zone_id, level_id, parent_station
        if self.stop_id is None:
            raise MissingKeyError("stop_id")
        if self.location_type <= 2:
            if self.stop_name is None:
                raise MissingKeyError("stop_name")
            if self.stop_lat is None:
                raise MissingKeyError("stop_lat")
            if self.stop_lon is None:
                raise MissingKeyError("stop_lon")
        if self.parent_station is None and self.location_type >= 2:
            raise MissingKeyError("parent_station")
        if (self.parent_station is not None and
                self.parent_station != "" and
                self.location_type == 1):
            raise InvalidKeyError("parent_station")

        if self.stop_lon < -180 or self.stop_lon > 180:
            raise InvalidKeyError("stop_lon")
        if self.stop_lat < -90 or self.stop_lat > 90:
            raise InvalidKeyError("stop_lat")
        if self.location_type < 0 or self.location_type >= len(ENUM_LOCATION_TYPE):
            raise InvalidKeyError("location_type")
        if (self.wheelchair_boarding < 0 or
                self.wheelchair_boarding >= len(ENUM_WHEELCHAIR_BOARDING)):
            raise InvalidKeyError("wheelchair_boarding")

        return True

    def setkey(self, key, value):
        """
        Sets a class attribute depending on `key`, raising
        InvalidKeyError if the key does not belong on stop

        Arguments:
        key, value: the key and value
        """
        if key == "stop_id":
            self.stop_id = value
        elif key == "stop_code":
            self.stop_code = value
        elif key == "stop_name":
            self.stop_name = value
        elif key == "stop_desc":
            self.stop_desc = value
        elif key == "stop_lat":
            self.stop_lat = float(value)
        elif key == "stop_lon":
            self.stop_lon = float(value)
        elif key == "zone_id":
            self.zone_id = value
        elif key == "stop_url":
            self.stop_url = value
        elif key == "location_type":
            self.location_type = int(value)
        elif key == "parent_station":
            self.parent_station = value
        elif key == "stop_timezone":
            self.stop_timezone = pytz.timezone(value)
        elif key == "wheelchair_boarding":
            self.wheelchair_boarding = int(value)
        elif key == "level_id":
            self.level_id = value
        elif key == "platform_code":
            self.platform_code = value
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[Stop {self.stop_name}]"

    def __eq__(self, other):
        if not isinstance(other, Stop):
            return False
        return (
            self.stop_id == other.stop_id and
            self.stop_code == other.stop_code and
            self.stop_name == other.stop_name and
            self.stop_desc == other.stop_desc and
            self.stop_lat == other.stop_lat and
            self.stop_lon == other.stop_lon and
            self.zone_id == other.zone_id and
            self.stop_url == other.stop_url and
            self.location_type == other.location_type and
            self.parent_station == other.parent_station and
            self.stop_timezone == other.stop_timezone and
            self.wheelchair_boarding == other.wheelchair_boarding and
            self.level_id == other.level_id and
            self.platform_code == other.platform_code
        )
