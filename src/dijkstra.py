import heapq
import time
from typing import Dict, List, Tuple, Optional

def dijkstra(graph, start: int, goal: int) -> Tuple[Optional[List[int]], float, int, float]:
    start_time = time.perf_counter()
    
    dist = {node: float('inf') for node in graph.adjacency_list}
    prev = {node: None for node in graph.adjacency_list}
    dist[start] = 0
    
    pq = [(0, start)]
    nodes_expanded = 0
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        nodes_expanded += 1
        
        if current_node == goal:
            break
        
        if current_dist > dist[current_node]:
            continue
        
        for neighbor, weight in graph.get_neighbors(current_node):
            new_dist = current_dist + weight
            
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current_node
                heapq.heappush(pq, (new_dist, neighbor))
    
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()
    
    if path[0] != start:
        path = None
    
    execution_time = time.perf_counter() - start_time
    
    return path, dist.get(goal, float('inf')), nodes_expanded, execution_time
