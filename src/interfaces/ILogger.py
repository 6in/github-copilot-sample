from abc import ABC, abstractmethod

class ILogger(ABC):
    @abstractmethod
    def info(self, msg: str):
        pass

    @abstractmethod
    def debug(self, msg: str):
        pass

    @abstractmethod
    def error(self, msg: str):
        pass
