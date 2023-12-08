import time
import pandas as pd
import matplotlib.pyplot as plt
import random
import itertools
from part3 import *
from final_project_part1 import *

def run_experiment(tube_graph, pairs, iterations=1):
    results = []

    for iteration in range(iterations):
        for source, destination in pairs:
            tube_graph.set_destination(destination)

            # Run A* Algorithm
            start_time = time.time()
            _, _ = a_star(tube_graph, source, destination, heuristic_wrapper)
            a_star_time = time.time() - start_time

            # Run Dijkstra's Algorithm
            start_time = time.time()
            _, _ = dijkstra2(tube_graph, source)
            dijkstra_time = time.time() - start_time

            results.append((source, destination, a_star_time, dijkstra_time))

    return pd.DataFrame(results, columns=['Source', 'Destination', 'A*_Time', 'Dijkstra_Time'])

tube_graph = TubeGraph()

for index, row in stations_df.iterrows():
    tube_graph.add_station(station_id=row['id'], lat=row['latitude'], lon=row['longitude'])

# Load connections with time as edge weight
for index, row in connections_df.iterrows():
    tube_graph.add_connection_by_time(station1=row['station1'], station2=row['station2'], time=row['time'])

tube_graph.initialize_adjacency()

all_stations = list(tube_graph.coordinates.keys())
random_pairs = random.sample(list(itertools.product(all_stations, repeat=2)), 1000)

experiment_results = run_experiment(tube_graph, random_pairs)

plt.figure(figsize=(10, 6))
plt.plot(experiment_results['A*_Time'], label='A*', linestyle='-')
plt.plot(experiment_results['Dijkstra_Time'], label='Dijkstra', linestyle='-')
plt.xlabel('Pair Index')
plt.ylabel('Time (seconds)')
plt.title('Performance Comparison using Time as Edge Weight: A* vs Dijkstra')
plt.legend()
plt.show()