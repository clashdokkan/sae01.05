"""import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

csv_file = "capture.csv"
rapport_md = "rapport_comparatif.md"

# ==============================
# 1️⃣ Extraction des données
# ==============================

# Tentatives SSH
ssh_counter = defaultdict(int)
with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        if row["Port_Destination"] == "22":
            ssh_counter[row["Source"]] += 1
ssh_alerts = {src: c for src, c in ssh_counter.items() if c > 20}

# Scan de ports
scan = defaultdict(set)
with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        if row["Port_Destination"]:
            scan[row["Source"]].add(row["Port_Destination"])
scan_alerts = {src: ports for src, ports in scan.items() if len(ports) > 10}

# Trafic anormal
traffic = defaultdict(int)
with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        traffic[row["Source"]] += 1
traffic_alerts = {src: c for src, c in traffic.items() if c > 100}

# ==============================
# 2️⃣ Regroupement des données
# ==============================

sources = set(list(ssh_counter.keys()) + list(scan_alerts.keys()) + list(traffic_alerts.keys()))

comparaison = {}
for src in sources:
    comparaison[src] = {
        "ssh": ssh_counter.get(src, 0),
        "scan": len(scan_alerts.get(src, [])) if src in scan_alerts else 0,
        "trafic": traffic_alerts.get(src, 0)
    }

# ==============================
# 3️⃣ Génération du graphique comparatif
# ==============================

labels = list(comparaison.keys())
ssh_values = [comparaison[src]["ssh"] for src in labels]
scan_values = [comparaison[src]["scan"] for src in labels]
trafic_values = [comparaison[src]["trafic"] for src in labels]

x = np.arange(len(labels))  # positions des sources
width = 0.25

plt.figure(figsize=(12, 6))
plt.bar(x - width, ssh_values, width, label="SSH")
plt.bar(x, scan_values, width, label="Scan")
plt.bar(x + width, trafic_values, width, label="Trafic")
plt.xticks(x, labels, rotation=45, ha="right")
plt.ylabel("Nombre d'événements")
plt.title("Comparaison des alertes par source")
plt.legend()
plt.tight_layout()
plt.savefig("comparaison_alertes.png")
plt.close()
print("✅ Graphique comparatif sauvegardé : comparaison_alertes.png")

'''# ==============================
# 4️⃣ Génération du rapport Markdown
# ==============================

with open(rapport_md, "w", encoding="utf-8") as f:
    f.write("# Rapport comparatif des alertes réseau\n\n")

    f.write("Ce rapport compare pour chaque source les tentatives SSH, le scan de ports et le trafic anormal.\n\n")

    f.write("## Tableau synthétique des alertes\n")
    f.write("| Source | SSH | Scan | Trafic |\n")
    f.write("|--------|-----|------|--------|\n")
    for src, data in comparaison.items():
        f.write(f"| {src} | {data['ssh']} | {data['scan']} | {data['trafic']} |\n")
    f.write("\n")

    f.write("## Graphique comparatif\n")
    f.write("![Comparaison des alertes](comparaison_alertes.png)\n\n")

    f.write("## Analyse\n")
    f.write(
        "Les sources affichant de hauts niveaux dans plusieurs catégories peuvent représenter "
        "des comportements suspects multi-facette. La visualisation permet de prioriser les mesures "
        "de sécurité et d'identifier rapidement les hôtes problématiques.\n"
    )

print(f"✅ Rapport Markdown généré : {rapport_md}")"""



