# Rapport d'analyse du trafic réseau

## 1. Objectif du TP
L'objectif de ce TP est d'analyser un trafic réseau à partir d'une capture
afin de détecter des activités suspectes telles que :
- attaques par force brute SSH
- scans de ports
- trafic anormal (saturation du réseau)

## 2. Méthodologie
Le programme Python lit un fichier `capture.csv` et analyse :
- le nombre de connexions SSH par hôte
- le nombre de ports distincts testés par source
- le volume de paquets envoyés par chaque source

Des seuils simples sont utilisés pour identifier les comportements suspects.

## 3. Résultats obtenus

### 3.1 Activité SSH suspecte
Les hôtes présentant plus de 20 tentatives SSH sont considérés comme suspects.

### 3.2 Scan de ports
Un scan est détecté lorsqu'une source teste plus de 10 ports différents.

### 3.3 Trafic anormal
Un trafic supérieur à 100 paquets indique une possible saturation du réseau.

## 4. Illustration graphique
Le graphique ci-dessous présente les 5 hôtes générant le plus de trafic.

![Top 5 du trafic](top_trafic.png)

## 5. Conclusion
L'analyse a permis d'identifier plusieurs comportements suspects.
Ce script constitue une base simple mais efficace pour la détection
d'activités malveillantes sur un réseau.
