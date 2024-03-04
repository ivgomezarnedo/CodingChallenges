from abc import ABC, abstractmethod

class InputInterface(ABC):

    @abstractmethod
    def fetch_data(self, identifier: str):
        pass