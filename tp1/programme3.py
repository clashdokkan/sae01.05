import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "test.csv"

critere_titre = "R1.07"

with open(csv_path, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")

    for row in reader:
        # Test du critère
        if row["title"] == critere_titre:
            # Affichage des colonnes souhaitées
            print("Début :", row["start"])
            print("Fin :", row["end"])
            print("Lieu :", row["location"])
            print("--------------------")
