# experiments/run_all.py

import os
import csv
import random
from datetime import datetime

from src.graph import generar_grafo_geometrico
from src.dijkstra import dijkstra
from src.astar import astar
from src.dijkstra_bi import bidirectional_dijkstra
from src.utils import run_with_timing


def ensure_dirs():
    """Crea carpetas necesarias si no existen."""
    if not os.path.exists("experiments/results"):
        os.makedirs("experiments/results")
    if not os.path.exists("experiments/plots"):
        os.makedirs("experiments/plots")


def seleccionar_pares(grafo, num_pares=10, seed=123):
    """
    Selecciona aleatoriamente 'num_pares' pares (u, v) distintos de nodos.
    """
    random.seed(seed)
    nodos = list(grafo.adj.keys())
    pares = set()

    while len(pares) < num_pares and len(pares) < len(nodos) * (len(nodos) - 1):
        u = random.choice(nodos)
        v = random.choice(nodos)
        if u != v:
            pares.add((u, v))

    return list(pares)


def run_experiments():
    ensure_dirs()

    # Configuraciones de grafos (puedes ajustar tamaños y densidades)
    configuraciones = [
        # (num_nodos, densidad, etiqueta, seed_grafo)
        (100, 0.15,  "small",  1),
        (500, 0.10,  "medium", 2),
        (1000, 0.05, "large",  3),
    ]

    algoritmos = {
        "dijkstra": dijkstra,
        "astar": astar,
        "dijkstra_bidireccional": bidirectional_dijkstra,
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = f"experiments/results/resultados_{timestamp}.csv"

    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "graph_label", "graph_seed", "num_nodes", "density",
            "source", "target",
            "algorithm", "run",
            "time_ms", "nodes_expanded", "path_cost"
        ])

        for num_nodos, densidad, label, seed_grafo in configuraciones:
            print(f"\n🧱 Generando grafo '{label}' "
                  f"({num_nodos} nodos, densidad={densidad}, seed={seed_grafo})...")
            grafo = generar_grafo_geometrico(num_nodos, densidad, seed=seed_grafo)

            # Elegir 10 pares O–D por grafo
            pares = seleccionar_pares(grafo, num_pares=10, seed=100 + seed_grafo)

            for (s, t) in pares:
                for nombre_alg, func in algoritmos.items():
                    # 3 corridas por algoritmo/par para promediar tiempos
                    for corrida in range(1, 4):
                        res = run_with_timing(func, grafo, s, t)

                        writer.writerow([
                            label,
                            seed_grafo,
                            num_nodos,
                            densidad,
                            s,
                            t,
                            nombre_alg,
                            corrida,
                            f"{res.elapsed_ms:.6f}",
                            res.nodes_expanded,
                            f"{res.cost:.6f}",
                        ])

                        print(
                            f"[{label}] {nombre_alg} {s}->{t} "
                            f"run {corrida}: "
                            f"time={res.elapsed_ms:.3f} ms, "
                            f"expanded={res.nodes_expanded}, "
                            f"cost={res.cost:.4f}"
                        )

    print(f"\n✔ Archivo generado: {out_file}")


if __name__ == "__main__":
    run_experiments()
