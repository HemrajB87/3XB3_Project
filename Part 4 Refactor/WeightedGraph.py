class WeightedGraph(Graph):
    def __init__(self):
        self.adj = {}
        self.weights = {}

    def add_node(self, node: int):
        self.adj[node] = []

    def add_edge(self, start: int, end: int, weight: float):
        self.adj[start].append(end)
        self.weights[(start, end)] = weight

    def get_adjacent_nodes(self, node: int) -> List[int]:
        return self.adj[node]

    def get_number_of_nodes(self) -> int:
        return len(self.adj)

    def get_edge_weight(self, node1: int, node2: int) -> float:
        return self.weights.get((node1, node2), float('inf'))