from collections import defaultdict

fichier = "capture.txt"

ssh_counter = defaultdict(int)

with open(fichier, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        # On ne garde QUE les vraies lignes réseau
        if " IP " not in line:
            continue

        # SSH identifié par le service .ssh
        if ".ssh" in line.lower():
            try:
                source = line.split(" IP ")[1].split(" > ")[0]
                ssh_counter[source] += 1
            except IndexError:
                pass

# AFFICHAGE
if not ssh_counter:
    print("❌ Aucun trafic SSH détecté")
else:
    print("✅ Activité SSH détectée :")
    for src, count in sorted(ssh_counter.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{src} → {count} paquets SSH")
