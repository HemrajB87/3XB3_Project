class HeuristicGraph(WeightedGraph):
    def __init__(self):
        super().__init__()
        self.heuristic = {}

    def get_heuristic(self, node: int) -> Dict[int, float]:
        return self.heuristic