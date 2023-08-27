from typing import Any

from app import constants, validators
from app.abstractions import DatabaseLoader
from app.models.station import Station
from app.repositories import LondonTubeNetworkRepository
from app.utils import read_json


class LondonTubeNetworkLoader(DatabaseLoader):
    def __init__(self, repository: LondonTubeNetworkRepository):
        self._repository = repository

    def _load_stations(self, stations_raw: list[dict[str, Any]]):
        """Load stations data into the database"""
        if self._repository.is_stations_empty():
            print("Stations are already loaded")
            return

        print("Loading stations data...")
        stations = []
        corrupted_data_count = 0
        valid_data_count = 0
        for station in stations_raw:
            issue_message = validators.validate_station(station)
            if issue_message:
                corrupted_data_count += 1
                print(f"Skiping data {station}: Reason: {issue_message}")
            else:
                valid_data_count += 1
                stations.append(
                    Station(
                        id=station[constants.ID],
                        name=station[constants.NAME],
                        longitude=station[constants.LONGITUDE],
                        latitude=station[constants.LATITUDE],
                    )
                )

        self._repository.insert_station_batch(stations)
        print(f"{valid_data_count} station data has been successfully added")
        print(f"Overall skipped {corrupted_data_count} station data")

    def _seed_lines(self, lines_raw: list[dict[str, Any]]):
        """Load lines data into the database"""
        if self._repository.is_lines_empty():
            print("Lines are already loaded")
            return

        print("Loading lines data...")
        corrupted_data_count = 0
        lines_added_count = 0
        line_stations_added_count = 0
        for line in lines_raw:
            issue_message = validators.validate_line(line)
            if issue_message:
                corrupted_data_count += 1
                print(f"Skiping data {line}: Reason: {issue_message}")
            else:
                line_id = self._repository.insert_line(
                    line_name=line[constants.NAME]
                )
                lines_added_count += 1
                self._repository.insert_line_stations(
                    line_id=line_id,
                    station_ids=line[constants.STATIONS],
                )
                line_stations_added_count += len(line[constants.STATIONS])
        print(f"{lines_added_count} line data has been successfully added")
        print(
            (
                f"{line_stations_added_count} line station data"
                " has been successfully added"
            )
        )
        print(f"Overall skipped {corrupted_data_count} lines data")

    def load_initial_data(self, file_path: str):
        """Load data into the database"""
        data = read_json(file_path)
        if constants.STATIONS not in data:
            raise ValueError("No stations data is provided")
        if constants.LINES not in data:
            raise ValueError("No lines data is provided")
        self._load_stations(data[constants.STATIONS])
        self._seed_lines(data[constants.LINES])
