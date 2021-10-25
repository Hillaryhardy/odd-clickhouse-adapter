import logging
from typing import List

from clickhouse_driver import connect
from odd_contract.models import DataEntity
from oddrn_generator import ClickHouseGenerator

from .mappers import _table_select, _column_select
from .mappers.tables import map_table


class ClickHouseAdapter:
    __connection = None
    __cursor = None

    def __init__(self, config) -> None:
        self.__host = config['ODD_HOST']
        self.__port = config['ODD_PORT']
        self.__database = config['ODD_DATABASE']
        self.__user = config['ODD_USER']
        self.__password = config['ODD_PASSWORD']
        self.__oddrn_generator = ClickHouseGenerator(host_settings=f"{self.__host}", databases=self.__database)

    def get_data_source_oddrn(self) -> str:
        return self.__oddrn_generator.get_data_source_oddrn()

    def get_datasets(self) -> List[DataEntity]:
        try:
            self.__connect()
            params = {
                "database": self.__database
            }
            tables = self.__execute(_table_select, params)
            columns = self.__execute(_column_select, params)

            return map_table(self.__oddrn_generator, tables, columns)
        except Exception as e:
            logging.error('Failed to load metadata for tables')
            logging.exception(e)
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

    def __connect(self):
        try:
            self.__connection = connect(
                database=self.__database,
                user=self.__user,
                password=self.__password,
                host=self.__host,
                port=self.__port
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
    pass
