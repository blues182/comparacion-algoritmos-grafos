# src/graph.py
import math
import csv
import os


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


# ---------- Funciones para cargar datos desde CSV ----------

def load_graph_from_csv(data_dir="data"):
    """
    Carga un grafo desde:
      - nodos.csv:  id,x,y
      - aristas.csv: source,target,weight

    Si 'weight' está vacío, se calcula como distancia euclidiana.
    """
    g = Graph()

    # --- Cargar nodos ---
    nodos_path = os.path.join(data_dir, "nodos.csv")
    with open(nodos_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            node_id = row["id"]
            x = float(row["x"])
            y = float(row["y"])
            g.add_node(node_id, x, y)

    # --- Cargar aristas ---
    aristas_path = os.path.join(data_dir, "aristas.csv")
    with open(aristas_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            u = row["source"]
            v = row["target"]
            w_str = row.get("weight", "").strip()

            if w_str == "":
                # Si no hay peso explícito, usar distancia euclidiana
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
    Devuelve una lista de tuplas (source, target) como strings.
    """
    pares_path = os.path.join(data_dir, "pares_OD.csv")
    pares = []
    with open(pares_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            s = row["source"]
            t = row["target"]
            if s != t:
                pares.append((s, t))
    return pares