from abc import abstractmethod
from typing import Protocol


class ExternalAPIGateway(Protocol):
    @abstractmethod
    def fetch_data(self, offset: int) -> dict:
        raise NotImplementedError
