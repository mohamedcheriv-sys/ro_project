from pathlib import Path
import csv
import math

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)


def load_parameters():
    params = {}
    with open(DATA / "eoq_data.csv", newline="") as f:
        for row in csv.DictReader(f):
            params[row["parametre"]] = float(row["valeur"])
    return params


def main():
    params = load_parameters()
    D, S, H = params["D"], params["S"], params["H"]
    q_star = math.sqrt((2 * D * S) / H)
    orders_per_year = D / q_star
    total_cost = (D / q_star) * S + (q_star / 2) * H
    with open(RESULTS / "eoq_result.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["indicateur", "valeur"])
        w.writerow(["Q_star", round(q_star, 2)])
        w.writerow(["nombre_commandes_par_an", round(orders_per_year, 2)])
        w.writerow(["cout_total_minimal", round(total_cost, 2)])
    print("Dimensionnement de stock EOQ")
    print(f"Q* = {q_star:.2f} unites")
    print(f"Nombre de commandes/an = {orders_per_year:.2f}")
    print(f"Cout total minimal = {total_cost:.2f} MRU")


if __name__ == "__main__":
    main()
