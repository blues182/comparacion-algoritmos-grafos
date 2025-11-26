# src/utils.py
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Callable


@dataclass
class PathResult:
    """
    Resultado de un algoritmo de rutas mínimas.
    """
    path: List[Any]
    cost: float
    nodes_expanded: int
    elapsed_ms: float | None = None  # tiempo en milisegundos (opcional)


def reconstruct_path(parents: Dict[Any, Any], start: Any, goal: Any) -> List[Any]:
    """
    Reconstruye el camino desde 'start' hasta 'goal'
    usando el diccionario de padres.
    """
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parents.get(current)
    path.reverse()
    if not path or path[0] != start:
        return []
    return path


def run_with_timing(algorithm: Callable, graph, start, goal) -> PathResult:
    """
    Ejecuta un algoritmo de ruta mínima y mide tiempo de ejecución.
    El algoritmo debe devolver un PathResult SIN elapsed_ms.
    """
    t0 = time.perf_counter()
    result: PathResult = algorithm(graph, start, goal)
    t1 = time.perf_counter()
    result.elapsed_ms = (t1 - t0) * 1000.0
    return result