import psycopg2

from DatabaseManager.DatabaseManagerBase import DatabaseManagerBase
from DatabaseManager.determine_column_type import determine_column_type


def handle_errors(func):
    """
    Декоратор для обработки ошибок в методах.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Ошибка: {e}")
    return wrapper

class PostgreSQLManager(DatabaseManagerBase):
    def __init__(self, host: str, port: str, database: str, user: str, password: str):
        self.__connection = None
        self.__cursor = None
        self._connect(host=host, port=port, database=database, user=user, password=password)

    def _connect(self, **kwargs):
        print("Параметры подключения:", kwargs)
        self.__connection = psycopg2.connect(**kwargs)
        self.__cursor = self.__connection.cursor()

    def create_table(self, table_name: str, columns: dict[str, str]):
        """
        Создает таблицу в базе данных на основе словаря.
        :param table_name: Название таблицы
        :param columns: Словарь с определением столбцов (ключ: атрибут, значение: тип данных)
        """

        create_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            {', '.join(f"{col} {dtype}" for col, dtype in columns.items())})"""

        self.__cursor.execute(create_query)
        self.__connection.commit()

    def insert_data(self, table_name: str, data: dict[str, any]):
        """
        Вставляет данные в таблицу.
        :param table_name: Название таблицы
        :param data: Словарь с данными для вставки (ключ: атрибут, значение: данные)
        """
        columns = ', '.join(data.keys())
        placeholders =  ', '.join(['%s'] * len(data)) # Для защиты от SQL инъекций

        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"

        self.__cursor.execute(insert_query, list(data.values()))
        self.__connection.commit()

    def insert_data_dynamic_columns(self, table_name: str, data: dict[str, any]):
        """
        Вставляет данные в таблицу и добавляет новые атрибуты, если их нет.
        :param table_name: Название таблицы
        :param columns: Словарь с данными для вставки (ключ: атрибут, значение: данные)
        """
        try:
            self.__cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
            existing_columns = {column[0] for column in self.__cursor.fetchall()} # Список существующих столбцов

            new_columns = {col: dtype for col, dtype in data.items()if col not in existing_columns}
            if new_columns:
                for column, dtype in new_columns.items():
                    column_type = determine_column_type(dtype)
                    alter_query = f"ALTER TABLE {table_name} ADD COLUMN {column} {column_type};"
                    self.__cursor.execute(alter_query)

            # Вставка данных в таблицу
            column_str = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            insert_query = f"INSERT INTO {table_name} ({column_str}) VALUES ({placeholders});"
            self.__cursor.execute(insert_query, list(data.values()))
            self.__connection.commit()

        except Exception as e:
            self.__connection.rollback()
            print(f"Ошибка для добавления данных: {e}")
        finally:
            self.__connection.commit()

    def add_columns(self, table_name: str, columns: dict[str, any]):
        """
        Добавляет новые столбцы в таблицу.
        :param table_name: Название столбца
        :param columns: Словарь с данными (ключ: атрибут, значение: тип данных)
        """
        for column, dtype in columns.items():
            column_type = determine_column_type(dtype)
            alter_query = f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column} {column_type};"
            self.__cursor.execute(alter_query)
        self.__connection.commit()

    @handle_errors
    def update_for_current_product(self, table_name: str, user_identifier: dict[str, any],
                                update_data: dict[str, any]):
        """
        Обновляет данные для конкретного пользователя в таблице.

        :param table_name: Название таблицы.
        :param user_identifier: Условие для идентификации пользователя (например, {"id": 1}).
        :param update_data: Данные для обновления (ключ: название столбца, значение: новые данные).
        """
        # Формирование частей запроса
        set_clause = ', '.join(f"{key} = %s" for key in update_data.keys())
        where_clause = " AND ".join(f"{key} = %s" for key in user_identifier.keys())

        # Объединение значений для плейсхолдеров
        values = tuple(update_data.values()) + tuple(user_identifier.values())

        # Финальный SQL-запрос
        update_query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause};"

        # Выполнение запроса
        self.__cursor.execute(update_query, values)
        self.__connection.commit()
        print("Данные успешно обновлены!")

    def close_connection(self):
        """
        Закрывает соединение с базой данных.
        """
        self.__cursor.close()
        self.__connection.close()
