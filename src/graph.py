# src/graph.py
import math
import csv
import os
import random


class Graph:
    """
    Grafo no dirigido con lista de adyacencia y posiciones 2D por nodo.
    """
    def __init__(self):
        # Lista de adyacencia: {nodo: [(vecino, peso), ...]}
        self.adj = {}
        # Posiciones 2D: {nodo: (x, y)}
        self.positions = {}

    # ---------- Operaciones básicas ----------

    def add_node(self, node, x=None, y=None):
        if node not in self.adj:
            self.adj[node] = []
        if x is not None and y is not None:
            self.positions[node] = (float(x), float(y))

    def add_edge(self, u, v, weight):
        """
        Agrega arista no dirigida u <-> v con peso >= 0.
        """
        w = float(weight)
        if w < 0:
            raise ValueError("Los pesos no pueden ser negativos.")
        self.adj.setdefault(u, []).append((v, w))
        self.adj.setdefault(v, []).append((u, w))

    def neighbors(self, node):
        return self.adj.get(node, [])

    # ---------- Utilidades geométricas ----------

    def distance_euclidiana(self, u, v):
        """
        Distancia euclidiana entre dos nodos usando sus posiciones 2D.
        """
        (x1, y1) = self.positions[u]
        (x2, y2) = self.positions[v]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# =====================================================================
#   GENERADOR DE GRAFOS ALEATORIOS (LO QUE NECESITAS)
# =====================================================================

def generar_grafo_geometrico(num_nodos: int, densidad: float, seed: int = 42) -> Graph:
    """
    Genera un grafo no dirigido:

    - num_nodos nodos con posiciones aleatorias en el cuadrado [0,1] x [0,1].
    - Conecta pares de nodos con probabilidad p para aproximar la densidad.
      densidad ≈ E / (N*(N-1)/2)  -> usamos p ≈ 2*densidad (acotado en [0,1]).
    - El peso de cada arista es la distancia euclidiana entre nodos.

    Los ids de los nodos son strings: "0", "1", ..., para que luego
    sea fácil guardarlos en CSV si quieres.
    """
    random.seed(seed)
    g = Graph()

    # Crear nodos con posiciones aleatorias
    for i in range(num_nodos):
        x = random.random()
        y = random.random()
        g.add_node(str(i), x, y)

    nodos = list(g.adj.keys())
    n = len(nodos)

    # Probabilidad de arista aproximando densidad
    p = min(1.0, max(0.0, 2 * densidad))

    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                u = nodos[i]
                v = nodos[j]
                w = g.distance_euclidiana(u, v)
                g.add_edge(u, v, w)

    return g


# =====================================================================
#   FUNCIONES OPCIONALES PARA CARGAR CSV (POR SI LAS LLEGAS A USAR)
# =====================================================================

def load_graph_from_csv(data_dir="data") -> Graph:
    """
    Carga un grafo desde:
      - nodos.csv:  id,x,y
      - aristas.csv: source,target,weight

    Si 'weight' está vacío, se calcula como distancia euclidiana.
    """
    g = Graph()

    nodos_path = os.path.join(data_dir, "nodos.csv")
    aristas_path = os.path.join(data_dir, "aristas.csv")

    if not os.path.exists(nodos_path) or not os.path.exists(aristas_path):
        raise FileNotFoundError("No se encontraron nodos.csv / aristas.csv en la carpeta data/.")

    # --- Cargar nodos ---
    with open(nodos_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            node_id = row["id"]
            x = float(row["x"])
            y = float(row["y"])
            g.add_node(node_id, x, y)

    # --- Cargar aristas ---
    with open(aristas_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            u = row["source"]
            v = row["target"]
            w_str = row.get("weight", "").strip()

            if w_str == "":
                if u not in g.positions or v not in g.positions:
                    raise ValueError("No se pueden calcular pesos: faltan posiciones para nodos.")
                weight = g.distance_euclidiana(u, v)
            else:
                weight = float(w_str)

            g.add_edge(u, v, weight)

    return g


def load_od_pairs(data_dir="data"):
    """
    Carga pares origen–destino desde pares_OD.csv:
      - columnas: source,target
    Devuelve lista de tuplas (source, target) como strings.
    """
    pares_path = os.path.join(data_dir, "pares_OD.csv")
    if not os.path.exists(pares_path):
        raise FileNotFoundError("No se encontró pares_OD.csv en la carpeta data/.")

    pares = []
    with open(pares_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            s = row["source"]
            t = row["target"]
            if s != t:
                pares.append((s, t))
    return pares
