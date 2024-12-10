from abc import ABC, abstractmethod

class DatabaseManagerBase(ABC):



    """
    Абстрактный базовый класс для работы с базами данных.
    """
    @abstractmethod
    def _connect(self, **kwargs):
        pass

    @abstractmethod
    def create_table(self, table_name: str, columns: dict[str, str]):
        pass

    @abstractmethod
    def insert_data(self, table_name: str, data: dict[str, any]):
        pass

    @abstractmethod
    def add_columns(self, table_name: str, columns: dict[str, str]):
        pass

    @abstractmethod
    def update_for_current_product(self, table_name: str, user_identifier: dict[str, any], update_data: dict[str, any]):
        pass

    @abstractmethod
    def close_connection(self):
        pass