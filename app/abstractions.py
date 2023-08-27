from abc import ABC, abstractmethod
from typing import Any, Optional, Sequence

from app.custom_types import Column


class Database(ABC):
    @abstractmethod
    def create_table(self, table: str, columns: list[Column]):
        pass

    @abstractmethod
    def insert_batch(
        self,
        table: str,
        columns: list[str],
        values: Sequence[tuple[Any, ...]],
    ):
        pass

    @abstractmethod
    def insert(
        self,
        table: str,
        columns: list[str],
        value: tuple[Any, ...],
        return_column: Optional[str] = None,
    ) -> Any:
        pass

    @abstractmethod
    def data_exists(self, table: str) -> bool:
        pass

    @abstractmethod
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
        pass


class DatabaseLoader(ABC):
    @abstractmethod
    def load_initial_data(self, file_path: str):
        pass
