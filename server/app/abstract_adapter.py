from abc import ABC, abstractmethod
from odd_contract.models import DataEntity

from typing import List


class AbstractAdapter(ABC):
    def __init__(self, user: str, password: str, host: str, port: str, database: str) -> None:
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._database = database
        super().__init__()

    @abstractmethod
    def get_data_source_oddrn(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_datasets(self) -> List[DataEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_data_transformers(self) -> List[DataEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_data_transformer_runs(self) -> List[DataEntity]:
        raise NotImplementedError
