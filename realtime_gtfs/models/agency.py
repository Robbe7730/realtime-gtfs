"""
agency.py: contains data relevant to agency.txt
"""

import pytz

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError


class Agency():
    """
    Agency: class for agencies
    """
    def __init__(self):
        self.agency_id = None
        self.agency_name = None
        self.agency_url = None
        self.agency_timezone = None
        self.agency_lang = None
        self.agency_phone = None
        self.agency_fare_url = None
        self.agency_email = None

    @staticmethod
    def from_dict(data):
        """
        Creates an Agency from a dict. Checks correctness after
        creation.

        Arguments:
        data: dict containing the data
        """
        ret = Agency()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        """
        Creates an Agency from a list of keys and a list of
        corresponding values. Checks correctness after creation

        Arguments:
        keys: list of keys (strings)
        data: list of values (strings)
        """
        ret = Agency()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret

    def verify(self):
        """
        Verify that the Agency has at least the required keys
        """
        # TODO: verify agency_id
        if self.agency_name is None:
            raise MissingKeyError("agency_name")
        if self.agency_url is None:
            raise MissingKeyError("agency_url")
        if self.agency_timezone is None:
            raise MissingKeyError("agency_timezone")
        return True

    def setkey(self, key, value):
        """
        Sets a class attribute depending on `key`, raising
        InvalidKeyError if the key does not belong on Agency

        Arguments:
        key, value: the key and value
        """
        if value == "":
            return
        if key == "agency_id":
            self.agency_id = value
        elif key == "agency_name":
            self.agency_name = value
        elif key == "agency_url":
            self.agency_url = value
        elif key == "agency_timezone":
            self.agency_timezone = pytz.timezone(value)
        elif key == "agency_lang":
            self.agency_lang = value
        elif key == "agency_phone":
            self.agency_phone = value
        elif key == "agency_fare_url":
            self.agency_fare_url = value
        elif key == "agency_email":
            self.agency_email = value
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[Agency {self.agency_name}]"

    def __eq__(self, other):
        if not isinstance(other, Agency):
            return False
        return (self.agency_id == other.agency_id and
                self.agency_name == other.agency_name and
                self.agency_url == other.agency_url and
                self.agency_timezone == other.agency_timezone and
                self.agency_phone == other.agency_phone and
                self.agency_lang == other.agency_lang and
                self.agency_fare_url == other.agency_fare_url and
                self.agency_email == other.agency_email)
