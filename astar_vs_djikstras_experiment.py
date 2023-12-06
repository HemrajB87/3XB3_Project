import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from itertools import combinations
from final_project_part1 import DirectedWeightedGraph, dijkstra
import AstarAlgorithm as Astar

def read_csv_file(file_path, has_header=True):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        if has_header:
            next(reader, None)  # Skip the header row
        return [row for row in reader]

def create_graph(stations_data, connections_data):
    G = DirectedWeightedGraph()
    for station_id, latitude, longitude, *_ in stations_data:
        G.add_node(int(station_id))
    for station1, station2, line, time, *_ in connections_data:
        G.add_edge(int(station1), int(station2), int(time))
    return G

def run_experiment(graph, start_node, goal_node, nodes_info, num_measurements=1):
    dijkstra_times = []
    a_star_times = []

    for _ in range(num_measurements):
        # Run Dijkstra's algorithm
        start_time = time.time()
        dijkstra_result = dijkstra(graph, start_node)
        dijkstra_time = time.time() - start_time
        dijkstra_times.append(dijkstra_time)

        # Run A* algorithm
        heuristic = {node: Astar.heuristic(node, goal_node, nodes_info) for node in graph.adj}
        start_time = time.time()
        a_star_result = Astar.a_star(graph, start_node, goal_node, heuristic)
        a_star_time = time.time() - start_time
        a_star_times.append(a_star_time)

    avg_dijkstra_time = sum(dijkstra_times) / num_measurements
    avg_a_star_time = sum(a_star_times) / num_measurements

    return avg_dijkstra_time, avg_a_star_time

def plot_results_3d(dijkstra_times, a_star_times, start_nodes, goal_nodes):
    # Ensure start_nodes and goal_nodes are lists of the same length as dijkstra_times and a_star_times
    if not (len(start_nodes) == len(dijkstra_times) == len(a_star_times) == len(goal_nodes)):
        raise ValueError("Error: The list lengths do not match.")

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Convert start_nodes and goal_nodes to the correct format if they're not already lists
    start_nodes_list = list(start_nodes)
    goal_nodes_list = list(goal_nodes)

    # Scatter plots for each algorithm
    ax.scatter(start_nodes_list, goal_nodes_list, dijkstra_times, c='b', marker='o', label='Dijkstra')
    ax.scatter(start_nodes_list, goal_nodes_list, a_star_times, c='r', marker='x', label='A*')

    ax.set_xlabel('Starting Node')
    ax.set_ylabel('Goal Node')
    ax.set_zlabel('Runtime (seconds)')
    ax.set_title('Dijkstra vs A* Runtime Comparison (3D)')
    ax.legend()

    plt.show()

def main():
    stations_data = read_csv_file('london_stations.csv')
    connections_data = read_csv_file('london_connections.csv')
    graph = create_graph(stations_data, connections_data)
    nodes_info = {int(row[0]): (float(row[1]), float(row[2])) for row in stations_data}

    dijkstra_runtimes = []
    a_star_runtimes = []
    stations = list(graph.adj.keys())

    for start_node, goal_node in combinations(stations, 2):
        print(f"Running experiment for station {start_node} and goal node {goal_node}")
        avg_dijkstra_time, avg_a_star_time = run_experiment(graph, start_node, goal_node, nodes_info)
        dijkstra_runtimes.append(avg_dijkstra_time)
        a_star_runtimes.append(avg_a_star_time)

    plot_results_3d(dijkstra_runtimes, a_star_runtimes, stations, stations)

    assert len(dijkstra_runtimes) == len(a_star_runtimes) == len(stations) * (len(stations) - 1) / 2

    plot_results_3d(dijkstra_runtimes, a_star_runtimes, stations, stations)

if __name__ == "__main__":
    main()
