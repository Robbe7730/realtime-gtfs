"""
feed_info.py: contains data relevant to feed_info.txt
"""

import sqlalchemy as sa

from realtime_gtfs.exceptions import InvalidKeyError, MissingKeyError


class FeedInfo():
    """
    FeedInfo: class for feed info
    """
    def __init__(self):
        self.feed_publisher_name = None
        self.feed_publisher_url = None
        self.feed_lang = None
        self.feed_start_date = None
        self.feed_end_date = None
        self.feed_version = None
        self.feed_contact_email = None
        self.feed_contact_url = None
        self.default_lang = None

    @staticmethod
    def create_table(meta):
        """
        Create the SQLAlchemy table
        """
        sa.Table(
            'feed_info', meta,
            sa.Column('feed_publisher_name', sa.String(length=255), nullable=False),
            sa.Column('feed_publisher_url', sa.String(length=255), nullable=False),
            sa.Column('feed_lang', sa.String(length=255), nullable=False),
            sa.Column('feed_start_date', sa.String(length=255)),
            sa.Column('feed_end_date', sa.String(length=255)),
            sa.Column('feed_version', sa.String(length=255)),
            sa.Column('feed_contact_email', sa.String(length=255)),
            sa.Column('feed_contact_url', sa.String(length=255)),
            sa.Column('default_lang', sa.String(length=255)),
        )

    @staticmethod
    def from_dict(data):
        """
        Creates an FeedInfo from a dict. Checks correctness after
        creation.

        Arguments:
        data: dict containing the data
        """
        ret = FeedInfo()
        for key, value in data.items():
            ret.setkey(key, value)
        ret.verify()
        return ret

    @staticmethod
    def from_gtfs(keys, data):
        """
        Creates an FeedInfo from a list of keys and a list of
        corresponding values. Checks correctness after creation

        Arguments:
        keys: list of keys (strings)
        data: list of values (strings)
        """
        ret = FeedInfo()
        for key, value in zip(keys, data):
            ret.setkey(key, value)
        ret.verify()
        return ret

    def verify(self):
        """
        Verify that the FeedInfo has at least the required keys
        """
        # TODO: verify feed_lang, feed_start_date, feed_end_date, default_lang
        if self.feed_publisher_name is None:
            raise MissingKeyError("feed_publisher_name")
        if self.feed_publisher_url is None:
            raise MissingKeyError("feed_publisher_url")
        if self.feed_lang is None:
            raise MissingKeyError("feed_lang")
        return True

    def setkey(self, key, value):
        """
        Sets a class attribute depending on `key`, raising
        InvalidKeyError if the key does not belong on FeedInfo

        Arguments:
        key, value: the key and value
        """
        if value == "":
            return
        if key == "feed_publisher_name":
            self.feed_publisher_name = value
        elif key == "feed_publisher_url":
            self.feed_publisher_url = value
        elif key == "feed_lang":
            self.feed_lang = value
        elif key == "feed_start_date":
            self.feed_start_date = value
        elif key == "feed_end_date":
            self.feed_end_date = value
        elif key == "feed_version":
            self.feed_version = value
        elif key == "feed_contact_email":
            self.feed_contact_email = value
        elif key == "feed_contact_url":
            self.feed_contact_url = value
        elif key == "default_lang":
            self.default_lang = value
        else:
            raise InvalidKeyError(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[FeedInfo {self.feed_publisher_name}]"

    def __eq__(self, other):
        if not isinstance(other, FeedInfo):
            return False
        return (
            self.feed_publisher_name == other.feed_publisher_name and
            self.feed_publisher_url == other.feed_publisher_url and
            self.feed_lang == other.feed_lang and
            self.feed_start_date == other.feed_start_date and
            self.feed_end_date == other.feed_end_date and
            self.feed_version == other.feed_version and
            self.feed_contact_email == other.feed_contact_email and
            self.feed_contact_url == other.feed_contact_url and
            self.default_lang == other.default_lang
        )
