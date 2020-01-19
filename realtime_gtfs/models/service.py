"""
calendar.py: contains data relevant to calendar.txt
"""

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError, InvalidValueError

ENUM_AVAILABLE = [
    "Available",
    "Not available"
]

class Service():
    """
    Service: class for a calendar entry
    """
    def __init__(self):
        self.service_id = None
        self.monday = None
        self.tuesday = None
        self.wednesday = None
        self.thursday = None
        self.friday = None
        self.saturday = None
        self.sunday = None
        self.start_date = None
        self.end_date = None

    @staticmethod
    def from_dict(data):
        """
        Creates an Service from a dict. Checks correctness after
        creation.

        Arguments:
        data: dict containing the data
        """
        ret = Service()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        """
        Creates an Service from a list of keys and a list of
        corresponding values. Checks correctness after creation

        Arguments:
        keys: list of keys (strings)
        data: list of values (strings)
        """
        ret = Service()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret

    def verify(self):
        """
        Verify that the Service has at least the required keys and correct values
        """
        if self.service_id is None:
            raise MissingKeyError("service_id")
        if self.monday is None:
            raise MissingKeyError("monday")
        if self.tuesday is None:
            raise MissingKeyError("tuesday")
        if self.wednesday is None:
            raise MissingKeyError("wednesday")
        if self.thursday is None:
            raise MissingKeyError("thursday")
        if self.friday is None:
            raise MissingKeyError("friday")
        if self.saturday is None:
            raise MissingKeyError("saturday")
        if self.sunday is None:
            raise MissingKeyError("sunday")
        if self.start_date is None:
            raise MissingKeyError("start_date")
        if self.end_date is None:
            raise MissingKeyError("end_date")

        if self.monday < 0 or self.monday >= len(ENUM_AVAILABLE):
            raise InvalidValueError("monday")
        if self.tuesday < 0 or self.tuesday >= len(ENUM_AVAILABLE):
            raise InvalidValueError("tuesday")
        if self.wednesday < 0 or self.wednesday >= len(ENUM_AVAILABLE):
            raise InvalidValueError("wednesday")
        if self.thursday < 0 or self.thursday >= len(ENUM_AVAILABLE):
            raise InvalidValueError("thursday")
        if self.friday < 0 or self.friday >= len(ENUM_AVAILABLE):
            raise InvalidValueError("friday")
        if self.saturday < 0 or self.saturday >= len(ENUM_AVAILABLE):
            raise InvalidValueError("saturday")
        if self.sunday < 0 or self.sunday >= len(ENUM_AVAILABLE):
            raise InvalidValueError("sunday")

        return True

    def setkey(self, key, value):
        """
        Sets a class attribute depending on `key`, raising
        InvalidKeyError if the key does not belong on Service

        Arguments:
        key, value: the key and value
        """
        if value == "":
            return

        if key == "service_id":
            self.service_id = value
        elif key == "monday":
            self.monday = int(value)
        elif key == "tuesday":
            self.tuesday = int(value)
        elif key == "wednesday":
            self.wednesday = int(value)
        elif key == "thursday":
            self.thursday = int(value)
        elif key == "friday":
            self.friday = int(value)
        elif key == "saturday":
            self.saturday = int(value)
        elif key == "sunday":
            self.sunday = int(value)
        elif key == "start_date":
            self.start_date = value
        elif key == "end_date":
            self.end_date = value
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[Service {self.service_id}]"

    def __eq__(self, other):
        if not isinstance(other, Service):
            return False
        return (
            self.service_id == other.service_id and
            self.monday == other.monday and
            self.tuesday == other.tuesday and
            self.wednesday == other.wednesday and
            self.thursday == other.thursday and
            self.friday == other.friday and
            self.saturday == other.saturday and
            self.sunday == other.sunday and
            self.start_date == other.start_date and
            self.end_date == other.end_date
        )
