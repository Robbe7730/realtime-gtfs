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
        self.write_pathways(gtfs.pathways)
        self.write_routes(gtfs.routes)

    def _write_list_as_dicts(self, data_list, table_name):
        for data in data_list:
            ins = sqlalchemy.sql.expression.insert(self.tables[table_name],
                                                   values=data.to_dict())
            self.connection.execute(ins)

    def write_agencies(self, agencies):
        """
        write_agencies: writes all instances of Agency
        """
        self._write_list_as_dicts(agencies, "agencies")

    def write_fare_attributes(self, fare_attributes):
        """
        write_fare_attributes: writes all instances of FareAttribute
        """
        self._write_list_as_dicts(fare_attributes, "fare_attributes")

    def write_fare_rules(self, fare_rules):
        """
        write_fare_rules: writes all instances of FareRule
        """
        self._write_list_as_dicts(fare_rules, "fare_rules")

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
        self._write_list_as_dicts(frequencies, "frequencies")

    def write_levels(self, levels):
        """
        write_levels: writes all instances of Level
        """
        self._write_list_as_dicts(levels, "levels")

    def write_pathways(self, pathways):
        """
        write_pathways: writes all instances of Pathway
        """
        self._write_list_as_dicts(pathways, "pathways")

    def write_routes(self, routes):
        """
        write_routes: writes all instances of Route
        """
        self._write_list_as_dicts(routes, "routes")
