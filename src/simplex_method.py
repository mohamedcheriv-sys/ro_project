from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)


def simplex_example():
    """Resout: max z=3x+4y, x+2y<=8, 3x+y<=9, x,y>=0.
    Tableau avec variables [x, y, s1, s2, RHS]. La ligne z contient -c.
    """
    tableaus = []
    T = [
        [1.0, 2.0, 1.0, 0.0, 8.0],
        [3.0, 1.0, 0.0, 1.0, 9.0],
        [-3.0, -4.0, 0.0, 0.0, 0.0],
    ]
    basis = ["s1", "s2"]
    variables = ["x", "y", "s1", "s2", "RHS"]
    tableaus.append(("initial", [row[:] for row in T], basis[:]))

    iteration = 0
    while min(T[-1][:-1]) < -1e-9:
        iteration += 1
        entering = min(range(len(T[-1]) - 1), key=lambda j: T[-1][j])
        ratios = []
        for i in range(len(T) - 1):
            if T[i][entering] > 1e-9:
                ratios.append((T[i][-1] / T[i][entering], i))
        if not ratios:
            raise ValueError("Probleme non borne")
        _, leaving = min(ratios)
        pivot = T[leaving][entering]
        T[leaving] = [v / pivot for v in T[leaving]]
        for i in range(len(T)):
            if i == leaving:
                continue
            factor = T[i][entering]
            T[i] = [T[i][j] - factor * T[leaving][j] for j in range(len(T[i]))]
        basis[leaving] = variables[entering]
        tableaus.append((f"iteration_{iteration}", [row[:] for row in T], basis[:]))

    solution = {"x": 0.0, "y": 0.0, "s1": 0.0, "s2": 0.0}
    for b, row in zip(basis, T[:-1]):
        solution[b] = row[-1]
    z = T[-1][-1]
    return variables, tableaus, solution, z


def main():
    variables, tableaus, solution, z = simplex_example()
    with open(RESULTS / "simplex_tableaux.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["etape", "base", *variables])
        for name, T, basis in tableaus:
            for row_name, row in zip(basis + ["z"], T):
                w.writerow([name, row_name, *[round(v, 4) for v in row]])
    with open(RESULTS / "simplex_solution.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["variable", "valeur"])
        for k in ["x", "y", "s1", "s2"]:
            w.writerow([k, round(solution[k], 4)])
        w.writerow(["z_max", round(z, 4)])
    print("Methode du simplexe")
    print(f"x* = {solution['x']:.2f}, y* = {solution['y']:.2f}, z* = {z:.2f}")


if __name__ == "__main__":
    main()
