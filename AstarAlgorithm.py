import csv
from final_project_part1 import DirectedWeightedGraph
from min_heap2 import MinHeap, Element
import math

# Function to calculate distance between two coordinates (Haversine)
def calculate_distance(coord1, coord2):
    R = 6371  # Earth radius in kilometers
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

# Heuristic function for A* algorithm
def heuristic(node, goal, nodes_info):
    node_coord = nodes_info[node]
    goal_coord = nodes_info[goal]
    return calculate_distance(node_coord, goal_coord)

# A* algorithm implementation
def a_star(G, start, goal, h):
    pred = {}
    dist = {node: float('inf') for node in G.adj}
    dist[start] = 0

    Q = MinHeap([Element(node, float('inf')) for node in G.adj if node != start])
    Q.insert(Element(start, h[start]))

    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value

        if current_node == goal:
            break

        for neighbour in G.adjacent_nodes(current_node):
            alt = dist[current_node] + G.w(current_node, neighbour)
            if alt < dist[neighbour]:
                dist[neighbour] = alt
                pred[neighbour] = current_node
                Q.decrease_key(neighbour, alt + h.get(neighbour, float('inf')))

    path = reconstruct_path(pred, start, goal)
    if path[-1] == start:
        print("There is no path between the two given nodes.")
    return pred, path

# Function to reconstruct the shortest path
def reconstruct_path(pred, start, goal):
    print("Backtracking path from", goal)
    current = goal
    while current != start and current in pred:
        print(f"Current: {current}, Pred: {pred[current]}")
        current = pred[current]
    print("Pred dictionary:", pred)  # Debug print
    path = []
    current = goal
    while current != start and current in pred:
        path.append(current)
        current = pred[current]
    path.append(start)
    path.reverse()
    return path

def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header row
        return [row for row in reader]

# Load CSV data using csv module
stations_data = read_csv_file('london_stations.csv')
connections_data = read_csv_file('london_connections.csv')

# Create graph from CSV data
G = DirectedWeightedGraph()
for row in stations_data:
    G.add_node(int(row[0]))  # Assuming first column is the node ID

for row in connections_data:
    G.add_edge(int(row[0]), int(row[1]), int(row[3]))  # Adjust indices based on your CSV structure

# Node information for heuristic function
nodes_info = {int(row[0]): (float(row[1]), float(row[2])) for row in stations_data}  # Adjust indices for latitude and longitude

# Define start and goal nodes for testing
start_node = 11 
goal_node = 83  

# Heuristic function for each node
h = {node: heuristic(node, goal_node, nodes_info) for node in G.adj}

# Run A* algorithm
pred, path = a_star(G, start_node, goal_node, h)

# Output the shortest path
print("Shortest path from {} to {}: {}".format(start_node, goal_node, path))
