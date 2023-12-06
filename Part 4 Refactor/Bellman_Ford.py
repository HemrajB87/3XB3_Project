import SPAlgorithm
from final_project_part1 import bellman_ford

class Bellman_Ford(SPAlgorithm):
    def calculate_spl(self, graph, source, destination):
        # Use the existing Bellman_Ford implementation from your code
        distances = bellman_ford(graph, source)
        return distances[destination]