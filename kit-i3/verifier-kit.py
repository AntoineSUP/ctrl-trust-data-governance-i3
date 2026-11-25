#!/usr/bin/env python3
"""Contrôle hors ligne de l'intégrité du kit I3, sans réseau ni réponse enseignant.

Reprend les contrôles de `verify-data.py` (site étudiant ESILV) : empreintes de la
base, des CSV et du schéma, `PRAGMA integrity_check` et `PRAGMA foreign_key_check`.
Ajoute l'inventaire complet du kit (`manifest.json`), la variante dégradée et les
traces historiques.

    python3 verifier-kit.py                      # résumé JSON ; code 0 si le kit est conforme
    python3 verifier-kit.py > controle-avant.json

Les gabarits et `reference-i3.csv` sont faits pour être remplis : leur modification
est signalée comme information, pas comme erreur. Un fichier ajouté dans le dossier
(vos productions) est listé sans faire échouer le contrôle.
"""
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    kit = Path(__file__).resolve().parent
    erreurs, informations = [], []
    if sys.version_info < (3, 10):
        erreurs.append("Python 3.10 ou plus récent requis, version trouvée " + sys.version.split()[0])

    inventaire = json.loads((kit / "manifest.json").read_text(encoding="utf-8"))
    attendus = inventaire["fichiers"]
    verifies = 0
    for nom, meta in sorted(attendus.items()):
        chemin = kit / nom
        if not chemin.is_file():
            erreurs.append(f"fichier absent : {nom}")
            continue
        verifies += 1
        if sha256(chemin) != meta["sha256"]:
            if meta.get("gabarit"):
                informations.append(f"gabarit rempli ou modifié : {nom}")
            else:
                erreurs.append(f"empreinte différente : {nom}")
    presents = sorted(p.relative_to(kit).as_posix() for p in kit.rglob("*")
                      if p.is_file() and "__pycache__" not in p.parts)
    ajouts = [p for p in presents if p not in attendus and p != "manifest.json"]

    donnees = json.loads((kit / "data" / "manifest.json").read_text(encoding="utf-8"))
    attendu_donnees = {"boutique.sqlite": donnees["sqlite_file_sha256"], **donnees["csv_sha256"]}
    fichiers_donnees = []
    for nom, empreinte in attendu_donnees.items():
        reel = sha256(kit / "data" / nom)
        fichiers_donnees.append({"fichier": "data/" + nom, "sha256": reel, "ok": reel == empreinte})
    schema = sha256(kit / "schema.sql")
    fichiers_donnees.append({"fichier": "schema.sql", "sha256": schema, "ok": schema == donnees["schema_sha256"]})
    for ligne in fichiers_donnees:
        if not ligne["ok"]:
            erreurs.append(f"empreinte de données différente : {ligne['fichier']}")

    with sqlite3.connect((kit / "data" / "boutique.sqlite").as_uri() + "?mode=ro", uri=True) as con:
        integrite = con.execute("PRAGMA integrity_check").fetchall()
        cles = con.execute("PRAGMA foreign_key_check").fetchall()
    if integrite != [("ok",)]:
        erreurs.append("PRAGMA integrity_check en échec sur data/boutique.sqlite")
    if cles:
        erreurs.append("PRAGMA foreign_key_check en échec sur data/boutique.sqlite")

    variante = json.loads((kit / "data" / "variante-degradee" / "manifest.json").read_text(encoding="utf-8"))
    for nom, empreinte in variante["sha256"].items():
        if sha256(kit / "data" / "variante-degradee" / nom) != empreinte:
            erreurs.append(f"empreinte différente : data/variante-degradee/{nom}")

    traces = kit / "traces" / "traces-pilote-2026-09-25.jsonl"
    lignes = [json.loads(l) for l in traces.read_text(encoding="utf-8").splitlines() if l.strip()]
    interdits = {"reference", "reference_variant", "verdict", "verdict_variant", "value_variant", "status"}
    fuites = sorted({cle for ligne in lignes for cle in ligne if cle in interdits})
    if fuites:
        erreurs.append(f"champs de correction présents dans les traces : {fuites}")

    resultat = {
        "python": sys.version.split()[0],
        "sqlite": sqlite3.sqlite_version,
        "version_kit": inventaire.get("version"),
        "fichiers_inventories": len(attendus),
        "fichiers_verifies": verifies,
        "donnees": fichiers_donnees,
        "integrite_sqlite": integrite == [("ok",)],
        "cles_etrangeres": not cles,
        "traces": len(lignes),
        "ajouts_dans_le_dossier": ajouts,
        "informations": informations,
        "erreurs": erreurs,
        "ok": not erreurs,
    }
    print(json.dumps(resultat, ensure_ascii=False, indent=2))
    return 0 if not erreurs else 1


if __name__ == "__main__":
    raise SystemExit(main())
