from pathlib import Path
import csv
import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

CAPACITY = 1000
DEPOT = "Depot"


def load_demands():
    demands = {}
    with open(DATA / "water_demands.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            demands[row["point"]] = int(row["demande_litres"])
    return demands


def build_graph():
    """Construit un graphe pondéré avec NetworkX à partir des distances."""
    graph = nx.Graph()
    with open(DATA / "water_distances.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            i, j = row["i"], row["j"]
            d = float(row["distance_km"])
            graph.add_edge(i, j, weight=d)
    return graph


def shortest_distance(graph, i, j):
    """Distance minimale entre deux noeuds du réseau selon NetworkX."""
    return nx.shortest_path_length(graph, i, j, weight="weight")


def nearest_neighbor_routes(demands, graph, capacity=CAPACITY):
    """
    Heuristique du plus proche voisin appliquée sur un graphe NetworkX.
    Cette méthode donne une solution réalisable mais ne garantit pas l'optimum global du VRP.
    """
    unvisited = set(demands)
    routes = []

    while unvisited:
        current = DEPOT
        load = 0
        route = [DEPOT]

        while True:
            feasible = [p for p in unvisited if load + demands[p] <= capacity]
            if not feasible:
                break

            next_point = min(feasible, key=lambda p: shortest_distance(graph, current, p))
            route.append(next_point)
            load += demands[next_point]
            unvisited.remove(next_point)
            current = next_point

        route.append(DEPOT)
        total_distance = sum(
            shortest_distance(graph, route[i], route[i + 1])
            for i in range(len(route) - 1)
        )
        routes.append((route, load, total_distance))

    return routes


def main():
    demands = load_demands()
    graph = build_graph()
    routes = nearest_neighbor_routes(demands, graph)

    with open(RESULTS / "water_routes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["tournee", "route", "charge_litres", "distance_km", "outil"])
        for k, (route, load, distance) in enumerate(routes, 1):
            writer.writerow([k, " -> ".join(route), load, round(distance, 2), "NetworkX"])

    print("Routage des camions d'eau - NetworkX + heuristique")
    for k, (route, load, distance) in enumerate(routes, 1):
        print(f"Tournee {k}: {' -> '.join(route)} | charge={load} L | distance={distance:.1f} km")
    print(f"Distance totale = {sum(r[2] for r in routes):.1f} km")


if __name__ == "__main__":
    main()
