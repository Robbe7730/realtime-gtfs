"""
database.py: all database interactions for GTFS
"""

import sqlalchemy

from realtime_gtfs.models import (Agency, Route, Stop, Trip, StopTime, Service,
                                  ServiceException, FareAttribute, FareRule, Shape, Frequency,
                                  Transfer, Pathway, Level, FeedInfo, Translation)

def write_to_db(_gtfs, url):
    """
    write_to_db: write GTFS data to database

    Arguments:
    url: URL for database connection
    """
    connection = sqlalchemy.create_engine(url, echo=True)
    create_tables(connection)

def create_tables(connection):
    """
    create_tables: create all tables required for GTFS

    Expects self.connection to be set up beforehand!
    """
    meta = sqlalchemy.MetaData()

    Agency.create_table(meta)
    FareAttribute.create_table(meta)
    Route.create_table(meta)
    Stop.create_table(meta)
    FareRule.create_table(meta)
    FeedInfo.create_table(meta)
    Frequency.create_table(meta)
    Level.create_table(meta)
    Pathway.create_table(meta)
    Service.create_table(meta)
    ServiceException.create_table(meta)
    Shape.create_table(meta)
    StopTime.create_table(meta)
    Transfer.create_table(meta)
    Translation.create_table(meta)
    Trip.create_table(meta)

    meta.create_all(connection)
