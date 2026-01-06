from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent
ics_path = BASE_DIR / "evenementSAE_15_2025.ics"
csv_path = BASE_DIR / "evenementSAE_15_2025.csv"

events = []
event = {}

with open(ics_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if line == "BEGIN:VEVENT":
            event = {}
        elif line.startswith("SUMMARY:"):
            event["title"] = line.replace("SUMMARY:", "")
        elif line.startswith("DTSTART:"):
            event["start"] = line.replace("DTSTART:", "")
        elif line.startswith("DTEND:"):
            event["end"] = line.replace("DTEND:", "")
        elif line.startswith("LOCATION:"):
            event["location"] = line.replace("LOCATION:", "")
        elif line.startswith("DESCRIPTION:"):
            event["description"] = line.replace("DESCRIPTION:", "")
        elif line == "END:VEVENT":
            events.append(event)

# Écriture CSV (pseudo CSV avec ;)
with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter=";")
    writer.writerow(["title", "start", "end", "location", "description"])

    for e in events:
        writer.writerow([
            e.get("title", ""),
            e.get("start", ""),
            e.get("end", ""),
            e.get("location", ""),
            e.get("description", "")
        ])

print("Conversion terminée ✔")