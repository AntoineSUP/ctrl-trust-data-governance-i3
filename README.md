# Ctrl+Trust — Data Governance & IA responsable (I3-APP, EFREI, BDML2)

Projet de l'équipe **Ctrl+Trust** : dossier de décision sur la mise en service d'un assistant IA (question en français → requête SQL → chiffre d'affaires) pour une boutique en ligne fictive.

## Contenu

- `kit-i3/` : kit du module (version i3-kit-2026-10-19), **non modifié**. Les commandes se lancent depuis ce dossier.
- `dossier-i3/` : les productions de l'équipe (jalon 1 : encadrement 1 du 25/11/2026).

## Commandes de base (depuis `kit-i3/`)

```bash
python3 verifier-kit.py > ../dossier-i3/integrite-kit.json
python3 analyse-traces.py resume > ../dossier-i3/inventaire-traces.json
python3 executer-requete.py "SELECT COUNT(*) AS lignes FROM orders"
```

Python 3.10 ou plus récent, bibliothèque standard uniquement. Les données sont inventées.

`dossier-i3/equipe.csv` (adresses de l'équipe) n'est pas versionné.
