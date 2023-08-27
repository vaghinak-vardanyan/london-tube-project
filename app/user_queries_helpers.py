from app import constants, repositories


def _print_possible_queries():
    print()
    print("Choose the query you like:")
    print()
    print(
        (
            f"{constants.QUERY_BY_LINE_NAME_NUMBER}."
            f" {constants.QUERY_BY_LINE_NAME}"
        )
    )
    print(
        (
            f"{constants.QUERY_BY_STATION_NAME_NUMBER}."
            f" {constants.QUERY_BY_STATION_NAME}"
        )
    )
    print(
        (
            f"{constants.QUERY_BY_STATION_ID_NUMBER}."
            f" {constants.QUERY_BY_STATION_ID}"
        )
    )
    print()


def _handle_by_line_name_query(
    network_repository: repositories.LondonTubeNetworkRepository,
):
    line_name = input("Enter the name of the line: ")
    stations = network_repository.get_stations_by_line_name(line_name)
    if not stations:
        print("No stations found, maybe the entered name is invalid")
    else:
        print(
            (
                "Here are the stations that the "
                f"line '{line_name}' passes through:"
            )
        )
        for station in stations:
            print(station)


def _handle_by_station_name_query(
    network_repository: repositories.LondonTubeNetworkRepository,
):
    station_name = input("Enter the name of the station: ")
    lines = network_repository.get_lines_by_station_name(station_name)
    if not lines:
        print("No lines found, maybe the entered name is invalid")
    else:
        print(
            (
                "Here are the lines passing"
                f" through station '{station_name}':"
            )
        )
        for line in lines:
            print(line)


def _handle_by_station_id_query(
    network_repository: repositories.LondonTubeNetworkRepository,
):
    station_id = input("Enter the id of the station: ")
    lines = network_repository.get_lines_by_station_id(station_id)
    if not lines:
        print("No lines found, maybe the entered id is invalid")
    else:
        print(
            (
                "Here are the lines passing "
                f"through station by id '{station_id}':"
            )
        )
        for line in lines:
            print(line)


def _handle_exit():
    exit(0)


def _handle_invalid_input():
    print("Wrong input. Valid inputs are query numbers and 'q' for exit")


def user_input_loop(
    network_repository: repositories.LondonTubeNetworkRepository,
):
    while True:
        _print_possible_queries()
        query_number = input("Enter the query number ('q' to exit): ")
        if query_number == constants.QUERY_BY_LINE_NAME_NUMBER:
            _handle_by_line_name_query(network_repository)
        elif query_number == constants.QUERY_BY_STATION_NAME_NUMBER:
            _handle_by_station_name_query(network_repository)
        elif query_number == constants.QUERY_BY_STATION_ID_NUMBER:
            _handle_by_station_id_query(network_repository)
        elif query_number == constants.EXIT_INPUT:
            _handle_exit()
        else:
            _handle_invalid_input()
