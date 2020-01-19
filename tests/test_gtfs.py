"""
test_gtfs.py: contains tests for realtime_gtfs/gtfs.py
"""

import pytest

from realtime_gtfs import gtfs

# TODO: read from config file
GTFS_URL = "https://sncb-opendata.hafas.de/gtfs/static/c21ac6758dd25af84cca5b707f3cb3de"
MYSQL_URL = "mysql://delaymap:Treinen@localhost:3306/DelayMap"
SQLITE_URL = "sqlite:///:memory:"

@pytest.mark.xfail
def test_gtfs_from_url_mysql():
    """
    test_gtfs_from_url_mysql: test if creation of GTFS works with
    MySQL database, expected to fail if no mysql database with the
    given parameters exists.
    """
    test_gtfs = gtfs.GTFS(MYSQL_URL)
    test_gtfs.from_url(GTFS_URL)

def test_gtfs_from_url_sqlite():
    """
    test_gtfs_from_url_sqlite: test if creation of GTFS works with
    in-memory SQLite database.
    """
    test_gtfs = gtfs.GTFS(SQLITE_URL)
    test_gtfs.from_url(GTFS_URL)
