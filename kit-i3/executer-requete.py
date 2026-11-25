#!/usr/bin/env python3
"""Exécute une requête SELECT en lecture seule sur une base du kit, sans réseau.

La requête passe par `sandbox_sqlite.py` : base ouverte en lecture seule, une seule
instruction, lecture des trois tables seulement, dix lignes au plus, plafond de
travail et de temps. Une requête refusée rend son motif au lieu d'un résultat.

    python3 executer-requete.py "SELECT COUNT(*) AS lignes FROM orders"
    python3 executer-requete.py --fichier ma-requete.sql
    python3 executer-requete.py --base data/variante-degradee/boutique-variante.sqlite "SELECT COUNT(*) AS clients FROM customers"

Le résultat s'affiche en JSON : colonnes, lignes, valeur quand le résultat tient en
une ligne et une colonne, empreinte de la base interrogée.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import sandbox_sqlite  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("requete", nargs="?", help="texte de la requête SELECT")
    parser.add_argument("--fichier", type=Path, help="fichier contenant la requête")
    parser.add_argument("--base", type=Path, default=ICI / "data" / "boutique.sqlite",
                        help="base interrogée (par défaut data/boutique.sqlite)")
    args = parser.parse_args()
    if bool(args.requete) == bool(args.fichier):
        parser.error("donner soit une requête, soit --fichier")
    sql = args.fichier.read_text(encoding="utf-8") if args.fichier else args.requete
    base = args.base.resolve()
    if not base.is_file():
        parser.error(f"base introuvable : {args.base}")
    resultat = sandbox_sqlite.execute_query(base, sql)
    sortie = {
        "base": args.base.as_posix(),
        "base_sha256": hashlib.sha256(base.read_bytes()).hexdigest()[:16],
        "execution": "ok" if resultat["ok"] else ("refusée" if resultat["rejected"] else "erreur"),
        "motif": resultat["reason"],
        "detail": resultat["detail"],
        "colonnes": resultat["columns"],
        "lignes": resultat["rows"],
        "valeur": resultat["value"] if resultat["shape_ok"] else None,
        "une_ligne_une_colonne": resultat["shape_ok"],
        "duree_ms": resultat["elapsed_ms"],
    }
    print(json.dumps(sortie, ensure_ascii=False, indent=2))
    return 0 if resultat["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
