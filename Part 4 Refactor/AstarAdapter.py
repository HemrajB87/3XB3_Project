# A_Star adapter class
import sys
sys.path.append('./')
from AstarAlgorithm import a_star, heuristic
from SPAlgorithm import SPAlgorithm

class A_Star_Adapter(SPAlgorithm):
    def __init__(self, nodes_info):
        self.nodes_info = nodes_info

    def calculate_spl(self, graph, source, destination):
        heuristic_func = lambda node: heuristic(node, destination, self.nodes_info)
        _, path = a_star(graph, source, destination, heuristic_func)
        
        if not path or path[-1] != destination:
            raise ValueError("No path found")
        return path  
