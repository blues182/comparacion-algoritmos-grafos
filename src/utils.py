import random
from graph import Graph

def generate_random_graph(num_nodes: int, connection_prob: float = 0.1) -> Graph:
    graph = Graph()
    
   
    for node in range(num_nodes):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        graph.add_node(node, x, y)
    
    
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < connection_prob:
                distance = graph.euclidean_distance(i, j)
                graph.add_edge(i, j, distance)
    
    return graph
