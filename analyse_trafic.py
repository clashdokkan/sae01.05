#python -m markdown rapport.md > rapport.html commande pour pouvoir tranformer le fichier en fichier html  
import csv
import re
import tkinter as tk
from tkinter import filedialog
import os
def choisir_fichier():
    root = tk.Tk()
    root.withdraw()  # cache la fenêtre principale
    fichier = filedialog.askopenfilename(
        title="Sélectionnez le fichier de capture",
        filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
    )
    return fichier
input_file = choisir_fichier()

if not input_file:
    print("❌ Aucun fichier sélectionné")
    exit()

output_file = os.path.splitext(input_file)[0] + ".csv"

#output_file = "capture.csv"

# Regex souple pour toutes les lignes IP
pattern = re.compile(
    r"(?P<time>\d{2}:\d{2}:\d{2}\.\d+)\s+IP\s+"
    r"(?P<src>[^ ]+)\s+>\s+"
    r"(?P<dst>[^:]+):"
)

# Regex secondaires pour Flags et Taille
flags_re = re.compile(r"Flags\s+\[([^\]]+)\]")
length_re = re.compile(r"length\s+(\d+)")

with open(input_file, "r", encoding="utf-8", errors="ignore") as f, \
     open(output_file, "w", newline="", encoding="utf-8") as csvfile:

    writer = csv.writer(csvfile, delimiter=";")
    writer.writerow([
        "Heure",
        "Source",
        "IP_Destination",
        "Port_Destination",
        "Flags",
        "Taille"
    ])

    for line in f:
        # Ignorer les lignes hexadécimales
        if line.lstrip().startswith("0x"):
            continue

        match = pattern.search(line)
        if not match:
            continue

        heure = match.group("time")
        source = match.group("src")
        dst_full = match.group("dst")

        # Séparer IP et Port
        if "." in dst_full and dst_full.split(".")[-1].isdigit():
            dst_parts = dst_full.split(".")
            dst_ip = ".".join(dst_parts[:-1])
            dst_port = dst_parts[-1]
        else:
            dst_ip = dst_full
            dst_port = ""

        # Flags optionnels
        flags_match = flags_re.search(line)
        flags = flags_match.group(1) if flags_match else ""

        # Taille optionnelle
        length_match = length_re.search(line)
        taille = length_match.group(1) if length_match else ""

        writer.writerow([
            heure,
            source,
            dst_ip,
            dst_port,
            flags,
            taille
        ])

print("✅ CSV généré avec IP et Port séparés.")
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

csv_file = "capture.csv"
rapport_md = "rapport.md"

# ======================
# ANALYSE SSH
# ======================
ssh_counter = defaultdict(int)

with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        if row["Port_Destination"] == "22":
            ssh_counter[row["Source"]] += 1

ssh_alerts = {src: c for src, c in ssh_counter.items() if c > 20}

# ======================
# SCAN DE PORTS
# ======================
scan = defaultdict(set)

with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        if row["Port_Destination"]:
            scan[row["Source"]].add(row["Port_Destination"])

scan_alerts = {src: ports for src, ports in scan.items() if len(ports) > 10}

# ======================
# TRAFIC GLOBAL
# ======================
traffic = defaultdict(int)

with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        traffic[row["Source"]] += 1

traffic_alerts = {src: c for src, c in traffic.items() if c > 100}
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

# ======================
# GRAPHIQUE TOP 5
# ======================
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
plt.close()




# ======================
# GÉNÉRATION DU RAPPORT MARKDOWN (avec résultats texte et graphiques)
# ======================
rapport_md = "rapport.md"

with open(rapport_md, "w", encoding="utf-8") as f:
    f.write("# Rapport d'analyse du trafic réseau\n\n")

    f.write("## Objectif\n")
    f.write(
        "Analyser une capture réseau afin de détecter des comportements "
        "suspects comme les attaques SSH, les scans de ports et le trafic anormal.\n\n"
    )

    f.write("## Activité SSH suspecte\n")
    if ssh_alerts:
        for src, count in ssh_alerts.items():
            f.write(f"- {src} : {count} tentatives SSH ⚠️\n")
    else:
        f.write("Aucune activité SSH suspecte détectée ✅\n")
    f.write("\n")

    # Génération graphique SSH pour le Markdown
    if ssh_alerts:
        sources_ssh = list(ssh_alerts.keys())
        counts_ssh = list(ssh_alerts.values())
        plt.figure(figsize=(8,4))
        plt.bar(sources_ssh, counts_ssh, color="red")
        plt.title("SSH suspect : top sources")
        plt.xlabel("Source")
        plt.ylabel("Nombre de tentatives")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig("ssh_alertes.png")
        plt.close()
        f.write("![Activité SSH](ssh_alertes.png)\n\n")

    f.write("## Scan de ports suspect\n")
    if scan_alerts:
        for src, ports in scan_alerts.items():
            f.write(f"- {src} : {len(ports)} ports testés ⚠️\n")
        # Graphique scan de ports
        plt.figure(figsize=(8,4))
        plt.bar(scan_alerts.keys(), [len(p) for p in scan_alerts.values()], color="orange")
        plt.title("Scan de ports suspect")
        plt.xlabel("Source")
        plt.ylabel("Nombre de ports testés")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig("scan_ports.png")
        plt.close()
        f.write("![Scan de ports](scan_ports.png)\n\n")
    else:
        f.write("Aucun scan de ports détecté ✅\n\n")

    f.write("## Trafic anormal\n")
    if traffic_alerts:
        for src, count in traffic_alerts.items():
            f.write(f"- {src} : {count} paquets envoyés ⚠️\n")
    else:
        f.write("Aucun trafic anormal détecté ✅\n")

    # Graphique Top 5 trafic
    f.write("\n### Top 5 des hôtes générant le plus de trafic\n")
    f.write("![Top trafic](top_trafic.png)\n\n")

    f.write("## Conclusion\n")
    f.write(
        "Cette analyse met en évidence plusieurs comportements potentiellement "
        "malveillants. Le rapport inclut désormais les alertes SSH, scan de ports "
        "et trafic anormal sous forme texte et graphique.\n"
    )

print("✅ Rapport Markdown mis à jour avec texte et graphiques : rapport.md")

with open(rapport_md, "w", encoding="utf-8") as f:
    f.write("# Rapport d'analyse du trafic réseau\n\n")

    f.write("## Objectif\n")
    f.write(
        "Analyser une capture réseau afin de détecter des comportements "
        "suspects comme les attaques SSH, les scans de ports et le trafic anormal.\n\n"
    )

    f.write("## Résultats\n\n")

    f.write("### Activité SSH suspecte\n")
    if ssh_alerts:
        for src, count in ssh_alerts.items():
            f.write(f"- {src} : {count} tentatives SSH\n")
    else:
        f.write("Aucune activité SSH suspecte détectée.\n")
    f.write("\n")

    f.write("### Scan de ports\n")
    if scan_alerts:
        for src, ports in scan_alerts.items():
            f.write(f"- {src} : {len(ports)} ports testés\n")
    else:
        f.write("Aucun scan de ports détecté.\n")
    f.write("\n")

    f.write("### Trafic anormal\n")
    if traffic_alerts:
        for src, count in traffic_alerts.items():
            f.write(f"- {src} : {count} paquets envoyés\n")
    else:
        f.write("Aucun trafic anormal détecté.\n")
    f.write("\n")

    f.write("## Illustration\n")
    f.write("Le graphique ci-dessous montre les 5 hôtes générant le plus de trafic.\n\n")
    f.write("![Top trafic](top_trafic.png)\n\n")

    f.write("## Conclusion\n")
    f.write(
        "Cette analyse met en évidence plusieurs comportements potentiellement "
        "malveillants. Le script peut être amélioré par l'analyse des flags TCP "
        "et l'automatisation complète du rapport HTML.\n"
    )

print("✅ Rapport Markdown généré : rapport.md")
print("✅ Graphique généré : top_trafic.png")
