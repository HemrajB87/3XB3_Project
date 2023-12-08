import time
import pandas as pd
import matplotlib.pyplot as plt
from part3 import *
from final_project_part1 import *

def run_same_line_experiment(tube_graph, connections_df, iterations=1):
    results = []

    # Filter for station pairs that are on the same line
    same_line_pairs = connections_df[connections_df['line'].duplicated(keep=False)]
    print(same_line_pairs)

    for iteration in range(iterations):
        for _, row in same_line_pairs.iterrows():
            source, destination = row['station1'], row['station2']
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

for index, row in connections_df.iterrows():
    tube_graph.add_connection_by_distance(station1=row['station1'], station2=row['station2'])

tube_graph.initialize_adjacency()

experiment_results = run_same_line_experiment(tube_graph, connections_df)

plt.figure(figsize=(10, 6))
plt.plot(experiment_results['A*_Time'], label='A*', linestyle='-')
plt.plot(experiment_results['Dijkstra_Time'], label='Dijkstra', linestyle='-')
plt.xlabel('Pair Index')
plt.ylabel('Time (seconds)')
plt.title('Performance Comparison on Same Line using Distance: A* vs Dijkstra')
plt.legend()
plt.show()