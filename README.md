# Comparación de Algoritmos de Ruta en Grafos
Proyecto de **Matemáticas Discretas – Otoño 2025** orientado a comparar el rendimiento de distintos algoritmos de búsqueda de rutas en grafos ponderados **sin aristas negativas**.

Este repositorio contiene:

- Implementaciones de **Dijkstra**, **A\*** y **Dijkstra Bidireccional**
- Scripts para generar grafos, correr experimentos y exportar resultados
- Código reproducible documentado
- Datos y gráficas utilizadas en el reporte final

---

## 📌 Objetivo del Proyecto
Desarrollar un sistema experimental que:

1. Compare el desempeño de tres algoritmos de búsqueda de rutas.
2. Evalúe tiempo de ejecución, nodos expandidos, costo de la ruta y (opcionalmente) memoria.
3. Analice la complejidad teórica vs. empírica.
4. Genere resultados reproducibles sobre múltiples tamaños de grafo.

---

## 📍 Algoritmos Implementados

### 🔹 1. Dijkstra
Usado como **línea base** por su:
- Optimalidad en grafos sin pesos negativos  
- Buena eficiencia con `priority_queue`  
- Documentación amplia para validación  
- Complejidad:  
  \[
  O((V + E)\log V)
  \]

### 🔹 2. A\*
Incluido por su uso práctico en aplicaciones reales:
- Utiliza heurística para guiar la búsqueda
- Reduce nodos expandidos en la práctica
- Heurística utilizada: **distancia euclidiana**
- Heurística es **admisible y consistente**, mantiene optimalidad

### 🔹 3. Dijkstra Bidireccional
Seleccionado como tercer algoritmo por:
- Mejorar directamente al Dijkstra tradicional
- Reducir drásticamente el espacio de búsqueda al correr desde origen y destino
- Ofrecer un punto intermedio entre Dijkstra y A\* en términos de rendimiento
- Aportar mayor valor comparativo que la Búsqueda de Costo Uniforme (equivalente a Dijkstra)

---

## 📐 Método de Ponderación (Pesos del Grafo)

Los pesos de las aristas se calculan mediante **distancia euclidiana**, asegurando pesos **no negativos**:

\[
w(i,j) = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}
\]

Ventajas:

- Compatible con Dijkstra, A\* y variantes
- Proporciona una heurística admisible para A\*
- Modela adecuadamente mapas 2D (campus/ciudad)
- Evita problemas de consistencia o subestimación

---

## 🗂️ Estructura del Repositorio

```text
.
├── data/
│   ├── nodos.csv            # Coordenadas (xi, yi)
│   ├── aristas.csv          # Conexiones entre nodos
│   └── pares_OD.csv         # Pares origen–destino para pruebas
│
├── src/
│   ├── dijkstra.py          # Dijkstra tradicional
│   ├── astar.py             # Algoritmo A*
│   ├── dijkstra_bi.py       # Dijkstra Bidireccional
│   ├── graph.py             # Generación/validación del grafo
│   └── utils.py             # Rutas, medición de tiempo, etc.
│
├── experiments/
│   ├── run_all.py           # Corre todos los experimentos
│   ├── results/             # CSVs generados automáticamente
│   └── plots/               # Gráficas para el reporte
│
├── report/
│   └── informe.pdf          # Reporte final del proyecto
│
└── README.md
