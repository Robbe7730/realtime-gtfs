"""
translation.py: contains data relevant to translations.txt
"""

import sqlalchemy as sa

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError, InvalidValueError

ENUM_TABLE_NAME = [
    "agency",
    "stops",
    "routes",
    "trips",
    "stop_times",
    "feed_info"
]

class Translation():
    """
    Translation: class for translations
    """
    def __init__(self):
        self.table_name = None
        self.field_name = None
        self.language = None
        self.translation = None
        self.record_id = None
        self.record_sub_id = None
        self.field_value = None

    @staticmethod
    def create_table(meta):
        """
        Create the SQLAlchemy table
        """
        return sa.Table(
            'translations', meta,
            sa.Column('table_name', sa.Integer(), nullable=False),
            sa.Column('field_name', sa.String(length=255), nullable=False),
            sa.Column('language', sa.String(length=255), nullable=False),
            sa.Column('translation', sa.String(length=255), nullable=False),
            sa.Column('record_id', sa.String(length=255)),
            sa.Column('record_sub_id', sa.Integer()),
            sa.Column('field_value', sa.String(length=255))
        )

    @staticmethod
    def from_dict(data):
        """
        Creates a Translation from a dict. Checks correctness after
        creation.

        Arguments:
        data: dict containing the data
        """
        ret = Translation()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        """
        Creates an Translation from a list of keys and a list of
        corresponding values. Checks correctness after creation

        Arguments:
        keys: list of keys (strings)
        data: list of values (strings)
        """
        ret = Translation()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret

    def verify(self):
        """
        Verify that the Translation has at least the required keys, lat and lon are correct
        """
        # TODO: verify languages
        if self.table_name is None:
            raise MissingKeyError("table_name")
        if self.field_name is None:
            raise MissingKeyError("field_name")
        if self.language is None:
            raise MissingKeyError("language")
        if self.translation is None:
            raise MissingKeyError("translation")

        if self.table_name not in ENUM_TABLE_NAME:
            raise InvalidValueError("table_name")

        if self.record_id is not None and self.table_name == "feed_info":
            raise InvalidValueError("record_id: forbidden for feed_info")
        if self.record_id is not None and self.field_value is not None:
            raise InvalidValueError("record_id: forbidden if field_value is set")
        if self.record_id is None and self.field_value is None:
            raise MissingKeyError("record_id: required if field_value is not set")

        if self.record_sub_id is None and (self.table_name == "stop_times"
                                           and self.record_id is not None):
            raise MissingKeyError("record_sub_id: required if"
                                  " table_name equals stop_times and record_id is set")
        if (self.record_sub_id is not None and
                self.table_name != "stop_times"):
            raise InvalidValueError("record_sub_id: only allowed for stop_times")

        if self.field_value is not None and self.table_name == "feed_info":
            raise InvalidValueError("field_value: forbidden for feed_info")

        return True

    def setkey(self, key, value):
        """
        Sets a class attribute depending on `key`, raising
        InvalidKeyError if the key does not belong on translation

        Arguments:
        key, value: the key and value
        """
        if value == "":
            return

        if key == "table_name":
            self.table_name = value
        elif key == "field_name":
            self.field_name = value
        elif key == "language":
            self.language = value
        elif key == "translation":
            self.translation = value
        elif key == "record_id":
            self.record_id = value
        elif key == "record_sub_id":
            self.record_sub_id = value
        elif key == "field_value":
            self.field_value = value
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[Translation {self.field_name} ({self.language})]"

    def __eq__(self, other):
        if not isinstance(other, Translation):
            return False
        return (
            self.table_name == other.table_name and
            self.field_name == other.field_name and
            self.language == other.language and
            self.translation == other.translation and
            self.record_id == other.record_id and
            self.record_sub_id == other.record_sub_id and
            self.field_value == other.field_value
        )
