import heapq
import time
from typing import Dict, List, Tuple, Optional

def astar(graph, start: int, goal: int) -> Tuple[Optional[List[int]], float, int, float]:
    start_time = time.perf_counter()
    
    g_score = {node: float('inf') for node in graph.adjacency_list}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph.adjacency_list}
    f_score[start] = graph.euclidean_distance(start, goal)
    
    prev = {node: None for node in graph.adjacency_list}
    
    pq = [(f_score[start], start)]
    nodes_expanded = 0
    
    while pq:
        current_f, current_node = heapq.heappop(pq)
        nodes_expanded += 1
        
        if current_node == goal:
            break
        
        for neighbor, weight in graph.get_neighbors(current_node):
            tentative_g = g_score[current_node] + weight
            
            if tentative_g < g_score[neighbor]:
                prev[neighbor] = current_node
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + graph.euclidean_distance(neighbor, goal)
                heapq.heappush(pq, (f_score[neighbor], neighbor))
    
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()
    
    if path[0] != start:
        path = None
    
    execution_time = time.perf_counter() - start_time
    
    return path, g_score.get(goal, float('inf')), nodes_expanded, execution_time
