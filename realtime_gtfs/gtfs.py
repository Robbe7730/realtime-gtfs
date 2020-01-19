"""
gtfs.py: contains main class GTFS
"""

import tempfile
import zipfile
import requests
import sqlalchemy
from sqlalchemy import MetaData, Column, String, Table

from realtime_gtfs.agency import Agency
from realtime_gtfs.stop import Stop

class GTFS():
    """
    GTFS: main GTFS class
    """
    def __init__(self):
        self.agencies = []
        self.stops = []
        self.connection = None

    def write_to_db(self, url):
        """
        write_to_db: write GTFS data to database

        Arguments:
        url: URL for database connection
        """
        self.connection = sqlalchemy.create_engine(url)
        meta = MetaData()
        Table(
            'agencies', meta,
            Column('agency_id', String(length=255), primary_key=True),
            Column('agency_name', String(length=255)),
            Column('agency_url', String(length=255)),
            Column('agency_timezone', String(length=255)),
        )
        meta.create_all(self.connection)

    # GTFS reading
    def from_url(self, url):
        """
        from_url: initialize a gtfs object from a URL. Zip file is only stored in a tempfile.

        Arguments:
        url: URL to realtime GTFS data
        """
        response = requests.get(url)
        if response.status_code == 200:
            with tempfile.TemporaryFile() as temp_zip_file:
                for chunk in response.iter_content(chunk_size=128):
                    temp_zip_file.write(chunk)
                with zipfile.ZipFile(temp_zip_file) as zip_file:
                    self.from_zip(zip_file)

    def from_zip(self, zip_file):
        """
        from_zip: initialize a gtfs object from a zip file.

        Arguments:
        zip_file: ZipFile containing the GTFS data
        """
        self.parse_agencies(zip_file.read("agency.txt"))
        self.parse_stops(zip_file.read("stops.txt"))

    def parse_agencies(self, agencies):
        """
        parse_agencies: read agency.txt

        Arguments:
        agencies: bytes-like object contianing the contents of `agency.txt`
        """
        agency_info = [line.split(',') for line in str(agencies, "UTF-8").strip().split('\n')]
        for line in agency_info[1:]:
            self.agencies.append(Agency.from_gtfs(agency_info[0], line))

    def parse_stops(self, stops):
        """
        parse_stops: read stops.txt

        Arguments:
        stops: bytes-like object contianing the contents of `stops.txt`
        """
        stop_info = [line.split(',') for line in str(stops, "UTF-8").strip().split('\n')]
        for line in stop_info[1:]:
            self.stops.append(Stop.from_gtfs(stop_info[0], line))
