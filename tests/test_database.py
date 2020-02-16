"""
test_fare_rule.py: tests for realtime_gtfs/database.py
"""

import zipfile

from realtime_gtfs import DatabaseConnection, GTFS

ZIP_FILE = zipfile.ZipFile("./tests/static/sample-feed.zip")
SQLITE_URL = "sqlite:///:memory:"

ALL_TABLES = [
    "agencies",
    "fare_attributes",
    "routes",
    "stops",
    "fare_rules",
    "feed_infos",
    "frequencies",
    "levels",
    "pathways",
    "services",
    "shapes",
    "stop_times",
    "transfers",
    "translations",
    "trips",
]

def test_database_happyflow():
    """
    test_database_happyflow: test creation of the database connection with an in-memory database.
    """
    gtfs = GTFS()
    gtfs.from_zip(ZIP_FILE)
    dbcon = DatabaseConnection(SQLITE_URL)
    for table in ALL_TABLES:
        assert table in dbcon.tables
    dbcon.add_gtfs(gtfs)
    dbcon.reset()
