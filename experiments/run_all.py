# experiments/run_all.py

import os
import csv
from datetime import datetime

# Importar algoritmos y cargadores desde src/
from src.graph import load_graph_from_csv, load_od_pairs
from src.dijkstra_bi import bidirectional_dijkstra
from src.dijkstra import dijkstra
from src.astar import astar
from src.utils import run_with_timing


def ensure_dirs():
    """Crea carpetas necesarias si no existen."""
    if not os.path.exists("experiments/results"):
        os.makedirs("experiments/results")
    if not os.path.exists("experiments/plots"):
        os.makedirs("experiments/plots")


def run_experiments():
    ensure_dirs()

    # Cargar grafo desde data/
    graph = load_graph_from_csv("data")

    # Cargar pares origen–destino
    pares = load_od_pairs("data")

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
            "source", "target", "algorithm", "time_ms",
            "nodes_expanded", "path_cost", "path"
        ])

        for (s, t) in pares:
            for nombre, alg in algoritmos.items():
                result = run_with_timing(alg, graph, s, t)

                writer.writerow([
                    s,
                    t,
                    nombre,
                    f"{result.elapsed_ms:.6f}",
                    result.nodes_expanded,
                    f"{result.cost:.6f}",
                    "->".join(result.path)
                ])

                print(
                    f"{nombre.upper()}  {s}->{t}  "
                    f"time={result.elapsed_ms:.2f} ms  "
                    f"expanded={result.nodes_expanded}  "
                    f"cost={result.cost:.4f}"
                )

    print(f"\n✔ Archivo generado: {out_file}")


if __name__ == "__main__":
    run_experiments()
