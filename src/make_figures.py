from pathlib import Path
import csv, math
import matplotlib.pyplot as plt
import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
DATA = ROOT / "data"
RESULTS = ROOT / "results"
FIG.mkdir(exist_ok=True)


def water_network():
    coords = {
        "Depot": (0, 0), "A": (1.4, 2.0), "B": (2.5, 1.2), "C": (4.1, 1.4),
        "D": (3.8, -1.6), "E": (1.2, -1.1), "F": (3.0, -0.5),
    }
    edges = [("Depot","A"),("A","B"),("B","C"),("Depot","E"),("E","F"),("F","D"),("B","F")]
    graph = nx.Graph()
    graph.add_edges_from(edges)
    fig, ax = plt.subplots(figsize=(6,4))
    nx.draw_networkx_edges(graph, coords, ax=ax, width=1.6)
    nx.draw_networkx_nodes(graph, coords, ax=ax, node_size=700)
    nx.draw_networkx_labels(graph, coords, ax=ax, font_size=10)
    ax.set_title("Réseau simplifié de distribution d'eau - graphe NetworkX")
    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(FIG/'water_network.png', dpi=200)
    plt.close(fig)


def eoq_curve():
    D, S, H = 1200, 50, 2
    qs = list(range(50, 501, 10))
    costs = [(D/q)*S + (q/2)*H for q in qs]
    qstar = math.sqrt((2*D*S)/H)
    cstar = (D/qstar)*S + (qstar/2)*H
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(qs, costs)
    ax.scatter([qstar],[cstar],s=90)
    ax.annotate(f"Q* ≈ {qstar:.0f}", xy=(qstar,cstar), xytext=(qstar+30,cstar+60), arrowprops=dict(arrowstyle='->'))
    ax.set_xlabel("Quantité commandée Q")
    ax.set_ylabel("Coût total")
    ax.set_title("Courbe du coût total EOQ")
    fig.tight_layout()
    fig.savefig(FIG/'eoq_curve.png', dpi=200)
    plt.close(fig)


def simplex_region():
    import numpy as np
    x = np.linspace(0, 4, 200)
    y1 = (8 - x)/2
    y2 = 9 - 3*x
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(x, y1, label='x + 2y = 8')
    ax.plot(x, y2, label='3x + y = 9')
    y_upper = np.minimum(y1, y2)
    y_upper = np.maximum(y_upper, 0)
    ax.fill_between(x, 0, y_upper, where=(y_upper>=0), alpha=0.25)
    ax.scatter([2],[3],s=90)
    ax.annotate('Optimum (2,3)', xy=(2,3), xytext=(2.4,3.3), arrowprops=dict(arrowstyle='->'))
    ax.set_xlim(0,4)
    ax.set_ylim(0,5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Région admissible du problème simplexe')
    ax.legend(loc='upper right', fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG/'simplex_region.png', dpi=200)
    plt.close(fig)


def assignment_plot():
    # Uses known optimal assignment from exhaustive enumeration
    students = ['E1','E2','E3','E4','E5','E6']
    projects = ['P1','P2','P3']
    assign = {'E1':'P1','E2':'P1','E3':'P2','E4':'P2','E5':'P3','E6':'P3'}
    sy = {s: i for i,s in enumerate(students)}
    py = {'P1':4.5,'P2':2.5,'P3':0.5}
    fig, ax = plt.subplots(figsize=(6,4))
    for s in students:
        ax.scatter(0, sy[s], s=130)
        ax.text(-0.1, sy[s], s, ha='right', va='center')
        ax.plot([0,1],[sy[s],py[assign[s]]], linewidth=1.6)
    for p in projects:
        ax.scatter(1, py[p], s=220)
        ax.text(1.08, py[p], p, ha='left', va='center')
    ax.set_xlim(-0.6,1.6)
    ax.set_ylim(-0.8,5.8)
    ax.set_title('Affectation optimale étudiants-projets')
    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(FIG/'student_assignment.png', dpi=200)
    plt.close(fig)

if __name__ == '__main__':
    water_network(); assignment_plot(); eoq_curve(); simplex_region()
