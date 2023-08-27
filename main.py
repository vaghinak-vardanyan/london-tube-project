#!/usr/bin/env python3

import argparse

from app import databases, repositories
from app.init_utils import add_app_arguments, initialize_db
from app.user_queries_helpers import user_input_loop


def main():
    parser = argparse.ArgumentParser()
    add_app_arguments(parser)
    args = parser.parse_args()

    postgre_db = databases.PostgreDB(
        database=args.database,
        user=args.user,
        password=args.password,
        host=args.host,
        port=args.port,
    )
    network_repository = repositories.LondonTubeNetworkRepository(postgre_db)
    initialize_db(network_repository)

    user_input_loop(network_repository)


if __name__ == "__main__":
    main()
