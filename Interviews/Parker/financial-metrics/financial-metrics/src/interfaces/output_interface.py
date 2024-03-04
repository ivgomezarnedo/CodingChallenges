from abc import ABC, abstractmethod

class OutputInterface(ABC):

    @abstractmethod
    def output_data(self, data):
        pass