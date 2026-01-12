import csv
import re

input_file = "capture.txt"
output_file = "capture.csv"

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
