# data
SEED_DATA_FILE_PATH = "data/london_tube_nework.json"
STATION_ID_LENGTH = 11


STATIONS = "stations"
LINES = "lines"
LINE_STATIONS = "line_stations"

# column names
ID = "id"
NAME = "name"
LONGITUDE = "longitude"
LATITUDE = "latitude"
STATION_ID = "station_id"
LINE_ID = "line_id"

# column types
VARCHAR = "varchar"
CHAR_11 = "char(11)"
NUMERIC = "numeric"
INT = "int"
SERIAL = "serial"


# Queries
QUERY_BY_LINE_NAME = (
    "Given the line name, return stations that the line passes through"
)
QUERY_BY_STATION_NAME = (
    "Given the station name, return the lines passing through that station"
)
QUERY_BY_STATION_ID = (
    "Given the station id, return the lines passing through that station"
)
QUERY_BY_LINE_NAME_NUMBER = "1"
QUERY_BY_STATION_NAME_NUMBER = "2"
QUERY_BY_STATION_ID_NUMBER = "3"
EXIT_INPUT = "q"
