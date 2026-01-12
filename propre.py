import csv
from collections import defaultdict

csv_file = "capture.csv"

ssh_counter = defaultdict(int)

with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        # SSH par port ou par nom
        if row["Port_Destination"] == "22" or "ssh" in row["Source"].lower():
            ssh_counter[row["Source"]] += 1

# Affichage
print("=== Activité SSH ===(Beaucoup de tentatives SSH)")
for src, count in sorted(ssh_counter.items(), key=lambda x: x[1], reverse=True):
    print(f"{src} → {count} paquets")

# Seuil simple
for src, count in ssh_counter.items():
    if count > 20:
        print(f"⚠️ Activité SSH suspecte depuis {src}")


scan = defaultdict(set)

with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        src = row["Source"]
        port = row["Port_Destination"]

        if port:
            scan[src].add(port)

print("\n=== Scan de ports === (Test de nombreux ports)")
for src, ports in scan.items():
    if len(ports) > 10:  # seuil raisonnable
        print(f"⚠️ Scan probable depuis {src} ({len(ports)} ports)")

traffic = defaultdict(int)

with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        traffic[row["Source"]] += 1

print("\n=== Trafic anormal ===(saturation du réseau)")
for src, count in sorted(traffic.items(), key=lambda x: x[1], reverse=True):
    if count > 100:
        print(f"⚠️ Trafic anormal depuis {src} ({count} paquets)")


import csv
import matplotlib.pyplot as plt
from collections import defaultdict

csv_file = "capture.csv"

traffic = defaultdict(int)

with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        traffic[row["Source"]] += 1

# Top 5 Ce graphique sert à prouver le trafic anormal.
top = sorted(traffic.items(), key=lambda x: x[1], reverse=True)[:5]
sources = [x[0] for x in top]
counts = [x[1] for x in top]

plt.figure(figsize=(9, 5))
plt.bar(sources, counts, color="steelblue")
plt.title("Top 5 des hôtes générant le plus de trafic")
plt.xlabel("Source")
plt.ylabel("Nombre de paquets")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("top_trafic.png")
plt.show()
