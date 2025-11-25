import math
import random
from typing import Dict, List, Tuple

class Graph:
    def __init__(self):
        self.adjacency_list: Dict[int, List[Tuple[int, float]]] = {}
        self.coordinates: Dict[int, Tuple[float, float]] = {}
    
    def add_node(self, node: int, x: float, y: float):
        self.adjacency_list[node] = []
        self.coordinates[node] = (x, y)
    
    def add_edge(self, node1: int, node2: int, weight: float):
        self.adjacency_list[node1].append((node2, weight))
        self.adjacency_list[node2].append((node1, weight))
    
    def get_neighbors(self, node: int) -> List[Tuple[int, float]]:
        return self.adjacency_list.get(node, [])
    
    def euclidean_distance(self, node1: int, node2: int) -> float:
        x1, y1 = self.coordinates[node1]
        x2, y2 = self.coordinates[node2]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
