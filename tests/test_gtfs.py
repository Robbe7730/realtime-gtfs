"""
test_gtfs.py: contains tests for realtime_gtfs/gtfs.py
"""

import zipfile
import pytest

from realtime_gtfs import GTFS
from realtime_gtfs.exceptions import InvalidURLError

# TODO: read from config file
GTFS_URL = "https://sncb-opendata.hafas.de/gtfs/static/c21ac6758dd25af84cca5b707f3cb3de"
MYSQL_URL = "mysql://delaymap:Treinen@localhost:3306/DelayMap"
SQLITE_URL = "sqlite:///:memory:"

ZIP_FILE = zipfile.ZipFile("./tests/static/sample-feed.zip")

@pytest.mark.xfail
@pytest.mark.integration
def test_from_zip_mysql():
    """
    test_from_url_mysql: test if creation of GTFS works with
    MySQL database, expected to fail if no mysql database with the
    given parameters exists.
    """
    test_gtfs = GTFS()
    test_gtfs.from_zip(ZIP_FILE)
    test_gtfs.write_to_db(MYSQL_URL)

@pytest.mark.integration
def test_from_zip_sqlite():
    """
    test_from_url_sqlite: test if creation of GTFS works with
    in-memory SQLite database.
    """
    test_gtfs = GTFS()
    test_gtfs.from_zip(ZIP_FILE)
    test_gtfs.write_to_db(SQLITE_URL)

@pytest.mark.slow
@pytest.mark.integration
def test_from_url():
    """
    test_from_url: test if creation of GTFS works from a URL
    """
    test_gtfs = GTFS()
    test_gtfs.from_url(GTFS_URL)

@pytest.mark.integration
def test_from_zip():
    """
    test_from_zip: test if creation of GTFS works from a zip
    """
    test_gtfs = GTFS()
    test_gtfs.from_zip(ZIP_FILE)

@pytest.mark.integration
def test_invalid_url():
    """
    test_invalid_url: test if it fails when given an invalid URL
    """
    test_gtfs = GTFS()
    with pytest.raises(InvalidURLError):
        test_gtfs.from_url("https://robbevanherck.be/nosuch.zip")
