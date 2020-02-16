"""
database.py: all database interactions for GTFS
"""

import sqlalchemy

from realtime_gtfs.models import (Agency, Route, Stop, Trip, StopTime, Service,
                                  FareAttribute, FareRule, Shape, Frequency,
                                  Transfer, Pathway, Level, FeedInfo, Translation)


class DatabaseConnection:
    """
    DatabaseConnection: Handles database interactions
    """
    def __init__(self, url):
        self.engine = sqlalchemy.create_engine(url, echo=True)
        self.connection = self.engine.connect()
        self.meta = sqlalchemy.MetaData()
        self.meta.bind = self.engine
        self.tables = {}

        self.tables["agencies"] = Agency.create_table(self.meta)
        self.tables["fare_attributes"] = FareAttribute.create_table(self.meta)
        self.tables["routes"] = Route.create_table(self.meta)
        self.tables["stops"] = Stop.create_table(self.meta)
        self.tables["fare_rules"] = FareRule.create_table(self.meta)
        self.tables["feed_infos"] = FeedInfo.create_table(self.meta)
        self.tables["frequencies"] = Frequency.create_table(self.meta)
        self.tables["levels"] = Level.create_table(self.meta)
        self.tables["pathways"] = Pathway.create_table(self.meta)
        self.tables["services"] = Service.create_table(self.meta)
        self.tables["shapes"] = Shape.create_table(self.meta)
        self.tables["stop_times"] = StopTime.create_table(self.meta)
        self.tables["transfers"] = Transfer.create_table(self.meta)
        self.tables["translations"] = Translation.create_table(self.meta)
        self.tables["trips"] = Trip.create_table(self.meta)


    def reset(self):
        """
        reset: resets the ENTIRE database, dropping and recreating all tables
        """
        self.meta.drop_all()
        self.meta.create_all()

    def add_gtfs(self, gtfs):
        """
        add_gtfs: Write all data of a GTFS instance to the database
        """
        self.meta.create_all()
        self.write_agencies(gtfs.agencies)
        self.write_fare_attributes(gtfs.fare_attributes)
        self.write_fare_rules(gtfs.fare_rules)
        self.write_feed_info(gtfs.feed_info)
        self.write_frequencies(gtfs.frequencies)
        self.write_levels(gtfs.levels)

    def write_agencies(self, agencies):
        """
        write_agencies: writes all instances of Agency
        """
        for agency in agencies:
            ins = sqlalchemy.sql.expression.insert(self.tables["agencies"],
                                                   values=agency.to_dict())
            self.connection.execute(ins)

    def write_fare_attributes(self, fare_attributes):
        """
        write_fare_attributes: writes all instances of FareAttribute
        """
        for attribute in fare_attributes:
            ins = sqlalchemy.sql.expression.insert(self.tables["fare_attributes"],
                                                   values=attribute.to_dict())
            self.connection.execute(ins)

    def write_fare_rules(self, fare_rules):
        """
        write_fare_rules: writes all instances of FareRule
        """
        for fare_rule in fare_rules:
            ins = sqlalchemy.sql.expression.insert(self.tables["fare_rules"],
                                                   values=fare_rule.to_dict())
            self.connection.execute(ins)


    def write_feed_info(self, feedinfo):
        """
        write_feed_info: writes all instances of FeedInfo
        """
        ins = sqlalchemy.sql.expression.insert(self.tables["feed_infos"], values=feedinfo.to_dict())
        self.connection.execute(ins)

    def write_frequencies(self, frequencies):
        """
        write_frequencies: writes all instances of Frequency
        """
        for frequency in frequencies:
            ins = sqlalchemy.sql.expression.insert(self.tables["frequencies"],
                                                   values=frequency.to_dict())
            self.connection.execute(ins)

    def write_levels(self, levels):
        """
        write_levels: writes all instances of Level
        """
        for level in levels:
            ins = sqlalchemy.sql.expression.insert(self.tables["levels"],
                                                   values=level.to_dict())
            self.connection.execute(ins)
