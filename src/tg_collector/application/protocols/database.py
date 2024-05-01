from abc import abstractmethod
from typing import Protocol, List, TypeVar


T = TypeVar('T')

class DataBaseGateway(Protocol):
    @abstractmethod
    def save_all(self, data: List[T]) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self) -> List[T]:
        raise NotImplementedError
