from realtime_gtfs import gtfs
import pytest

def test_gtfs_from_url_mysql():
    test_gtfs = gtfs.GTFS("mysql://delaymap:Treinen@localhost:3306/DelayMap")
    test_gtfs.from_url("https://sncb-opendata.hafas.de/gtfs/static/c21ac6758dd25af84cca5b707f3cb3de")

def test_gtfs_from_url_sqlite():
    test_gtfs = gtfs.GTFS("sqlite:///:memory:")
    test_gtfs.from_url("https://sncb-opendata.hafas.de/gtfs/static/c21ac6758dd25af84cca5b707f3cb3de")