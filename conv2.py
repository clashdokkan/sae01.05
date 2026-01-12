import csv
import re

input_file = "capture.txt"
output_file = "capture2.csv"

pattern = re.compile(
    r"(?P<time>\d{2}:\d{2}:\d{2}\.\d+)\s+IP\s+"
    r"(?P<src>[^ ]+)\s+>\s+"
    r"(?P<dst_ip>\d+\.\d+\.\d+\.\d+)\.(?P<dst_port>\d+).*"
    r"Flags\s+\[(?P<flags>[^\]]+)\].*"
    r"length\s+(?P<length>\d+)"
)

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
        if line.lstrip().startswith("0x"):
            continue

        match = pattern.search(line)
        if match:
            writer.writerow([
                match.group("time"),
                match.group("src"),
                match.group("dst_ip"),
                match.group("dst_port"),
                match.group("flags"),
                match.group("length")
            ])

print("CSV enrichi généré avec succès.")



from collections import defaultdict
import matplotlib.pyplot as plt

fichier = "capture.txt"

# Compteurs
ip_counter = defaultdict(int)
ssh_counter = defaultdict(int)

with open(fichier, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if " IP " not in line:
            continue

        try:
            source = line.split(" IP ")[1].split(" > ")[0]
            ip_counter[source] += 1

            # Trafic SSH
            if ".ssh" in source.lower():
                ssh_counter[source] += 1

        except IndexError:
            pass

# -------------------------
# TOP 5 IP les plus actives
# -------------------------
top_ips = sorted(ip_counter.items(), key=lambda x: x[1], reverse=True)[:5]

ips = [ip for ip, _ in top_ips]
counts = [count for _, count in top_ips]

plt.figure(figsize=(9, 5))
plt.bar(ips, counts, color="cornflowerblue")
plt.title("Top 5 des hôtes / IP les plus actifs")
plt.xlabel("Hôte / IP source")
plt.ylabel("Nombre de paquets")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("top_ips.png")
plt.show()

# -------------------------
# Camembert trafic SSH
# -------------------------
if ssh_counter:
    ssh_top = sorted(ssh_counter.items(), key=lambda x: x[1], reverse=True)[:5]

    labels = [ip for ip, _ in ssh_top]
    values = [count for _, count in ssh_top]

    plt.figure(figsize=(7, 7))
    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Répartition du trafic SSH")
    plt.axis("equal")
    plt.savefig("ssh_camembert.png")
    plt.show()
else:
    print("Aucun trafic SSH détecté.")
