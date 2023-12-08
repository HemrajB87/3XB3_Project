import time
import pandas as pd
import matplotlib.pyplot as plt
import random
import itertools
from part3 import *
from final_project_part1 import *

def run_experiment(tube_graph, pairs, iterations=5, use_random=False, num_pairs=1000):
    results = []

    if use_random and num_pairs < len(pairs):
        pairs = random.sample(pairs, num_pairs)

    for iteration in range(iterations):
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

    df = pd.DataFrame(results, columns=['Iteration', 'Source', 'Destination', 'A*_Time', 'Dijkstra_Time'])
    return df.groupby(['Source', 'Destination']).mean().reset_index()

# Generate all possible pairs
all_stations = list(tube_graph.coordinates.keys())
all_pairs = list(itertools.product(all_stations, repeat=2))

experiment_results = run_experiment(tube_graph, all_pairs, iterations=10, use_random=True, num_pairs=1000)

plt.figure(figsize=(10, 6))
plt.plot(experiment_results['A*_Time'], label='A*', linestyle='-')
plt.plot(experiment_results['Dijkstra_Time'], label='Dijkstra', linestyle='-')
plt.xlabel('Pair Index')
plt.ylabel('Average Time (seconds)')
plt.title('Performance Comparison: A* vs Dijkstra')
plt.legend()
plt.show()