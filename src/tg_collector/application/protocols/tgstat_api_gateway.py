from abc import abstractmethod
from typing import Protocol

from tg_collector.application.models import Post


class TGStatAPIGateway(Protocol):
    @abstractmethod
    def fetch_data(self, offset: int) -> list[Post | None]:
        raise NotImplementedError
