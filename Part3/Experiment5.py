import matplotlib.pyplot as plt
import time
import random
from itertools import combinations
import sys
sys.path.append('./Part 4 Refactor')
sys.path.append('./')
from AstarAdapter import A_Star_Adapter as AstarA
import AstarAlgorithm as Astar
from Dijkstra import Dijkstra as dijkstra
from final_project_part1 import DirectedWeightedGraph

#need several transfer 
def calculate_transfers(path):
    # Helper function to calculate the number of transfers in a path
    print(f"path:{path}")
    transfers = 0
    prev_line = None
    for station in path:
        line = station // 100  # Assuming stations are numbered with a line identifier in the hundreds place
        if prev_line is not None and prev_line != line:
            transfers += 1
        prev_line = line
    return transfers

def run_experiment(graph, start_node, goal_node, nodes_info, num_measurements=1):
    dijkstra_times = []
    a_star_times = []
    for _ in range(num_measurements):
        # Run Dijkstra's algorithm
        start_time = time.time()
        dijkstra.calculate_spl(dijkstra, graph, start_node, goal_node)
        dijkstra_time = time.time() - start_time
        dijkstra_times.append(dijkstra_time)

        # Run A* algorithm
        h = {node: Astar.heuristic(node, goal_node, nodes_info) for node in graph.adj}
        start_time = time.time()
        a_star_result, _ = Astar.a_star(graph, start_node, goal_node, h)
        a_star_time = time.time() - start_time
        a_star_times.append(a_star_time)

    # Calculate average runtimes
    avg_dijkstra_time = sum(dijkstra_times) / num_measurements
    avg_a_star_time = sum(a_star_times) / num_measurements

    return avg_dijkstra_time, avg_a_star_time

def plot_results(start_nodes, goal_nodes, dijkstra_runtimes, a_star_runtimes):
    plt.figure(figsize=(12, 8))

    for i, (start_node, goal_node) in enumerate(zip(start_nodes, goal_nodes)):
        plt.scatter(i, dijkstra_runtimes[i], c='b', marker='o', label=f'Dijkstra {start_node}-{goal_node}')
        plt.scatter(i, a_star_runtimes[i], c='r', marker='x', label=f'A* {start_node}-{goal_node}')

    plt.xlabel('Experiment Index')
    plt.ylabel('Runtime (seconds)')
    plt.title('Dijkstra vs A* Runtime Comparison')
    plt.legend()
    plt.show()

def main():
    # Load CSV data
    stations_data = Astar.read_csv_file('london_stations.csv')
    connections_data = Astar.read_csv_file('london_connections.csv')

    # Create graph from CSV data
    graph = DirectedWeightedGraph()
    for row in stations_data:
        graph.add_node(int(row[0]))

    for row in connections_data:
        graph.add_edge(int(row[0]), int(row[1]), int(row[3]))

    # Node information for heuristic function
    nodes_info = {int(row[0]): (float(row[1]), float(row[2])) for row in stations_data}

    # Run experiments
    dijkstra_runtimes = []
    a_star_runtimes = []

    # Specify the number of measurements and the threshold for transfers
    num_measurements = 500
    transfer_threshold = 2  # Adjust this threshold as needed

    # Generate random node pairs until we have enough pairs with the specified number of transfers
    while len(dijkstra_runtimes) < num_measurements:
        start_node, goal_node = random.sample(list(graph.adj.keys()), 2)
        avg_dijkstra_time, avg_a_star_time = run_experiment(graph, start_node, goal_node, nodes_info)

        # Check if the number of transfers exceeds the threshold
        dijkstra_path = dijkstra.calculate_spl(dijkstra, graph, start_node, goal_node)
        if calculate_transfers(dijkstra_path) > transfer_threshold:
            dijkstra_runtimes.append(avg_dijkstra_time)
            a_star_runtimes.append(avg_a_star_time)

    # Plot results
    plot_results(start_nodes, goal_nodes, dijkstra_runtimes, a_star_runtimes)

if __name__ == "__main__":
    main()
