# src/astar.py
import math
import heapq

from utils import PathResult, reconstruct_path


def heuristic_euclidiana(graph, u, goal) -> float:
    """
    Heurística euclidiana (admisible) usando positions del grafo.
    """
    (x1, y1) = graph.positions[u]
    (x2, y2) = graph.positions[goal]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def astar(graph, start, goal) -> PathResult:
    """
    Algoritmo A* (A-star) con heurística euclidiana.
    """
    g_cost = {node: math.inf for node in graph.adj}
    g_cost[start] = 0.0

    parents = {start: None}
    visited = set()
    pq = []  # elementos: (f, g, node)
    heapq.heappush(pq, (heuristic_euclidiana(graph, start, goal), 0.0, start))
    nodes_expanded = 0

    while pq:
        f, g_curr, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        nodes_expanded += 1

        if u == goal:
            break

        for v, w in graph.neighbors(u):
            tentative_g = g_curr + w
            if tentative_g < g_cost[v]:
                g_cost[v] = tentative_g
                parents[v] = u
                f_v = tentative_g + heuristic_euclidiana(graph, v, goal)
                heapq.heappush(pq, (f_v, tentative_g, v))

    path = reconstruct_path(parents, start, goal)
    cost = g_cost.get(goal, math.inf)
    return PathResult(path=path, cost=cost, nodes_expanded=nodes_expanded)
