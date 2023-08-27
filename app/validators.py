from typing import Any

from app import constants


def validate_station(station_raw: dict[str, Any]):
    """Check whether the station data read from file is valid"""
    result = ""
    if constants.ID not in station_raw:
        result = f"{constants.ID} is missing"
    elif constants.NAME not in station_raw:
        result = f"{constants.NAME} is missing"
    elif constants.LONGITUDE not in station_raw:
        result = f"{constants.LONGITUDE} is missing"
    elif constants.LATITUDE not in station_raw:
        result = f"{constants.LATITUDE} is missing"
    elif len(station_raw[constants.ID]) != constants.STATION_ID_LENGTH:
        result = f"{constants.ID} length is other than expected"
    elif not isinstance(station_raw[constants.ID], str):
        result = f"{constants.ID} has wrong type"
    elif not isinstance(station_raw[constants.NAME], str):
        result = f"{constants.NAME} has wrong type"
    elif not isinstance(station_raw[constants.LONGITUDE], float):
        result = f"{constants.LONGITUDE} has wrong type"
    elif not isinstance(station_raw[constants.LATITUDE], float):
        result = f"{constants.LATITUDE} has wrong type"
    return result


def validate_line(line_raw: dict[str, Any]):
    result = ""
    if constants.NAME not in line_raw:
        result = f"{constants.NAME} is missing"
    elif constants.STATIONS not in line_raw:
        result = f"{constants.STATIONS} is missing"
    elif not isinstance(line_raw[constants.NAME], str):
        result = f"{constants.NAME} has wrong type"
    elif not isinstance(line_raw[constants.STATIONS], list):
        result = f"{constants.STATIONS} has wrong type"
    elif any(
        not isinstance(station_id, str)
        for station_id in line_raw[constants.STATIONS]
    ):
        result = "one or more station in the line has wrong type"
    elif any(
        len(station_id) != constants.STATION_ID_LENGTH
        for station_id in line_raw[constants.STATIONS]
    ):
        result = "one or more station id has other length than expected"
    return result
