"""
level.py: contains data relevant to levels.txt
"""

import sqlalchemy as sa

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError

class Level():
    """
    Level: class for levels
    """
    def __init__(self):
        self.level_id = None
        self.level_index = None
        self.level_name = None

    @staticmethod
    def create_table(meta):
        """
        Create the SQLAlchemy table
        """
        sa.Table(
            'levels', meta,
            sa.Column('level_id', sa.String(length=255), primary_key=True),
            sa.Column('level_index', sa.Float(), nullable=False),
            sa.Column('level_name', sa.String(length=255))
        )

    @staticmethod
    def from_dict(data):
        """
        Creates a Level from a dict. Checks correctness after
        creation.

        Arguments:
        data: dict containing the data
        """
        ret = Level()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        """
        Creates an Level from a list of keys and a list of
        corresponding values. Checks correctness after creation

        Arguments:
        keys: list of keys (strings)
        data: list of values (strings)
        """
        ret = Level()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret

    def verify(self):
        """
        Verify that the Level has at least the required keys, lat and lon are correct
        """
        # TODO: verify level_id
        if self.level_id is None:
            raise MissingKeyError("level_id")
        if self.level_index is None:
            raise MissingKeyError("level_index")

        return True

    def setkey(self, key, value):
        """
        Sets a class attribute depending on `key`, raising
        InvalidKeyError if the key does not belong on level

        Arguments:
        key, value: the key and value
        """
        if value == "":
            return
        if key == "level_id":
            self.level_id = value
        elif key == "level_index":
            self.level_index = float(value)
        elif key == "level_name":
            self.level_name = value
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[Level {self.level_id}]"

    def __eq__(self, other):
        if not isinstance(other, Level):
            return False
        return (
            self.level_id == other.level_id and
            self.level_name == other.level_name and
            self.level_index == other.level_index
        )
