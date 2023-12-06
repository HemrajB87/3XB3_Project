import SPAlgorithm
from final_project_part1 import dijkstra

class Dijkstra(SPAlgorithm):
    def calculate_spl(self, graph, source, destination):
        # Use the existing Dijkstra implementation from your code
        distances = dijkstra(graph, source)
        return distances[destination]