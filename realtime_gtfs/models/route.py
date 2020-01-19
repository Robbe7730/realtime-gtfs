"""
route.py: contains data relevant to routes.txt
"""

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError, InvalidValueError


ENUM_ROUTE_TYPE = {
    0: "Tram, Streetcar, Light rail",
    1: "Subway, Metro",
    2: "Rail",
    3: "Bus",
    4: "Ferry",
    5: "Cable car",
    6: "Gondola",
    7: "Funicular",
    100: "Railway Service",
    101: "High Speed Rail Service",
    102: "Long Distance Trains",
    103: "Inter Regional Rail Service",
    104: "Car Transport Rail Service",
    105: "Sleeper Rail Service",
    106: "Regional Rail Service",
    107: "Tourist Railway Service",
    108: "Rail Shuttle (Within Complex)",
    109: "Suburban Railway",
    110: "Replacement Rail Service",
    111: "Special Rail Service",
    112: "Lorry Transport Rail Service",
    113: "All Rail Services",
    114: "Cross-Country Rail Service",
    115: "Vehicle Transport Rail Service",
    116: "Rack and Pinion Railway",
    117: "Additional Rail Service",
    200: "Coach Service",
    201: "International Coach Service",
    202: "National Coach Service",
    203: "Shuttle Coach Service",
    204: "Regional Coach Service",
    205: "Special Coach Service",
    206: "Sightseeing Coach Service",
    207: "Tourist Coach Service",
    208: "Commuter Coach Service",
    209: "All Coach Services",
    400: "Urban Railway Service",
    401: "Metro Service",
    402: "Underground Service",
    403: "Urban Railway Service",
    404: "All Urban Railway Services",
    405: "Monorail",
    700: "Bus Service",
    701: "Regional Bus Service",
    702: "Express Bus Service",
    703: "Stopping Bus Service",
    704: "Local Bus Service",
    705: "Night Bus Service",
    706: "Post Bus Service",
    707: "Special Needs Bus",
    708: "Mobility Bus Service",
    709: "Mobility Bus for Registered Disabled",
    710: "Sightseeing Bus",
    711: "Shuttle Bus",
    712: "School Bus",
    713: "School and Public Service Bus",
    714: "Rail Replacement Bus Service",
    715: "Demand and Response Bus Service",
    716: "All Bus Services",
    717: "Share Taxi Service",
    800: "Trolleybus Service",
    900: "Tram Service",
    901: "City Tram Service",
    902: "Local Tram Service",
    903: "Regional Tram Service",
    904: "Sightseeing Tram Service",
    905: "Shuttle Tram Service",
    906: "All Tram Services",
    907: "Cable Tram",
    1000: "Water Transport Service",
    1100: "Air Service",
    1200: "Ferry Service",
    1300: "Aerial Lift Service",
    1400: "Funicular Service",
    1500: "Taxi Service",
    1501: "Communal Taxi Service",
    1502: "Water Taxi Service",
    1503: "Rail Taxi Service",
    1504: "Bike Taxi Service",
    1505: "Licensed Taxi Service",
    1506: "Private Hire Service Vehicle",
    1507: "All Taxi Services",
    1700: "Miscellaneous Service",
}

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

        if self.route_type not in ENUM_ROUTE_TYPE:
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
