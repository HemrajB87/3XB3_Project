import time
import pandas as pd
import matplotlib.pyplot as plt
import random
import itertools
from part3 import *
from final_project_part1 import *

def find_adjacent_line_pairs(connections_df):
    station_lines = {}
    for _, row in connections_df.iterrows():
        station_lines.setdefault(row['station1'], set()).add(row['line'])
        station_lines.setdefault(row['station2'], set()).add(row['line'])

    # Find pairs where stations are on different lines but those lines intersect
    adjacent_pairs = []
    for (station1, lines1), (station2, lines2) in itertools.combinations(station_lines.items(), 2):
        if lines1.intersection(lines2):  # Check if lines intersect
            adjacent_pairs.append((station1, station2))

    return adjacent_pairs

def run_adjacent_line_experiment(tube_graph, adjacent_pairs, iterations=10):
    results = []

    for iteration in range(iterations):
        for source, destination in random.sample(adjacent_pairs, min(1000, len(adjacent_pairs))):
            tube_graph.set_destination(destination)

            # Run A* Algorithm
            start_time = time.time()
            _, _ = a_star(tube_graph, source, destination, heuristic_wrapper)
            a_star_time = time.time() - start_time

            # Run Dijkstra's Algorithm
            start_time = time.time()
            _, _ = dijkstra2(tube_graph, source)
            dijkstra_time = time.time() - start_time

            results.append((iteration, source, destination, a_star_time, dijkstra_time))

    df = pd.DataFrame(results, columns=['Iteration', 'Source', 'Destination', 'A*_Time', 'Dijkstra_Time'])

    averaged_results = df.groupby(['Source', 'Destination']).mean().reset_index()

    return averaged_results

tube_graph = TubeGraph()

for index, row in stations_df.iterrows():
    tube_graph.add_station(station_id=row['id'], lat=row['latitude'], lon=row['longitude'])

for index, row in connections_df.iterrows():
    tube_graph.add_connection_by_distance(station1=row['station1'], station2=row['station2'])

tube_graph.initialize_adjacency()

adjacent_line_pairs = find_adjacent_line_pairs(connections_df)
print(adjacent_line_pairs)

experiment_results = run_adjacent_line_experiment(tube_graph, adjacent_line_pairs)

plt.figure(figsize=(10, 6))
plt.plot(experiment_results['A*_Time'], label='A*', linestyle='-')
plt.plot(experiment_results['Dijkstra_Time'], label='Dijkstra', linestyle='-')
plt.xlabel('Pair Index')
plt.ylabel('Time (seconds)')
plt.title('Performance Comparison on Adjacent Lines: A* vs Dijkstra')
plt.legend()
plt.show()