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
from collections import deque
import itertools 

def build_graph(connections_data):
    graph = DirectedWeightedGraph()
    for row in connections_data:
        station1, station2, weight = int(row[0]), int(row[1]), int(row[3])
        # Add nodes if they don't exist
        if station1 not in graph.adj:
            graph.add_node(station1)
        if station2 not in graph.adj:
            graph.add_node(station2)
        # Add the edge
        graph.add_edge(station1, station2, weight)
    return graph

#compute node pairs along a line
def run_experiment(graph, start_node, goal_node, nodes_info, num_measurements=1):
    dijkstra_times = []
    a_star_times = []
    for _ in range(num_measurements):
        # Debug print statement
        print(f"Running experiment for start_node={start_node}, goal_node={goal_node}")
        
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

    # Debug print statements
    print(f"Avg Dijkstra Time: {avg_dijkstra_time}")
    print(f"Avg A* Time: {avg_a_star_time}")

    return avg_dijkstra_time, avg_a_star_time


def plot_results(indices, dijkstra_runtimes, a_star_runtimes, title):
    # Debug print statements
    print(f"Indices: {indices}")
    print(f"Dijkstra Runtimes: {dijkstra_runtimes}")
    print(f"A* Runtimes: {a_star_runtimes}")
    print(f"Title: {title}")

    plt.figure(figsize=(12, 8))

    plt.plot(indices, dijkstra_runtimes, label='Dijkstra')
    plt.plot(indices, a_star_runtimes, label='A*')
    plt.xlabel('Experiment Index')
    plt.ylabel('Runtime (seconds)')
    plt.title(title)
    plt.legend()
    plt.show()



def get_stations_on_same_line(connections_data, line_number):
    stations = []
    current_line = None

    for row in connections_data:
        station1, station2, line = int(row[0]), int(row[1]), int(row[2])

        # Check if the line number changes
        if current_line is None:
            current_line = line
        elif current_line != line:
            current_line = line

        # Check if the current line matches the specified line_number
        if line == line_number:
            stations.append((station1, station2))

    return stations



def get_adjacent_line_pairs(connections_data):
    # Dictionary to hold the lines each station is on
    station_lines = {}
    for row in connections_data:
        station1, station2, line = int(row[0]), int(row[1]), int(row[2])
        if station1 not in station_lines:
            station_lines[station1] = set()
        if station2 not in station_lines:
            station_lines[station2] = set()
        station_lines[station1].add(line)
        station_lines[station2].add(line)

    # Find pairs where stations are on different lines but those lines intersect
    adjacent_line_pairs = []
    for station1, lines1 in station_lines.items():
        for station2, lines2 in station_lines.items():
            if station1 != station2 and not lines1.isdisjoint(lines2):
                adjacent_line_pairs.append((station1, station2))

    return adjacent_line_pairs


def get_station_pairs_requiring_transfers(connections_data):
    # Build a graph representation from the connections data
    graph = build_graph(connections_data)

    # Find all unique station pairs
    stations = list(graph.adj.keys())  # Use the keys of the adjacency dictionary

    # Find station pairs requiring transfers
    transfer_pairs = []
    for station1, station2 in itertools.combinations(stations, 2):
        if not is_direct_path(graph, station1, station2):
            transfer_pairs.append((station1, station2))

    return transfer_pairs



def is_direct_path(graph, start, end):
    # Initialize a queue and add the start node
    queue = deque([start])
    visited = set()

    # Perform BFS from the start node
    while queue:
        current_station = queue.popleft()
        visited.add(current_station)

        # If the end station is found, return True
        if current_station == end:
            return True

        # Add all unvisited adjacent stations to the queue
        for neighbor in graph.adj[current_station]:
            if neighbor not in visited:
                queue.append(neighbor)

    # If BFS completes without finding the end station, return False
    return False

def run_and_plot_scenario(graph, nodes_info, station_pairs, title):
    dijkstra_runtimes = []
    a_star_runtimes = []
    indices = []

    for index, (start_node, goal_node) in enumerate(station_pairs):
        print(f"Running {title.lower()} experiment for station {start_node} to {goal_node}")
        avg_dijkstra_time, avg_a_star_time = run_experiment(graph, start_node, goal_node, nodes_info)
        dijkstra_runtimes.append(avg_dijkstra_time)
        a_star_runtimes.append(avg_a_star_time)
        indices.append(index)

    # Plot results for the current scenario with the correct title
    plot_results(indices, dijkstra_runtimes, a_star_runtimes, title)



def main():
    # Load CSV data
    stations_data = Astar.read_csv_file('london_stations.csv')
    connections_data = Astar.read_csv_file('london_connections.csv')

    # Create graph from CSV data
    graph = build_graph(connections_data)
    for row in stations_data:
        graph.add_node(int(row[0]))

    for row in connections_data:
        graph.add_edge(int(row[0]), int(row[1]), int(row[3]))

    # Node information for heuristic function
    nodes_info = {int(row[0]): (float(row[1]), float(row[2])) for row in stations_data}

    # Run experiments
    dijkstra_runtimes = []
    a_star_runtimes = []

    # Scenario 1: Stations on the same line
    #same_line_stations = get_stations_on_same_line(connections_data, 1)
    #run_and_plot_scenario(graph, nodes_info, same_line_stations, "Same Line Scenario")

    # Scenario 2: Stations on adjacent lines
    '''adjacent_line_pairs = get_adjacent_line_pairs(connections_data)

    # Define the jump value
    jump = 100

    for index, (start_node, goal_node) in enumerate(adjacent_line_pairs):
        # Only run experiments at multiples of the jump value
        if index % jump == 0:
            print(f"Running {index}-th experiment for station {start_node} to {goal_node}")
            avg_dijkstra_time, avg_a_star_time = run_experiment(graph, start_node, goal_node, nodes_info)
            dijkstra_runtimes.append(avg_dijkstra_time)
            a_star_runtimes.append(avg_a_star_time)
    
    if dijkstra_runtimes:
        plot_results(list(range(0, len(dijkstra_runtimes) * jump, jump)), dijkstra_runtimes, a_star_runtimes, "Adjacent Line Scenario")
'''
    # Scenario 3: Stations requiring multiple transfers
    transfer_pairs = get_station_pairs_requiring_transfers(connections_data)
    run_and_plot_scenario(graph, nodes_info, transfer_pairs, "Transfer Scenario")

if __name__ == "__main__":
    main()
