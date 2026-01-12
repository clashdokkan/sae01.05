'''import matplotlib.pyplot as plt
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "test.csv"

critere_titre = "A1"
labels = []
sizes = []
colors = ["yellowgreen", "gold", "lightskyblue", "lightcoral"]


with open(csv_path, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")

    for row in reader:
        # Test du critère
        if critere_titre in row["description"]:
            # Affichage des colonnes souhaitées
            print("Nom :", row["title"])
            print("--------------------")
            for i in labels:
                if row["title"] != i :
                    labels.append(row["title"])
                elif row["title"] == i:
                    sizes[i] = sizes[i] + 1


plt.pie(sizes, labels=labels, colors=colors,
    autopct="%1.1f%%", shadow=True, startangle=90)
plt.axis("equal")
plt.savefig("PieChart01.png")
plt.show()'''
import csv
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "test.csv"

# Comptage des séances par mois
mois = {
    "Septembre": 0,
    "Octobre": 0,
    "Novembre": 0,
    "Décembre": 0
}

with open(csv_path, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")

    for row in reader:
        # On filtre le groupe A1
        if "B1" in row["description"]:

            # Conversion de la date
            date_tp = datetime.strptime(row["start"], "%Y%m%dT%H%M%SZ")

            if date_tp.year == 2025:
                if date_tp.month == 9:
                    mois["Septembre"] += 1
                elif date_tp.month == 10:
                    mois["Octobre"] += 1
                elif date_tp.month == 11:
                    mois["Novembre"] += 1
                elif date_tp.month == 12:
                    mois["Décembre"] += 1

# Création du graphe (diagramme en bâtons)
plt.figure(figsize=(8, 5))
plt.bar(mois.keys(), mois.values(), color="cornflowerblue")

plt.title("Nombre de séances de TP – Groupe A1 (2025)")
plt.xlabel("Mois")
plt.ylabel("Nombre de séances")

# Export PNG
plt.savefig("TP_A1_2025.png")
plt.show()


"""PROGRAMME EN CAMEMBERT"""
# Importation des modules nécessaires
import csv  # pour lire le fichier CSV
import matplotlib.pyplot as plt  # pour créer les graphiques
from pathlib import Path  # pour gérer les chemins de fichiers
from datetime import datetime  # pour manipuler les dates

# Définir le chemin vers le fichier CSV
BASE_DIR = Path(__file__).resolve().parent  # dossier où se trouve le script
csv_path = BASE_DIR / "test.csv"  # fichier CSV à lire

# Initialisation du compteur des séances par mois
mois = {
    "Septembre": 0,
    "Octobre": 0,
    "Novembre": 0,
    "Décembre": 0
}

# Ouverture du fichier CSV en lecture
with open(csv_path, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")  # on lit le CSV avec DictReader

    # Parcours de chaque ligne du CSV
    for row in reader:
        # Filtrer uniquement les séances du groupe A1
        if "A1" in row["description"]:

            # Conversion de la date de la colonne "start" en objet datetime
            # Format du CSV : 20251215T150000Z
            date_tp = datetime.strptime(row["start"], "%Y%m%dT%H%M%SZ")

            # Vérifier que l'année est 2025
            if date_tp.year == 2025:
                # Comptage en fonction du mois
                if date_tp.month == 9:
                    mois["Septembre"] += 1
                elif date_tp.month == 10:
                    mois["Octobre"] += 1
                elif date_tp.month == 11:
                    mois["Novembre"] += 1
                elif date_tp.month == 12:
                    mois["Décembre"] += 1

# -----------------------
# Création du graphique camembert (pie chart)
# -----------------------

# Les valeurs sont le nombre de séances par mois
values = list(mois.values())

# Les labels sont les noms des mois
labels = list(mois.keys())

# Couleurs personnalisées pour le camembert
colors = ["yellowgreen", "gold", "lightskyblue", "lightcoral"]

# Création du camembert
plt.pie(
    values,          # valeurs à représenter
    labels=labels,   # noms des catégories
    colors=colors,   # couleurs du graphique
    autopct="%1.1f%%",  # affichage du pourcentage
    shadow=True,         # ombre pour effet 3D
    startangle=90        # rotation pour que le premier secteur commence en haut
)

# Titre du graphique
plt.title("Répartition des séances de TP du groupe A1 (2025)")

# Égalité des axes pour que le camembert soit rond
plt.axis("equal")

# Export du graphique en PNG
plt.savefig("TP_A1_2025_camembert.png")

# Affichage du graphique à l'écran
plt.show()

