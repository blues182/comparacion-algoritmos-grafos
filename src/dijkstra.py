# src/dijkstra.py
import math
import heapq

from src.utils import PathResult, reconstruct_path


def dijkstra(graph, start, goal) -> PathResult:
    """
    Algoritmo de Dijkstra clásico con priority queue.
    No mide tiempo (eso lo hace utils.run_with_timing).
    """
    dist = {node: math.inf for node in graph.adj}
    dist[start] = 0.0

    parents = {start: None}
    visited = set()
    pq = [(0.0, start)]
    nodes_expanded = 0

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        nodes_expanded += 1

        if u == goal:
            break

        for v, w in graph.neighbors(u):
            new_cost = d + w
            if new_cost < dist[v]:
                dist[v] = new_cost
                parents[v] = u
                heapq.heappush(pq, (new_cost, v))

    path = reconstruct_path(parents, start, goal)
    cost = dist.get(goal, math.inf)
    return PathResult(path=path, cost=cost, nodes_expanded=nodes_expanded)
