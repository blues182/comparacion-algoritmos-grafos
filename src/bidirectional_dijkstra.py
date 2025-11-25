import heapq
import time
from typing import Dict, List, Tuple, Optional

def bidirectional_dijkstra(graph, start: int, goal: int) -> Tuple[Optional[List[int]], float, int, float]:
    start_time = time.perf_counter()
    
    dist_forward = {node: float('inf') for node in graph.adjacency_list}
    dist_forward[start] = 0
    prev_forward = {node: None for node in graph.adjacency_list}
    pq_forward = [(0, start)]
    
    dist_backward = {node: float('inf') for node in graph.adjacency_list}
    dist_backward[goal] = 0
    prev_backward = {node: None for node in graph.adjacency_list}
    pq_backward = [(0, goal)]
    
    meeting_node = None
    best_distance = float('inf')
    nodes_expanded = 0
    
    visited_forward = set()
    visited_backward = set()
    
    while pq_forward and pq_backward:
        if pq_forward:
            current_dist_f, current_node_f = heapq.heappop(pq_forward)
            nodes_expanded += 1
            
            if current_node_f in visited_forward:
                continue
            visited_forward.add(current_node_f)
            
            if current_node_f in visited_backward:
                total_dist = dist_forward[current_node_f] + dist_backward[current_node_f]
                if total_dist < best_distance:
                    best_distance = total_dist
                    meeting_node = current_node_f
            
            for neighbor, weight in graph.get_neighbors(current_node_f):
                new_dist = dist_forward[current_node_f] + weight
                if new_dist < dist_forward[neighbor]:
                    dist_forward[neighbor] = new_dist
                    prev_forward[neighbor] = current_node_f
                    heapq.heappush(pq_forward, (new_dist, neighbor))
        
        if pq_backward:
            current_dist_b, current_node_b = heapq.heappop(pq_backward)
            nodes_expanded += 1
            
            if current_node_b in visited_backward:
                continue
            visited_backward.add(current_node_b)
            
            if current_node_b in visited_forward:
                total_dist = dist_forward[current_node_b] + dist_backward[current_node_b]
                if total_dist < best_distance:
                    best_distance = total_dist
                    meeting_node = current_node_b
            
            for neighbor, weight in graph.get_neighbors(current_node_b):
                new_dist = dist_backward[current_node_b] + weight
                if new_dist < dist_backward[neighbor]:
                    dist_backward[neighbor] = new_dist
                    prev_backward[neighbor] = current_node_b
                    heapq.heappush(pq_backward, (new_dist, neighbor))
        
        if (pq_forward and pq_backward and 
            best_distance <= pq_forward[0][0] + pq_backward[0][0]):
            break
    
    if meeting_node is not None:
        path_forward = []
        current = meeting_node
        while current is not None:
            path_forward.append(current)
            current = prev_forward[current]
        path_forward.reverse()
        
        path_backward = []
        current = prev_backward[meeting_node]
        while current is not None:
            path_backward.append(current)
            current = prev_backward[current]
        
        path = path_forward + path_backward
    else:
        path = None
        best_distance = float('inf')
    
    execution_time = time.perf_counter() - start_time
    
    return path, best_distance, nodes_expanded, execution_time
