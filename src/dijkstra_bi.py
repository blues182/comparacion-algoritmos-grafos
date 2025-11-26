# src/dijkstra_bi.py
import math
import heapq

from utils import PathResult, reconstruct_path


def bidirectional_dijkstra(graph, start, goal) -> PathResult:
    """
    Dijkstra bidireccional para grafos no dirigidos.
    Ejecuta dos búsquedas: una desde start y otra desde goal,
    hasta que se encuentran.
    """
    if start == goal:
        return PathResult(path=[start], cost=0.0, nodes_expanded=1)

    # Hacia adelante
    dist_f = {node: math.inf for node in graph.adj}
    dist_f[start] = 0.0
    parents_f = {start: None}
    visited_f = set()
    pq_f = [(0.0, start)]

    # Hacia atrás (en grafo no dirigido es equivalente)
    dist_b = {node: math.inf for node in graph.adj}
    dist_b[goal] = 0.0
    parents_b = {goal: None}
    visited_b = set()
    pq_b = [(0.0, goal)]

    nodes_expanded = 0
    best_meeting = None
    best_dist = math.inf

    while pq_f and pq_b:
        # Expansión adelante
        if pq_f:
            d_f, u = heapq.heappop(pq_f)
            if u not in visited_f:
                visited_f.add(u)
                nodes_expanded += 1

                if u in visited_b:
                    total = dist_f[u] + dist_b[u]
                    if total < best_dist:
                        best_dist = total
                        best_meeting = u

                for v, w in graph.neighbors(u):
                    new_cost = dist_f[u] + w
                    if new_cost < dist_f[v]:
                        dist_f[v] = new_cost
                        parents_f[v] = u
                        heapq.heappush(pq_f, (new_cost, v))

        # Expansión atrás
        if pq_b:
            d_b, u = heapq.heappop(pq_b)
            if u not in visited_b:
                visited_b.add(u)
                nodes_expanded += 1

                if u in visited_f:
                    total = dist_f[u] + dist_b[u]
                    if total < best_dist:
                        best_dist = total
                        best_meeting = u

                for v, w in graph.neighbors(u):
                    new_cost = dist_b[u] + w
                    if new_cost < dist_b[v]:
                        dist_b[v] = new_cost
                        parents_b[v] = u
                        heapq.heappush(pq_b, (new_cost, v))

        # Si ya hay punto de encuentro razonable, podemos parar
        if best_meeting is not None:
            break

    if best_meeting is None:
        # No se encontró camino
        return PathResult(path=[], cost=math.inf, nodes_expanded=nodes_expanded)

    # Reconstruir camino: start -> best_meeting
    path_forward = reconstruct_path(parents_f, start, best_meeting)

    # Reconstruir camino: best_meeting -> goal (usando parents_b hacia atrás)
    path_backward = []
    current = parents_b.get(best_meeting)
    while current is not None:
        path_backward.append(current)
        current = parents_b.get(current)

    full_path = path_forward + path_backward
    return PathResult(path=full_path, cost=best_dist, nodes_expanded=nodes_expanded)
