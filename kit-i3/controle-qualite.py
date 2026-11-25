#!/usr/bin/env python3
"""Exécute les règles qualité d'un fichier CSV sur une ou plusieurs bases, sans réseau.

Chaque règle porte une requête de contrôle qui rend une ligne et une colonne : le
nombre d'écarts constatés (0 signifie conforme). Colonnes lues dans le CSV :
`id_regle`, `requete_controle` et, si elle est renseignée, `seuil_acceptation`
(nombre maximal d'écarts admis, 0 par défaut). Les autres colonnes sont ignorées.

    python3 controle-qualite.py --regles mes-regles-qualite.csv
    python3 controle-qualite.py --regles mes-regles-qualite.csv \\
        --base data/boutique.sqlite --base data/variante-degradee/boutique-variante.sqlite \\
        --sortie resultats-qualite.csv

Partir d'une copie de `gabarits/regles-qualite.csv`. Les requêtes passent par le
bac à sable en lecture seule : SELECT sur les trois tables, une instruction.
"""
import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import sandbox_sqlite  # noqa: E402

BASES_PAR_DEFAUT = [ICI / "data" / "boutique.sqlite",
                    ICI / "data" / "variante-degradee" / "boutique-variante.sqlite"]
COLONNES_SORTIE = ["id_regle", "base", "base_sha256", "ecarts", "seuil_acceptation", "statut", "detail"]


def lire_regles(chemin: Path) -> list:
    with chemin.open(encoding="utf-8", newline="") as flux:
        lignes = list(csv.DictReader(flux))
    regles = []
    for ligne in lignes:
        identifiant = (ligne.get("id_regle") or "").strip()
        requete = (ligne.get("requete_controle") or "").strip()
        if not identifiant or not requete:
            continue
        seuil = (ligne.get("seuil_acceptation") or "").strip()
        regles.append({"id_regle": identifiant, "requete": requete, "seuil": int(seuil) if seuil else 0})
    return regles


def controler(regle: dict, base: Path) -> dict:
    resultat = sandbox_sqlite.execute_query(base, regle["requete"])
    sortie = {"id_regle": regle["id_regle"], "base": base.name,
              "base_sha256": hashlib.sha256(base.read_bytes()).hexdigest()[:16],
              "ecarts": "", "seuil_acceptation": regle["seuil"], "statut": "erreur", "detail": ""}
    if not resultat["ok"]:
        sortie["detail"] = (resultat["reason"] + " " + resultat["detail"]).strip()
    elif not resultat["shape_ok"]:
        sortie["detail"] = "la requête doit rendre une ligne et une colonne : " + resultat["detail"]
    elif not isinstance(resultat["value"], int):
        sortie["detail"] = f"valeur non entière : {resultat['value']!r}"
    else:
        sortie["ecarts"] = resultat["value"]
        sortie["statut"] = "conforme" if resultat["value"] <= regle["seuil"] else "écart"
    return sortie


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--regles", type=Path, required=True, help="CSV des règles qualité")
    parser.add_argument("--base", type=Path, action="append", help="base contrôlée (répéter l'option)")
    parser.add_argument("--sortie", type=Path, help="CSV des résultats")
    args = parser.parse_args()
    bases = [b.resolve() for b in (args.base or BASES_PAR_DEFAUT)]
    for base in bases:
        if not base.is_file():
            parser.error(f"base introuvable : {base}")
    regles = lire_regles(args.regles)
    if not regles:
        parser.error("aucune règle avec id_regle et requete_controle dans le fichier")
    resultats = [controler(regle, base) for regle in regles for base in bases]
    for ligne in resultats:
        print(f"{ligne['id_regle']:10} {ligne['base']:28} {str(ligne['ecarts']):>6}  {ligne['statut']:9} {ligne['detail']}")
    if args.sortie:
        with args.sortie.open("w", encoding="utf-8", newline="") as flux:
            ecrivain = csv.DictWriter(flux, fieldnames=COLONNES_SORTIE, lineterminator="\n")
            ecrivain.writeheader()
            ecrivain.writerows(resultats)
    bilan = {"regles": len(regles), "bases": [b.name for b in bases],
             "conformes": sum(r["statut"] == "conforme" for r in resultats),
             "ecarts": sum(r["statut"] == "écart" for r in resultats),
             "erreurs": sum(r["statut"] == "erreur" for r in resultats)}
    print(json.dumps(bilan, ensure_ascii=False))
    return 1 if bilan["erreurs"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
