from __future__ import annotations

from typing import Any, Optional, Sequence, cast

import psycopg2
from psycopg2 import extras, sql

from app.abstractions import Database
from app.custom_types import Column


class PostgreDB(Database):
    def __init__(
        self, database: str, user: str, password: str, host: str, port: str
    ):
        self._connection = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port,
        )

    def _create_column_definition_string(self, column: Column) -> sql.Composed:
        """Create column definition to use them in order to create a table"""
        column_definition = (
            sql.Identifier(column.name)
            + sql.SQL(" ")
            + sql.SQL(column.data_type)
        )

        if column.is_foreign_key:
            column_definition += sql.SQL(
                " REFERENCES {table}({column})"
            ).format(
                sql.Identifier(column.foreign_key_table),
                sql.Identifier(column.foreign_key_column),
            )
        return column_definition

    def _to_valid_identifier(self, value: str):
        return sql.SQL(".").join(
            [sql.Identifier(component) for component in value.split(".")]
        )

    def create_table(self, table: str, columns: list[Column]):
        """Create table in the database"""
        primary_key = sql.SQL("PRIMARY KEY ({columns})").format(
            columns=sql.SQL(",").join(
                [
                    sql.Identifier(column.name)
                    for column in columns
                    if column.is_primary_key
                ]
            )
        )
        query = sql.SQL(
            "CREATE TABLE IF NOT EXISTS {table} ({columns});"
        ).format(
            table=sql.Identifier(table),
            columns=sql.SQL(",").join(
                [
                    self._create_column_definition_string(column)
                    for column in columns
                ]
                + [primary_key]
            ),
        )
        with self._connection, self._connection.cursor() as cursor:
            cursor.execute(query)

    def insert_batch(
        self,
        table: str,
        columns: list[str],
        values: Sequence[tuple[Any, ...]],
    ):
        """Insert data with batches in order to reduce roundtrips"""
        placeholders = sql.SQL(",").join(sql.Placeholder() * len(values[0]))
        query = sql.SQL(
            "INSERT INTO {table} ({columns}) VALUES ({values})"
        ).format(
            table=sql.Identifier(table),
            columns=sql.SQL(",").join(
                [sql.Identifier(column) for column in columns]
            ),
            values=placeholders,
        )
        with self._connection, self._connection.cursor() as cursor:
            extras.execute_batch(cursor, query, values)

    def insert(
        self,
        table: str,
        columns: list[str],
        value: tuple[Any, ...],
        return_column: Optional[str] = None,
    ) -> Any:
        """Insert row into table and optionally return any value"""
        result = None
        placeholders = sql.SQL(",").join(sql.Placeholder() * len(value))
        query = sql.SQL(
            "INSERT INTO {table} ({columns}) VALUES ({value})"
        ).format(
            table=sql.Identifier(table),
            columns=sql.SQL(",").join(
                [sql.Identifier(column) for column in columns]
            ),
            value=placeholders,
        )
        if return_column:
            query += sql.SQL(" RETURNING {return_column}").format(
                return_column=sql.Identifier(return_column)
            )
        with self._connection, self._connection.cursor() as cursor:
            cursor.execute(query, value)
            if return_column:
                result = cast(tuple, cursor.fetchone())[0]

        return result

    def data_exists(self, table: str) -> bool:
        """Check whether there is data in the {table}"""
        query = sql.SQL("SELECT COUNT(*) FROM {table};").format(
            table=sql.Identifier(table)
        )
        with self._connection, self._connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            count = cast(tuple, result)[0]
            return count > 0

    def select(
        self,
        table: str,
        columns: list[str],
        join_tables: Optional[list[str]] = None,
        left_ons: Optional[list[str]] = None,
        right_ons: Optional[list[str]] = None,
        filter_colummn: Optional[str] = None,
        filter_value: Optional[Any] = None,
    ) -> list[dict[str, Any]]:
        """select rows from table optionally join multiple tables"""
        query = sql.SQL("SELECT {columns} FROM {table}").format(
            columns=sql.SQL(",").join(
                [self._to_valid_identifier(column) for column in columns]
            ),
            table=self._to_valid_identifier(table),
        )

        if join_tables and left_ons and right_ons:
            query += sql.SQL(" ") + sql.SQL(" ").join(
                [
                    sql.SQL("JOIN {table} ON {left_on} = {right_on}").format(
                        table=self._to_valid_identifier(join_table),
                        left_on=self._to_valid_identifier(left_on),
                        right_on=self._to_valid_identifier(right_on),
                    )
                    for join_table, left_on, right_on in zip(
                        join_tables, left_ons, right_ons
                    )
                ]
            )

        if filter_colummn and filter_value:
            query += sql.SQL(" ") + sql.SQL("WHERE {column} = %s").format(
                column=self._to_valid_identifier(filter_colummn)
            )

        with self._connection, self._connection.cursor(
            cursor_factory=extras.DictCursor
        ) as cursor:
            if filter_value:
                cursor.execute(query, (filter_value,))
            else:
                cursor.execute(query)

            rows = cast(list[dict[str, Any]], cursor.fetchall())
            return rows
