from oddrn import Generator
from config import BaseConfig

generator = Generator(data_source=BaseConfig.ODD_SOURCE, cloud=BaseConfig.CLOUD)


def generate_database_oddrn(database_name: str) -> str:
    return generator.get_database(database_name)


def generate_table_oddrn(database_name: str, table_name: str) -> str:
    return generator.get_table(database_name, table_name)


def generate_column_oddrn(database_name: str, table_name: str, column_name: str) -> str:
    return generator.get_column(database_name, table_name, column_name)
