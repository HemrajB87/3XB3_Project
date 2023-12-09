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

#compute node pairs along a line
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

    # Create an index array for the x-axis
    indices = list(range(len(start_nodes)))

    # Plot Dijkstra and A* times as line graphs
    plt.plot(indices, dijkstra_runtimes, 'b-o', label='Dijkstra')  # Blue line with circle markers
    plt.plot(indices, a_star_runtimes, 'r-x', label='A*')  # Red line with x markers

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
    
    # Specify the start and end node indices for the line
    start_index = 1
    end_index = 30
    
    # Generate node pairs along the line
    start_goal_pairs = [(i, i+1) for i in range(start_index, end_index)]

    for start_goal_pair in start_goal_pairs:
        start_node, goal_node = start_goal_pair
        print(f"Running experiment for station {start_node} and goal node {goal_node}")
        avg_dijkstra_time, avg_a_star_time = run_experiment(graph, start_node, goal_node, nodes_info)
        dijkstra_runtimes.append(avg_dijkstra_time)
        a_star_runtimes.append(avg_a_star_time)

    # Plot results
    plot_results(start_goal_pairs, start_goal_pairs, dijkstra_runtimes, a_star_runtimes)

if __name__ == "__main__":
    main()
