from abc import ABC, abstractmethod
from typing import List, Dict

class Graph(ABC):

    @abstractmethod
    def add_node(self, node: int):
        pass

    @abstractmethod
    def add_edge(self, start: int, end: int, weight: float):
        pass

    @abstractmethod
    def get_adjacent_nodes(self, node: int) -> List[int]:
        pass

    @abstractmethod
    def get_number_of_nodes(self) -> int:
        pass

    @abstractmethod
    def get_edge_weight(self, node1: int, node2: int) -> float:
        pass
