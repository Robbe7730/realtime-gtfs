"""
route.py: contains data relevant to routes.txt
"""

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError, InvalidValueError


ENUM_ROUTE_TYPE = [
    "Tram",
    "Subway",
    "Rail",
    "Bus",
    "Ferry",
    "Cable car",
    "Gondola",
    "Funicular"
]

class Route():
    """
    Route: class for routes
    """
    def __init__(self):
        self.route_id = None
        self.agency_id = None
        self.route_short_name = None
        self.route_long_name = None
        self.route_desc = None
        self.route_type = None
        self.route_url = None
        self.route_color = "FFFFFF"
        self.route_text_color = "000000"
        self.route_sort_order = 0

    @staticmethod
    def from_dict(data):
        """
        Creates a Route from a dict. Checks correctness after
        creation.

        Arguments:
        data: dict containing the data
        """
        ret = Route()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        """
        Creates an Route from a list of keys and a list of
        corresponding values. Checks correctness after creation

        Arguments:
        keys: list of keys (strings)
        data: list of values (strings)
        """
        ret = Route()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret

    def verify(self):
        """
        Verify that the Route has at least the required keys and correct values
        """
        # TODO: verify agency_id,
        if self.route_id is None:
            raise MissingKeyError("route_id")

        if self.route_type is None:
            raise MissingKeyError("route_type")

        if ((self.route_short_name == "" or self.route_short_name is None) and
                (self.route_long_name == "" or self.route_long_name is None)):
            raise MissingKeyError("route_long_name or route_short_name")

        if self.route_type < 0 or self.route_type >= len(ENUM_ROUTE_TYPE):
            print(self.route_type)
            raise InvalidValueError("route_type")

        if len(self.route_color) != 6:
            raise InvalidValueError("route_color")

        if len(self.route_text_color) != 6:
            raise InvalidValueError("route_text_color")

        try:
            int(self.route_color, 16)
        except ValueError:
            raise InvalidValueError("route_color")

        try:
            int(self.route_text_color, 16)
        except ValueError:
            raise InvalidValueError("route_text_color")

        if self.route_sort_order < 0:
            raise InvalidValueError("route_sort_order")

        return True

    def setkey(self, key, value):
        """
        Sets a class attribute depending on `key`, raising
        InvalidKeyError if the key does not belong on route

        Arguments:
        key, value: the key and value
        """
        if value == "":
            return
        if key == "route_id":
            self.route_id = value
        elif key == "agency_id":
            self.agency_id = value
        elif key == "route_short_name":
            self.route_short_name = value
        elif key == "route_long_name":
            self.route_long_name = value
        elif key == "route_desc":
            self.route_desc = value
        elif key == "route_type":
            self.route_type = int(value)
        elif key == "route_url":
            self.route_url = value
        elif key == "route_color":
            self.route_color = value
        elif key == "route_text_color":
            self.route_text_color = value
        elif key == "route_sort_order":
            self.route_sort_order = int(value)
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[Route {self.route_type}]"

    def __eq__(self, other):
        if not isinstance(other, Route):
            return False
        return (
            self.route_id == other.route_id and
            self.agency_id == other.agency_id and
            self.route_short_name == other.route_short_name and
            self.route_long_name == other.route_long_name and
            self.route_desc == other.route_desc and
            self.route_type == other.route_type and
            self.route_url == other.route_url and
            self.route_color == other.route_color and
            self.route_text_color == other.route_text_color and
            self.route_sort_order == other.route_sort_order
        )
