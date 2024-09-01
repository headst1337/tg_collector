from abc import abstractmethod
from typing import Protocol

from tg_collector.application.models import Post


class PostGateway(Protocol):
    @abstractmethod
    def save_all(self, data: list[Post]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Post]:
        raise NotImplementedError
