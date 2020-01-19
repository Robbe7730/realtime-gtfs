"""
gtfs.py: contains main class GTFS
"""

import tempfile
import zipfile
import requests
import sqlalchemy
from sqlalchemy import MetaData, Column, String, Table

from realtime_gtfs.models import (Agency, Route, Stop, Trip, StopTime, Service,
                                  ServiceException, FareAttribute, FareRule, Shape)

from realtime_gtfs.exceptions import InvalidURLError

class GTFS():
    """
    GTFS: main GTFS class
    """
    def __init__(self):
        self.agencies = []
        self.stops = []
        self.routes = []
        self.trips = []
        self.stop_times = []
        self.services = []
        self.service_exceptions = []
        self.fare_attributes = []
        self.fare_rules = []
        self.shapes = []
        self.connection = None
        self.zip_file = None
        self.zip_file_url = ""

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
    def get_zip(self, url):
        """
        get_zip: download zip from url, returns tempfile with zip

        Arguments:
        url: URL to static GTFS data
        """
        if self.zip_file is None or url != self.zip_file_url:
            response = requests.get(url)

            if response.status_code != 200:
                raise InvalidURLError(url)

            temp_zip_file = tempfile.TemporaryFile()
            for chunk in response.iter_content(chunk_size=128):
                temp_zip_file.write(chunk)
            self.zip_file = zipfile.ZipFile(temp_zip_file)
            self.zip_file_url = url

        return self.zip_file


    def from_url(self, url):
        """
        from_url: initialize a gtfs object from a URL.

        Arguments:
        url: URL to static GTFS data
        """
        zip_file = self.get_zip(url)
        self.from_zip(zip_file)
        zip_file.close()

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
        self.parse_stop_times(zip_file.read("stop_times.txt"))
        if "calendar.txt" in zip_file.namelist():
            self.parse_calendar(zip_file.read("calendar.txt"))
        if "calendar_dates.txt" in zip_file.namelist():
            self.parse_calendar_dates(zip_file.read("calendar_dates.txt"))
        if "fare_attributes.txt" in zip_file.namelist():
            self.parse_fare_attributes(zip_file.read("fare_attributes.txt"))
        if "fare_rules.txt" in zip_file.namelist():
            self.parse_fare_rules(zip_file.read("fare_rules.txt"))
        if "shapes.txt" in zip_file.namelist():
            self.parse_shapes(zip_file.read("shapes.txt"))

    def parse_agencies(self, agencies):
        """
        parse_agencies: read agency.txt

        Arguments:
        agencies: bytes-like object containing the contents of `agency.txt`
        """
        agency_info = [line.strip().split(',') for line in
                       str(agencies, "UTF-8").strip().split('\n')]
        for line in agency_info[1:]:
            self.agencies.append(Agency.from_gtfs(agency_info[0], line))

    def parse_stops(self, stops):
        """
        parse_stops: read stops.txt

        Arguments:
        stops: bytes-like object containing the contents of `stops.txt`
        """
        stop_info = [line.strip().split(',') for line in str(stops, "UTF-8").strip().split('\n')]
        for line in stop_info[1:]:
            self.stops.append(Stop.from_gtfs(stop_info[0], line))

    def parse_routes(self, routes):
        """
        parse_routes: read routes.txt

        Arguments:
        routes: bytes-like object containing the contents of `routes.txt`
        """
        stop_info = [line.strip().split(',') for line in str(routes, "UTF-8").strip().split('\n')]

        for line in stop_info[1:]:
            self.routes.append(Route.from_gtfs(stop_info[0], line))

    def parse_trips(self, trips):
        """
        parse_trips: read trips.txt

        Arguments:
        trips: bytes-like object containing the contents of `trips.txt`
        """
        trip_info = [line.strip().split(',') for line in
                     str(trips, "UTF-8").strip().split('\n')]

        # ------ v UGLY FIX FOR NMBS DATA v ------

        if trip_info[0][-1] == "trip_type":
            for line in trip_info[1:]:
                del line[-1]

        # ------ ^ UGLY FIX FOR NMBS DATA ^ ------


        for line in trip_info[1:]:
            self.trips.append(Trip.from_gtfs(trip_info[0], line))

    def parse_stop_times(self, stop_times):
        """
        parse_stop_times: read stop_times.txt

        Arguments:
        stop_times: bytes-like object containing the contents of `stop_times.txt`
        """
        stop_time_info = [line.strip().split(',') for line in
                          str(stop_times, "UTF-8").strip().split('\n')]
        for line in stop_time_info[1:]:
            self.stop_times.append(StopTime.from_gtfs(stop_time_info[0], line))

    def parse_calendar(self, calendar):
        """
        parse_calendar: read calendar.txt

        Arguments:
        calendar: bytes-like object containing the contents of `calendar.txt`
        """
        calendar_info = [line.strip().split(',') for line in
                         str(calendar, "UTF-8").strip().split('\n')]
        for line in calendar_info[1:]:
            self.services.append(Service.from_gtfs(calendar_info[0], line))

    def parse_calendar_dates(self, calendar_dates):
        """
        parse_calendar_dates: read calendar_dates.txt

        Arguments:
        calendar_dates: bytes-like object containing the contents of `calendar_dates.txt`
        """
        calendar_dates_info = [
            line.strip().split(',') for line in str(calendar_dates, "UTF-8").strip().split('\n')
        ]
        for line in calendar_dates_info[1:]:
            self.service_exceptions.append(ServiceException.from_gtfs(calendar_dates_info[0], line))

    def parse_fare_attributes(self, fare_attribute):
        """
        parse_fare_attributes: read fare_attributes.txt

        Arguments:
        fare_attribute: bytes-like object containing the contents of `fare_attributes.txt`
        """
        fare_attribute_info = [
            line.strip().split(',') for line in str(fare_attribute, "UTF-8").strip().split('\n')
        ]
        for line in fare_attribute_info[1:]:
            self.fare_attributes.append(FareAttribute.from_gtfs(fare_attribute_info[0], line))

    def parse_fare_rules(self, fare_rule):
        """
        parse_fare_rules: read fare_rules.txt

        Arguments:
        fare_rule: bytes-like object containing the contents of `fare_rules.txt`
        """
        fare_rule_info = [
            line.strip().split(',') for line in str(fare_rule, "UTF-8").strip().split('\n')
        ]
        for line in fare_rule_info[1:]:
            self.fare_rules.append(FareRule.from_gtfs(fare_rule_info[0], line))

    def parse_shapes(self, shape):
        """
        parse_shapes: read shapes.txt

        Arguments:
        shape: bytes-like object containing the contents of `shapes.txt`
        """
        shape_info = [
            line.strip().split(',') for line in str(shape, "UTF-8").strip().split('\n')
        ]
        for line in shape_info[1:]:
            self.shapes.append(Shape.from_gtfs(shape_info[0], line))
