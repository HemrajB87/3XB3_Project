import final_project_part1
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

# note to self: check previous labs to fix anything with plots

# EXPERIMENT 1
def experiment_kValues(G, source, k_values, trials):

    d_avg_values = []
    b_avg_values = []

    for k in k_values:
        dijkstra_distances = []
        bellman_ford_distances = []

        for _ in range(trials):
            dijkstra_dist = final_project_part1.dijkstra_approx(G, source, k)
            bellman_ford_dist = final_project_part1.bellman_ford_approx(G, source, k)

            dijkstra_distances.append(final_project_part1.total_dist(dijkstra_dist))
            bellman_ford_distances.append(final_project_part1.total_dist(bellman_ford_dist))

        avg_dijkstra_distance = np.mean(dijkstra_distances)
        avg_bellman_ford_distance = np.mean(bellman_ford_distances)

        d_avg_values.append(avg_dijkstra_distance)
        b_avg_values.append(avg_bellman_ford_distance)

    plt.plot(k_values, d_avg_values, label='Dijkstra_approx', marker='o', linestyle='-')
    plt.plot(k_values, b_avg_values, label='Bellman_Ford_approx', marker='o', linestyle='-')

    plt.xlabel('Number of Relaxation Steps (k)')
    plt.ylabel('Average Total Distance')
    plt.title(f'Approx Algorithms with Different k Values')
    plt.legend()
    plt.grid(True)
    plt.show()

ran_graph = final_project_part1.create_random_complete_graph(20, 25)
k_values = [0,1, 2, 3, 4, 5, 6]
experiment_kValues(ran_graph, 0, k_values, 15)

# EXPERIMENT 2
def experiment_numberOfNodes():
    nodes = [10,20,30,40,50]
    k_values = [2]
    trials =15

    for k in k_values:
        dijkstra_distances2 = []
        bellman_ford_distances2 = []
        dijkstra_distances2_original = []
        bellman_ford_distances2_original = []

        for node in nodes:
            trial_dijkstra_distances = []
            trial_bellman_ford_distances = []
            trial_dijkstra_distances_original = []
            trial_bellman_ford_distances_original = []

            for _ in range(trials):
                graph = final_project_part1.create_random_complete_graph(node, 15)
                source_node = 0

                dist_dijkstra = final_project_part1.dijkstra_approx(graph, source_node, k)
                dist_bellman_ford = final_project_part1.bellman_ford_approx(graph, source_node, k)

                dist_dijkstra_original = final_project_part1.dijkstra(graph, source_node)
                dist_bellman_ford_original = final_project_part1.bellman_ford(graph, source_node)

                trial_dijkstra_distances.append(np.mean(final_project_part1.total_dist(dist_dijkstra)))
                trial_bellman_ford_distances.append(np.mean(final_project_part1.total_dist(dist_bellman_ford)))

                trial_dijkstra_distances_original.append(np.mean(final_project_part1.total_dist(dist_dijkstra_original)))
                trial_bellman_ford_distances_original.append(np.mean(final_project_part1.total_dist(dist_bellman_ford_original)))


            dijkstra_distances2.append(np.mean(trial_dijkstra_distances))
            bellman_ford_distances2.append(np.mean(trial_bellman_ford_distances))

            dijkstra_distances2_original.append(np.mean(trial_dijkstra_distances_original))
            bellman_ford_distances2_original.append(np.mean(trial_bellman_ford_distances_original))

        plt.plot(nodes, dijkstra_distances2, label=f'Dijkstra_approx (k={k})', marker='o')
        plt.plot(nodes, bellman_ford_distances2, label=f'Bellman_Ford_approx (k={k})', marker='o')


    dijkstra_distances2_original = []
    bellman_ford_distances2_original = []

    for node in nodes:

        trial_dijkstra_distances_original = []
        trial_bellman_ford_distances_original = []

        for _ in range(trials):
            graph = final_project_part1.create_random_complete_graph(node, 15)
            source_node = 0

            dist_dijkstra_original = final_project_part1.dijkstra(graph, source_node)
            dist_bellman_ford_original = final_project_part1.bellman_ford(graph, source_node)

            trial_dijkstra_distances_original.append(np.mean(final_project_part1.total_dist(dist_dijkstra_original)))
            trial_bellman_ford_distances_original.append(np.mean(final_project_part1.total_dist(dist_bellman_ford_original)))


        dijkstra_distances2_original.append(np.mean(trial_dijkstra_distances_original))
        bellman_ford_distances2_original.append(np.mean(trial_bellman_ford_distances_original))

    plt.plot(nodes, dijkstra_distances2_original, label=f'Dijkstra', marker='o')
    plt.plot(nodes, bellman_ford_distances2_original, label=f'Bellman_Ford', marker='o')


    plt.xlabel('Number of Nodes')
    plt.ylabel('Average Total Distance')
    plt.title('Approx Algorithms with Different Node Values')
    plt.legend()
    plt.show()

experiment_numberOfNodes()

# EXPERIMENT 3

def experiment_sourceNodes(G, sources, k, trials):

    d_avg_values = []
    b_avg_values = []

    for source in sources:
        dijkstra_distances = []
        bellman_ford_distances = []

        for _ in range(trials):
            dijkstra_dist = final_project_part1.dijkstra_approx(G, source, k)
            bellman_ford_dist = final_project_part1.bellman_ford_approx(G, source, k)

            dijkstra_distances.append(final_project_part1.total_dist(dijkstra_dist))
            bellman_ford_distances.append(final_project_part1.total_dist(bellman_ford_dist))

        avg_dijkstra_distance = np.mean(dijkstra_distances)
        avg_bellman_ford_distance = np.mean(bellman_ford_distances)

        d_avg_values.append(avg_dijkstra_distance)
        b_avg_values.append(avg_bellman_ford_distance)

    plt.plot(sources, d_avg_values, label='Dijkstra_approx', marker='o', linestyle='-')
    plt.plot(sources, b_avg_values, label='Bellman_Ford_approx', marker='o', linestyle='-')

    plt.xlabel('Source Nodes')
    plt.ylabel(f'Average Total Distance')
    plt.title('Approx Algorithms with Different Source Nodes')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage:
ran_graph = final_project_part1.create_random_complete_graph(20, 25)
source_nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
k_value = 3
experiment_sourceNodes(ran_graph, source_nodes, k_value, 15)
