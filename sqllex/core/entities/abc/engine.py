from abc import ABC, abstractmethod


class AbstractEngine(ABC):

    class AbstractExtensions(ABC):
        @abstractmethod
        def new_type(self, *args, **kwargs):
            pass

        @abstractmethod
        def register_type(self, *args, **kwargs):
            pass

    @property
    @abstractmethod
    def extensions(self):
        pass

    @abstractmethod
    def connect(
            self,
            dbname=None,
            user=None,
            password=None,
            host=None,
            port=None,
            **kwargs
    ):
        pass

