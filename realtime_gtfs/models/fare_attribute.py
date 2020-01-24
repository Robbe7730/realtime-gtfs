"""
fare_attribute.py: contains data relevant to fare_attributes.txt
"""

import sqlalchemy as sa

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError, InvalidValueError

ENUM_PAYMENT_METHOD = [
    "Payed on board",
    "Pay before boarding"
]

class FareAttribute():
    """
    FareAttribute: class for fare_attributes
    """
    def __init__(self):
        self.fare_id = None
        self.price = None
        self.currency_type = None
        self.payment_method = None
        self.transfers = None
        self.agency_id = None
        self.transfer_duration = None

    @staticmethod
    def create_table(meta):
        """
        Create the SQLAlchemy table
        """
        sa.Table(
            'fare_attributes', meta,
            sa.Column('fare_id', sa.String(length=255), primary_key=True),
            sa.Column('price', sa.Float(), nullable=False),
            sa.Column('currency_type', sa.String(length=3), nullable=False),
            sa.Column('payment_method', sa.Integer(), nullable=False),
            sa.Column('transfers', sa.Integer(), nullable=False),
            sa.Column('agency_id', sa.String(length=255), sa.ForeignKey("agencies.agency_id")),
            sa.Column('transfer_duration', sa.String(length=255))
        )

    @staticmethod
    def from_dict(data):
        """
        Creates a FareAttribute from a dict. Checks correctness after
        creation.

        Arguments:
        data: dict containing the data
        """
        ret = FareAttribute()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        """
        Creates an FareAttribute from a list of keys and a list of
        corresponding values. Checks correctness after creation

        Arguments:
        keys: list of keys (strings)
        data: list of values (strings)
        """
        ret = FareAttribute()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret

    def verify(self):
        """
        Verify that the FareAttribute has at least the required keys, lat and lon are correct
        """
        # TODO: verify fare_id and agency_id
        if self.fare_id is None:
            raise MissingKeyError("fare_id")
        if self.price is None:
            raise MissingKeyError("price")
        if self.currency_type is None:
            raise MissingKeyError("currency_type")
        if self.payment_method is None:
            raise MissingKeyError("payment_method")

        if self.price < 0:
            raise InvalidValueError("price")

        if self.payment_method < 0 or self.payment_method >= len(ENUM_PAYMENT_METHOD):
            raise InvalidValueError("payment_method")

        if self.transfers is not None and (self.transfers < 0 or self.transfers > 5):
            raise InvalidValueError("transfers")

        if self.transfer_duration is not None and self.transfer_duration < 0:
            raise InvalidValueError("transfer_duration")

        return True

    def setkey(self, key, value):
        """
        Sets a class attribute depending on `key`, raising
        InvalidKeyError if the key does not belong on fare_attribute

        Arguments:
        key, value: the key and value
        """
        if value == "":
            return

        if key == "fare_id":
            self.fare_id = value
        elif key == "price":
            self.price = float(value)
        elif key == "currency_type":
            self.currency_type = value
        elif key == "payment_method":
            self.payment_method = int(value)
        elif key == "transfers":
            self.transfers = int(value)
        elif key == "agency_id":
            self.agency_id = value
        elif key == "transfer_duration":
            self.transfer_duration = int(value)
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[FareAttribute {self.fare_id}]"

    def __eq__(self, other):
        if not isinstance(other, FareAttribute):
            return False
        return (
            self.fare_id == other.fare_id and
            self.price == other.price and
            self.currency_type == other.currency_type and
            self.payment_method == other.payment_method and
            self.transfers == other.transfers and
            self.agency_id == other.agency_id and
            self.transfer_duration == other.transfer_duration
        )
