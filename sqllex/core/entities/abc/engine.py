from abc import ABC, abstractmethod
from sqllex.core.entities.abc.connection import AbstractConnection


class AbstractEngine(ABC):

    @abstractmethod
    def connect(self) -> AbstractConnection:
        pass
