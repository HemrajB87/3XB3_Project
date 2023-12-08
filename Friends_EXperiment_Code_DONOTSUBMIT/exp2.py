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
        counter = 0
        for source, destination in pairs:
            tube_graph.set_destination(destination)

            # Run A* Algorithm
            start_time = time.time()
            _, path_a_star = a_star(tube_graph, source, destination, heuristic_wrapper)
            a_star_time = time.time() - start_time

            # Run Dijkstra's Algorithm
            start_time = time.time()
            _, _ = dijkstra2(tube_graph, source)
            dijkstra_time = time.time() - start_time

            results.append((iteration, source, destination, a_star_time, dijkstra_time))
            counter += 1

    df = pd.DataFrame(results, columns=['Iteration', 'Source', 'Destination', 'A*_Time', 'Dijkstra_Time'])
    return df.groupby(['Source', 'Destination']).mean().reset_index()

all_stations = list(tube_graph.coordinates.keys())
all_pairs = list(itertools.product(all_stations, repeat=2))

experiment_results = run_experiment(tube_graph, all_pairs, iterations=1)

plt.figure(figsize=(10, 6))
plt.plot(experiment_results['A*_Time'], label='A*', linestyle='-')
plt.plot(experiment_results['Dijkstra_Time'], label='Dijkstra', linestyle='-')
plt.xlabel('Pair Index')
plt.ylabel('Average Time (seconds)')
plt.title('Performance Comparison: A* vs Dijkstra')
plt.legend()
plt.show()