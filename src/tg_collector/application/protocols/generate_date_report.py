from abc import abstractmethod
from typing import Protocol, List, TypeVar
from io import BytesIO


T = TypeVar('T')

class GenerateDateReport(Protocol):
    @abstractmethod
    def genetare_report(self, dates: List[str]) -> str:
        raise NotImplementedError
