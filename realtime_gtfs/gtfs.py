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
from realtime_gtfs.route import Route
from realtime_gtfs.trip import Trip

class GTFS():
    """
    GTFS: main GTFS class
    """
    def __init__(self):
        self.agencies = []
        self.stops = []
        self.routes = []
        self.trips = []
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
        self.parse_routes(zip_file.read("routes.txt"))
        self.parse_trips(zip_file.read("trips.txt"))

    def parse_agencies(self, agencies):
        """
        parse_agencies: read agency.txt

        Arguments:
        agencies: bytes-like object containing the contents of `agency.txt`
        """
        agency_info = [line.split(',') for line in str(agencies, "UTF-8").strip().split('\n')]
        for line in agency_info[1:]:
            self.agencies.append(Agency.from_gtfs(agency_info[0], line))

    def parse_stops(self, stops):
        """
        parse_stops: read stops.txt

        Arguments:
        stops: bytes-like object containing the contents of `stops.txt`
        """
        stop_info = [line.split(',') for line in str(stops, "UTF-8").strip().split('\n')]
        for line in stop_info[1:]:
            self.stops.append(Stop.from_gtfs(stop_info[0], line))

    def parse_routes(self, routes):
        """
        parse_routes: read routes.txt

        Arguments:
        routes: bytes-like object containing the contents of `routes.txt`
        """
        stop_info = [line.split(',') for line in str(routes, "UTF-8").strip().split('\n')]

        # ------ v UGLY FIX FOR NMBS DATA v ------

        for line in stop_info[1:]:
            line[5] = line[5][0]

        # ------ ^ UGLY FIX FOR NMBS DATA ^ ------

        for line in stop_info[1:]:
            self.routes.append(Route.from_gtfs(stop_info[0], line))

    def parse_trips(self, trips):
        """
        parse_trips: read trips.txt

        Arguments:
        trips: bytes-like object containing the contents of `trips.txt`
        """
        trip_info = [line.split(',') for line in str(trips, "UTF-8").strip().split('\n')]

        # ------ v UGLY FIX FOR NMBS DATA v ------

        for line in trip_info[1:]:
            del line[-1]

        # ------ ^ UGLY FIX FOR NMBS DATA ^ ------


        for line in trip_info[1:]:
            self.trips.append(Trip.from_gtfs(trip_info[0], line))
