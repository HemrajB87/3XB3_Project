from WeightedGraph import WeightedGraph


class HeuristicGraph(WeightedGraph):
    def __init__(self):
        super().__init__()
        self.heuristic = {}

    def get_heuristic(self, node: int) -> dict[int, float]:
        return self.heuristic