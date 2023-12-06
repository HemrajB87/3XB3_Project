class ShortPathFinder:
    def __init__(self):
        self.graph = None
        self.algorithm = None

    def set_graph(self, graph: Graph):
        self.graph = graph

    def set_algorithm(self, algorithm: SPAlgorithm):
        self.algorithm = algorithm

    def calc_short_path(self, source: int, destination: int) -> float:
        if self.graph is None or self.algorithm is None:
            raise ValueError("Graph and algorithm must be set before calculating the shortest path.")
        return self.algorithm.calculate_spl(self.graph, source, destination)
