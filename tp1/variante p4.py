import csv
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

# -----------------------
# Paramètres
# -----------------------
GROUPE = "B2"      # groupe à analyser
ANNEE = 2025       # année étudiée

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "test.csv"

# Dictionnaire : matière -> nombre de séances
matieres = {}

# -----------------------
# Lecture du CSV
# -----------------------
with open(csv_path, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")

    for row in reader:
        description = row.get("description", "")
        titre = row.get("title", "")

        # Filtrer par groupe
        if GROUPE in description:

            # Conversion de la date
            date_tp = datetime.strptime(row["start"], "%Y%m%dT%H%M%SZ")

            # Filtrer par année
            if date_tp.year == ANNEE:

                # Initialisation si nouvelle matière
                if titre not in matieres:
                    matieres[titre] = 0

                matieres[titre] += 1

# -----------------------
# Graphique en barres
# -----------------------
plt.figure(figsize=(9, 5))
plt.bar(matieres.keys(), matieres.values(), color="cornflowerblue")

plt.title(f"Nombre de séances par matière – Groupe {GROUPE} ({ANNEE})")
plt.xlabel("Matière")
plt.ylabel("Nombre de séances")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig(f"Matieres_{GROUPE}_{ANNEE}.png")
plt.show()

plt.figure(figsize=(7, 7))
plt.pie(
    matieres.values(),
    labels=matieres.keys(),
    autopct="%1.1f%%",
    startangle=90
)

plt.title(f"Répartition des matières – Groupe {GROUPE} ({ANNEE})")
plt.axis("equal")
plt.savefig(f"Matieres_{GROUPE}_{ANNEE}_camembert.png")
plt.show()


