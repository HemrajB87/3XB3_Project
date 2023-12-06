from abc import ABC, abstractmethod


class SPAlgorithm(ABC):

    @abstractmethod
    def calculate_spl(self, graph, source, destination):
        pass