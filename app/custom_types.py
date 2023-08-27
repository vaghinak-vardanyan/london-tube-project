from typing import NamedTuple


class Column(NamedTuple):
    name: str
    data_type: str
    is_primary_key: bool = False
    is_foreign_key: bool = False
    foreign_key_table: str = ""
    foreign_key_column: str = ""
