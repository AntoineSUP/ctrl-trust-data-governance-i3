# Politique de contrôle et d'escalade

Supports réalisés avec assistance IA (Claude et Codex).

Équipe : 
Version : 
Date : 

Écrire la règle avant de lire les décisions de `atelier-routage.py` et de `atelier-vote.py`, puis comparer.

## 1. Règle

- Usage concerné et conséquence d'une erreur :
- Familles de questions admises, et observations des traces qui le justifient :
- Configuration de réponse (modèle seul, vote k sur n, panel) :
- Contrôle exigé avant d'utiliser une réponse, selon l'usage :
- Déclencheurs d'escalade (abstention, désaccord, question hors périmètre, donnée personnelle demandée, valeur hors plage attendue) :
- Destinataire de chaque escalade et délai de traitement :
- Conduite si le modèle ou le fournisseur est indisponible :
- Délai maximal acceptable et budget par demande :
- Conditions de restriction ou d'arrêt du service, et personne qui les décide :
- Informations conservées dans la trace pour chaque décision :

## 2. Niveaux d'escalade

| Niveau | Déclencheur | Qui traite | Délai | Action possible | Trace conservée |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

## 3. Scénarios

| ID | Situation | Action retenue | Raison tirée de la règle | Preuve ou hypothèse explicite |
|---|---|---|---|---|
| E1 | Question d'une famille fiable, modèle principal disponible | | | |
| E2 | Désaccord du panel : aucune valeur n'atteint le seuil | | | |
| E3 | Accord du panel sur une valeur découverte fausse après publication | | | |
| E4 | Modèle principal indisponible, demande qui peut attendre | | | |
| E5 | Demande urgente, aucune route admise dans le budget | | | |
| E6 | Demande de données personnelles ligne à ligne | | | |
| E7 | Usage à impact élevé, réponses concordantes | | | |

`python3 atelier-routage.py` affiche les décisions d'une règle fournie sur sept scénarios synthétiques ; `python3 atelier-vote.py --toutes --references reference-i3.csv` montre les abstentions et les accords erronés d'un panel sur les traces. Les ressources du routage sont fictives et l'exercice n'appelle aucun modèle.
