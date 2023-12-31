import matplotlib.pyplot as plt
import time
import random
from itertools import combinations
import sys
sys.path.append('./Part 4 Refactor')
sys.path.append('./')
import AstarAlgorithm as Astar
from Dijkstra import Dijkstra as dijkstra
from final_project_part1 import DirectedWeightedGraph

def run_experiment(graph, start_node, goal_node, nodes_info, num_measurements=100):
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
        Astar.a_star(graph, start_node, goal_node, h)
        a_star_time = time.time() - start_time
        a_star_times.append(a_star_time)

    # Calculate average runtimes
    avg_dijkstra_time = sum(dijkstra_times) / num_measurements
    avg_a_star_time = sum(a_star_times) / num_measurements

    return avg_dijkstra_time, avg_a_star_time

def plot_results(start_nodes, goal_nodes, dijkstra_runtimes, a_star_runtimes):
    plt.figure(figsize=(12, 8))

    # Plot Dijkstra runtimes as a blue line
    plt.plot(range(len(start_nodes)), dijkstra_runtimes, 'b-', marker='o', label='Dijkstra')

    # Plot A* runtimes as a red line
    plt.plot(range(len(start_nodes)), a_star_runtimes, 'r-', marker='x', label='A*')

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
    start_nodes = [1,10,20,30,40,50,60]  # Specify specific start nodes
    goal_nodes = [65,55,45,35,25,15,5]  # Specify specific goal nodes

    # Iterate over specified start and goal nodes
    for start_node, goal_node in zip(start_nodes, goal_nodes):
        print(f"Running experiment for station {start_node} and goal node {goal_node}")
        avg_dijkstra_time, avg_a_star_time = run_experiment(graph, start_node, goal_node, nodes_info)
        dijkstra_runtimes.append(avg_dijkstra_time)
        a_star_runtimes.append(avg_a_star_time)

    # Plot results
    plot_results(start_nodes, goal_nodes, dijkstra_runtimes, a_star_runtimes)

if __name__ == "__main__":
    main()
