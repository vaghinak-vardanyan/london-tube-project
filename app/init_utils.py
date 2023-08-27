import argparse
import os

from app import constants, loaders, repositories


def add_app_arguments(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-d",
        "--database",
        help="Specify the database name",
    )
    parser.add_argument(
        "-u",
        "--user",
        help="Specify the user name used to authenticate",
    )
    parser.add_argument(
        "-p",
        "--password",
        help="Specify the password used to authenticate",
    )
    parser.add_argument(
        "-ht",
        "--host",
        required=False,
        default="localhost",
        help="Specify the database host address (defaults to localhost)",
    )
    parser.add_argument(
        "-pt",
        "--port",
        required=False,
        default="5432",
        help="Specify the connection port number (defaults to 5432)",
    )


def initialize_db(
    network_repository: repositories.LondonTubeNetworkRepository,
):
    network_repository.create_tables_if_not_exists()
    loader = loaders.LondonTubeNetworkLoader(network_repository)
    load_data_file_path = os.path.join(
        os.getcwd(), constants.SEED_DATA_FILE_PATH
    )
    loader.load_initial_data(load_data_file_path)
