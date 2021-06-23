import os
import logging
from typing import Any


class MissingEnvironmentVariable(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


def get_env(env: str, default_value: Any = None) -> str:
    try:
        return os.environ[env]
    except KeyError:
        if default_value is not None:
            return default_value
        raise MissingEnvironmentVariable(f'{env} does not exist')


class BaseConfig:
    ODD_HOST = get_env('CLICKHOUSE_HOST', get_env('ODD_DATA_SOURCE_NAME', 'localhost'))
    ODD_PORT = get_env('CLICKHOUSE_PORT', '9000')
    ODD_DATABASE = get_env('CLICKHOUSE_DATABASE', 'default')
    ODD_USER = get_env('CLICKHOUSE_USER', None)
    ODD_PASSWORD = get_env('CLICKHOUSE_PASSWORD', None)
    ODD_SOURCE = get_env('ODD_DATA_SOURCE', 'clickhouse')

    SCHEDULER_INTERVAL_MINUTES = get_env('SCHEDULER_INTERVAL_MINUTES', 60)

    CLOUD_TYPE = "aws"
    CLOUD_REGION = "region_1"
    CLOUD_ACCOUNT = "account_1"

    CLOUD = {
        "type": CLOUD_TYPE,
        "region": CLOUD_REGION,
        "account": CLOUD_ACCOUNT
    }

class DevelopmentConfig(BaseConfig):
    FLASK_DEBUG = True


class ProductionConfig(BaseConfig):
    FLASK_DEBUG = True


def log_env_vars(config: dict):
    logging.info('Environment variables:')
    logging.info(f'ODD_SOURCE={config["ODD_SOURCE"]}')
    logging.info(f'CLICKHOUSE_HOST={config["ODD_HOST"]}')
    logging.info(f'CLICKHOUSE_PORT={config["ODD_PORT"]}')
    logging.info(f'CLICKHOUSE_DATABASE={config["ODD_DATABASE"]}')
    logging.info(f'CLICKHOUSE_USER={config["ODD_USER"]}')
    if config["ODD_PASSWORD"] != '':
        logging.info('CLICKHOUSE_PASSWORD=***')
    logging.info(f'SCHEDULER_INTERVAL_MINUTES={config["SCHEDULER_INTERVAL_MINUTES"]}')
    logging.info(f'CLOUD={config["CLOUD"]}')
