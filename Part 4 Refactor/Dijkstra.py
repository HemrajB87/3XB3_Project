from SPAlgorithm import SPAlgorithm
import sys
sys.path.append('./')
from final_project_part1 import dijkstra

class Dijkstra(SPAlgorithm):
    def calculate_spl(self, graph, source, destination):
        
        distances = dijkstra(graph, source)
        return distances[destination]