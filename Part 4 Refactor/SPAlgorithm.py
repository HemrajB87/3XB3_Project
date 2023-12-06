class SPAlgorithm(ABC):

    @abstractmethod
    def calculate_spl(self, graph: Graph, source: int, destination: int) -> float:
        pass