from app import constants
from app.custom_types import Column
from app.databases import Database
from app.models.line import Line
from app.models.station import Station


class LondonTubeNetworkRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def _create_stations_table_if_not_exists(self):
        """Create Stations table in the database"""
        columns = [
            Column(
                name=constants.ID,
                data_type=constants.CHAR_11,
                is_primary_key=True,
            ),
            Column(name=constants.NAME, data_type=constants.VARCHAR),
            Column(name=constants.LONGITUDE, data_type=constants.NUMERIC),
            Column(name=constants.LATITUDE, data_type=constants.NUMERIC),
        ]
        self._database.create_table(table=constants.STATIONS, columns=columns)

    def _create_lines_table_if_not_exists(self):
        """Create lines table in the database"""
        columns = [
            Column(
                name=constants.ID,
                data_type=constants.SERIAL,
                is_primary_key=True,
            ),
            Column(name=constants.NAME, data_type=constants.VARCHAR),
        ]
        self._database.create_table(table=constants.LINES, columns=columns)

    def _create_line_stations_table_if_not_exists(self):
        """Create line_stations table in the database"""
        columns = [
            Column(
                name=constants.LINE_ID,
                data_type=constants.INT,
                is_primary_key=True,
            ),
            Column(
                name=constants.STATION_ID,
                data_type=constants.CHAR_11,
                is_primary_key=True,
            ),
        ]
        self._database.create_table(
            table=constants.LINE_STATIONS, columns=columns
        )

    def create_tables_if_not_exists(self):
        """Create required tables"""
        self._create_stations_table_if_not_exists()
        self._create_lines_table_if_not_exists()
        self._create_line_stations_table_if_not_exists()

    def insert_station_batch(self, stations: list[Station]):
        """Insert stations data with batch"""
        columns = [
            constants.ID,
            constants.NAME,
            constants.LONGITUDE,
            constants.LATITUDE,
        ]
        values = [
            (
                station.id,
                station.name,
                station.longitude,
                station.latitude,
            )
            for station in stations
        ]
        self._database.insert_batch(
            table=constants.STATIONS,
            columns=columns,
            values=values,
        )

    def insert_line(self, line_name: str) -> int:
        """Insert line row and return line id"""
        return self._database.insert(
            table=constants.LINES,
            columns=[constants.NAME],
            value=(line_name,),
            return_column=constants.ID,
        )

    def insert_line_stations(self, line_id: int, station_ids: list[str]):
        """Insert line stations"""
        columns = [constants.LINE_ID, constants.STATION_ID]
        values = [
            (
                line_id,
                station_id,
            )
            for station_id in station_ids
        ]
        self._database.insert_batch(
            table=constants.LINE_STATIONS,
            columns=columns,
            values=values,
        )

    def is_stations_empty(self):
        return self._database.data_exists(constants.STATIONS)

    def is_lines_empty(self):
        return self._database.data_exists(constants.LINES)

    def get_lines_by_station_id(self, id: str):
        rows = self._database.select(
            table=constants.LINES,
            columns=[
                f"{constants.LINES}.{constants.ID}",
                f"{constants.LINES}.{constants.NAME}",
            ],
            join_tables=[constants.LINE_STATIONS],
            left_ons=[
                f"{constants.LINE_STATIONS}.{constants.LINE_ID}",
            ],
            right_ons=[
                f"{constants.LINES}.{constants.ID}",
            ],
            filter_colummn=f"{constants.LINE_STATIONS}.{constants.STATION_ID}",
            filter_value=id,
        )

        return [
            Line(id=row[constants.ID], name=row[constants.NAME])
            for row in rows
        ]

    def get_lines_by_station_name(self, name: str) -> list[Line]:
        rows = self._database.select(
            table=constants.STATIONS,
            columns=[
                f"{constants.LINES}.{constants.ID}",
                f"{constants.LINES}.{constants.NAME}",
            ],
            join_tables=[constants.LINE_STATIONS, constants.LINES],
            left_ons=[
                f"{constants.STATIONS}.{constants.ID}",
                f"{constants.LINE_STATIONS}.{constants.LINE_ID}",
            ],
            right_ons=[
                f"{constants.LINE_STATIONS}.{constants.STATION_ID}",
                f"{constants.LINES}.{constants.ID}",
            ],
            filter_colummn=f"{constants.STATIONS}.{constants.NAME}",
            filter_value=name,
        )

        return [
            Line(id=row[constants.ID], name=row[constants.NAME])
            for row in rows
        ]

    def get_stations_by_line_name(self, name: str) -> list[Station]:
        rows = self._database.select(
            table=constants.STATIONS,
            columns=[
                f"{constants.STATIONS}.{constants.ID}",
                f"{constants.STATIONS}.{constants.NAME}",
                f"{constants.STATIONS}.{constants.LONGITUDE}",
                f"{constants.STATIONS}.{constants.LATITUDE}",
            ],
            join_tables=[constants.LINE_STATIONS, constants.LINES],
            left_ons=[
                f"{constants.STATIONS}.{constants.ID}",
                f"{constants.LINE_STATIONS}.{constants.LINE_ID}",
            ],
            right_ons=[
                f"{constants.LINE_STATIONS}.{constants.STATION_ID}",
                f"{constants.LINES}.{constants.ID}",
            ],
            filter_colummn=f"{constants.LINES}.{constants.NAME}",
            filter_value=name,
        )

        return [
            Station(
                id=row[constants.ID],
                name=row[constants.NAME],
                longitude=row[constants.LONGITUDE],
                latitude=row[constants.LATITUDE],
            )
            for row in rows
        ]
