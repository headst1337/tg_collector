from abc import abstractmethod
from typing import Protocol, TypeVar


T = TypeVar('T')


class GenerateDateReport(Protocol):
    @abstractmethod
    def genetare_report(self, dates: list[str]) -> str:
        raise NotImplementedError
