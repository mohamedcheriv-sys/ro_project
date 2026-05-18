from pathlib import Path
import csv
from itertools import product

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

PROJECTS = ["Projet_1", "Projet_2", "Projet_3"]
CAPACITY = {"Projet_1": 2, "Projet_2": 2, "Projet_3": 2}


def load_preferences():
    students, preferences = [], {}
    with open(DATA / "student_preferences.csv", newline="") as f:
        for row in csv.DictReader(f):
            e = row["etudiant"]
            students.append(e)
            for p in PROJECTS:
                preferences[(e, p)] = int(row[p])
    return students, preferences


def solve_assignment(students, preferences):
    best_assign, best_score = None, -1
    for choices in product(PROJECTS, repeat=len(students)):
        counts = {p: choices.count(p) for p in PROJECTS}
        if counts != CAPACITY:
            continue
        score = sum(preferences[(e, p)] for e, p in zip(students, choices))
        if score > best_score:
            best_score = score
            best_assign = list(zip(students, choices))
    return best_assign, best_score


def main():
    students, preferences = load_preferences()
    assignment, score = solve_assignment(students, preferences)
    with open(RESULTS / "student_assignment.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["etudiant", "projet", "satisfaction"])
        for e, p in assignment:
            w.writerow([e, p, preferences[(e, p)]])
        w.writerow(["TOTAL", "", score])
    print("Affectation des etudiants aux projets")
    for e, p in assignment:
        print(f"{e} -> {p} | satisfaction={preferences[(e, p)]}")
    print(f"Satisfaction totale = {score}")


if __name__ == "__main__":
    main()
