# London Tube Project

![Python](https://img.shields.io/badge/Python-3.10-brightgreen)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


### Run

1. Create virtual env
    ```shell
    $ python -m venv .venv
    $ source .venv/bin/activate
    $ pip install -U pip
    ```

2. Install the requirements
    ```shell
    $ pip install -r requirements.txt
    ```

3. Run the application
    ```shell
    $ python main.py -d <database_name> -u <user_name> -p <password> [-ht <host>] [-pt <port>]
    ```
    simplest way
    ```shell
    $  python main.py -d london-tube -u postgres -p postgres
    ```


## About the project
Loads london's tube network data into database and allows user to perform some simple queries on it.

DB structure
stations(id primary key, name, longitude, latitude) <br />
line_stations(line_id foreign key lines(id), station_id foreign key stations(id)) <br />
lines(id primary key, name)
