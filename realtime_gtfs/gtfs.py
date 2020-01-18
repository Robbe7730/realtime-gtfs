import requests
import tempfile
import zipfile
import sqlalchemy
from sqlalchemy import MetaData, Column, String, Table

from realtime_gtfs.agency import Agency

class GTFS(object):
    def __init__(self, url):
        self.agencies = []
        self.connection = sqlalchemy.create_engine(url)
        meta = MetaData()
        agency_table = Table(
            'agencies', meta, 
            Column('agency_id', String(length=255), primary_key = True), 
            Column('agency_name', String(length=255)), 
            Column('agency_url', String(length=255)),
            Column('agency_timezone', String(length=255)),
        )
        meta.create_all(self.connection)

    # GTFS reading
    def from_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            with tempfile.TemporaryFile() as temp_zip_file:
                for chunk in response.iter_content(chunk_size=128):
                    temp_zip_file.write(chunk)
                with zipfile.ZipFile(temp_zip_file) as zip_file:
                    self.from_zip(zip_file)

    def from_zip(self, zip_file):
        self.parse_agencies(zip_file.read("agency.txt"))

    def parse_agencies(self, agencies):
        agency_info = [line.split(',') for line in str(agencies, "UTF-8").strip().split('\n')]
        for line in agency_info[1:]:
            self.agencies.append(Agency.from_gtfs(agency_info[0], line))