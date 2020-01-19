"""
service_exception.py: contains data relevant to calendar_dates.txt
"""

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError, InvalidValueError

ENUM_EXCEPTION_TYPE = [
    None,
    "Added",
    "Removed"
]

class ServiceException():
    """
    ServiceException: class for a calendar_dates entry
    """
    def __init__(self):
        self.service_id = None
        self.date = None
        self.exception_type = None

    @staticmethod
    def from_dict(data):
        """
        Creates an ServiceException from a dict. Checks correctness after
        creation.

        Arguments:
        data: dict containing the data
        """
        ret = ServiceException()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        """
        Creates an ServiceException from a list of keys and a list of
        corresponding values. Checks correctness after creation

        Arguments:
        keys: list of keys (strings)
        data: list of values (strings)
        """
        ret = ServiceException()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret

    def verify(self):
        """
        Verify that the ServiceException has at least the required keys and correct values
        """
        if self.service_id is None:
            raise MissingKeyError("service_id")
        if self.date is None:
            raise MissingKeyError("date")
        if self.exception_type is None:
            raise MissingKeyError("exception_type")

        if self.exception_type < 1 or self.exception_type >= len(ENUM_EXCEPTION_TYPE):
            raise InvalidValueError("exception_type")

        return True

    def setkey(self, key, value):
        """
        Sets a class attribute depending on `key`, raising
        InvalidKeyError if the key does not belong on ServiceException

        Arguments:
        key, value: the key and value
        """
        if value == "":
            return

        if key == "service_id":
            self.service_id = value
        elif key == "date":
            self.date = value
        elif key == "exception_type":
            self.exception_type = int(value)
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[ServiceException {self.service_id}]"

    def __eq__(self, other):
        if not isinstance(other, ServiceException):
            return False
        return (
            self.service_id == other.service_id and
            self.date == other.date and
            self.exception_type == other.exception_type
        )
