"""
transfer.py: contains data relevant to transfers.txt
"""

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError, InvalidValueError

ENUM_TRANSFER_TYPE = [
    "Recomended transfer",
    "Timed transfer, waiting",
    "Timed transfer, not waiting",
    "No transfer possible"
]

class Transfer():
    """
    Transfer: class for transfers
    """
    def __init__(self):
        self.from_stop_id = None
        self.to_stop_id = None
        self.transfer_type = 0
        self.min_transfer_time = None

    @staticmethod
    def from_dict(data):
        """
        Creates a Transfer from a dict. Checks correctness after
        creation.

        Arguments:
        data: dict containing the data
        """
        ret = Transfer()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        """
        Creates an Transfer from a list of keys and a list of
        corresponding values. Checks correctness after creation

        Arguments:
        keys: list of keys (strings)
        data: list of values (strings)
        """
        ret = Transfer()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret

    def verify(self):
        """
        Verify that the Transfer has at least the required keys, lat and lon are correct
        """
        # TODO: verify from_stop_id and to_stop_id
        if self.from_stop_id is None:
            raise MissingKeyError("from_stop_id")
        if self.to_stop_id is None:
            raise MissingKeyError("to_stop_id")

        if self.min_transfer_time is not None and self.min_transfer_time < 0:
            raise InvalidValueError("min_transfer_time")

        if self.transfer_type < 0 or self.transfer_type >= len(ENUM_TRANSFER_TYPE):
            raise InvalidValueError("transfer_type")

        return True

    def setkey(self, key, value):
        """
        Sets a class attribute depending on `key`, raising
        InvalidKeyError if the key does not belong on transfer

        Arguments:
        key, value: the key and value
        """
        if value == "":
            return

        if key == "from_stop_id":
            self.from_stop_id = value
        elif key == "to_stop_id":
            self.to_stop_id = value
        elif key == "transfer_type":
            self.transfer_type = int(value)
        elif key == "min_transfer_time":
            self.min_transfer_time = int(value)
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[Transfer {self.from_stop_id} - {self.to_stop_id}]"

    def __eq__(self, other):
        if not isinstance(other, Transfer):
            return False
        return (
            self.from_stop_id == other.from_stop_id and
            self.to_stop_id == other.to_stop_id and
            self.transfer_type == other.transfer_type and
            self.min_transfer_time == other.min_transfer_time
        )
