import requests
import tempfile
import zipfile
import sqlalchemy
from sqlalchemy import MetaData, Column, String, Table

connection = None

# Exceptions
class NoConnectionError(RuntimeError):
   def __init__(self):
       self.args = ["No database connection"]

# Database
def connect(url):
    global connection
    connection = sqlalchemy.create_engine(url, echo = True)
    meta = MetaData()
    agency = Table(
        'agencies', meta, 
        Column('agency_id', String(length=255), primary_key = True), 
        Column('agency_name', String(length=255)), 
        Column('agency_url', String(length=255)),
        Column('agency_timezone', String(length=255)),
    )
    meta.create_all(connection)

# Decorators
def requires_connection(func):
    def inner(*args):
        if (connection == None):
            raise NoConnectionError()
        else:
            func(*args)
    return inner

# GTFS reading
@requires_connection
def from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        with tempfile.TemporaryFile() as temp_zip_file:
            for chunk in response.iter_content(chunk_size=128):
                temp_zip_file.write(chunk)
            with zipfile.ZipFile(temp_zip_file) as zip_file:
                from_zip(zip_file)

@requires_connection
def from_zip(zip_file):
    zip_file.printdir()