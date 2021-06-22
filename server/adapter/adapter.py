import logging

from clickhouse_driver import connect

from odd_contract.models import DataEntity
from adapter import _table_select, _column_select
from adapter.table import _map_table

from app.abstract_adapter import AbstractAdapter
from app.oddrn import generate_database_oddrn

from typing import List



def create_adapter(user: str, password: str, host: str, port: str, database: str) -> AbstractAdapter:
    return ClickHouseAdapter(user, password, host, port, database)


class ClickHouseAdapter(AbstractAdapter):
    __connection = None
    __cursor = None

    def __init__(self, user: str, password: str, host: str, port: str, database: str) -> None:
        super().__init__(user, password, host, port, database)

    def get_data_source_oddrn(self) -> str:
        return generate_database_oddrn(self._database)

    def get_datasets(self) -> List[DataEntity]:
        try:
            self.__connect()

            params = {
                "database": self._database
            }

            tables = self.__execute(_table_select, params)
            columns = self.__execute(_column_select, params)

            return _map_table(tables, columns)
        except Exception:
            logging.error('Failed to load metadata for tables')
            logging.exception(Exception)
        finally:
            self.__disconnect()
        return []

    def get_data_transformers(self) -> List[DataEntity]:
        return []

    def get_data_transformer_runs(self) -> List[DataEntity]:
        return []

    def __execute(self, query: str, params: dict = None) -> List[tuple]:
        self.__cursor.execute(query, params)
        records = self.__cursor.fetchall()
        return records

    def __execute_sql(self, query) -> List[tuple]:
        self.__cursor.execute(query)
        records = self.__cursor.fetchall()
        return records

    def __connect(self):
        try:
            print(self._user)
            self.__connection = connect(
                database=self._database,
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port
            )

            self.__cursor = self.__connection.cursor()

        except Exception as err:
            logging.error(err)
            raise DBException('Database error')

    def __disconnect(self):
        self.__close_cursor()
        self.__close_connection()

    def __close_cursor(self):
        try:
            if self.__cursor:
                self.__cursor.close()
        except Exception:
            pass

    def __close_connection(self):
        try:
            if self.__connection:
                self.__connection.close()
        except Exception:
            pass


class DBException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
