"""
fare_rule.py: contains data relevant to fare_rules.txt
"""

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError

class FareRule():
    """
    FareRule: class for fare_rules
    """
    def __init__(self):
        self.fare_id = None
        self.route_id = None
        self.origin_id = None
        self.destination_id = None
        self.contains_id = None

    @staticmethod
    def from_dict(data):
        """
        Creates a FareRule from a dict. Checks correctness after
        creation.

        Arguments:
        data: dict containing the data
        """
        ret = FareRule()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        """
        Creates an FareRule from a list of keys and a list of
        corresponding values. Checks correctness after creation

        Arguments:
        keys: list of keys (strings)
        data: list of values (strings)
        """
        ret = FareRule()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret

    def verify(self):
        """
        Verify that the FareRule has at least the required keys, lat and lon are correct
        """
        # TODO: verify all ids
        if self.fare_id is None:
            raise MissingKeyError("fare_id")

        return True

    def setkey(self, key, value):
        """
        Sets a class attribute depending on `key`, raising
        InvalidKeyError if the key does not belong on fare_rule

        Arguments:
        key, value: the key and value
        """
        if value == "":
            return

        if key == "fare_id":
            self.fare_id = value
        elif key == "route_id":
            self.route_id = value
        elif key == "origin_id":
            self.origin_id = value
        elif key == "destination_id":
            self.destination_id = value
        elif key == "contains_id":
            self.contains_id = value
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[FareRule {self.fare_id}]"

    def __eq__(self, other):
        if not isinstance(other, FareRule):
            return False
        return (
            self.fare_id == other.fare_id and
            self.route_id == other.route_id and
            self.origin_id == other.origin_id and
            self.destination_id == other.destination_id and
            self.contains_id == other.contains_id
        )
