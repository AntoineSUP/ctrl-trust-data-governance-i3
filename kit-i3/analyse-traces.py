#!/usr/bin/env python3
"""Analyse hors ligne des traces historiques de l'assistant (pilote du 25/09/2026).

Aucun appel réseau, aucune clé. Chaque trace donne la requête SQL rendue par un
modèle et la valeur obtenue le 25/09/2026. Les traces ne contiennent ni référence
ni verdict : le verdict vient de VOS références indépendantes (`reference-i3.csv`).

    python3 analyse-traces.py resume
    python3 analyse-traces.py rejouer --references reference-i3.csv
    python3 analyse-traces.py rejouer --references reference-i3.csv --lot 2 --sortie rejeu-traces.csv
    python3 analyse-traces.py rejouer --references reference-i3.csv \\
        --base data/variante-degradee/boutique-variante.sqlite --sortie rejeu-variante.csv
    python3 analyse-traces.py accords --rejeu rejeu-traces.csv

`rejouer` réexécute chaque requête dans le bac à sable en lecture seule, compare la
valeur obtenue à la valeur de la trace et à votre référence, puis compte les
résultats par modèle et par famille de questions. Les lignes produites portent la
nature `rejeu` : latence, tokens et coût restent ceux mesurés le 25/09/2026.
`accords` liste, question par question, les valeurs rendues par au moins deux
modèles et indique si elles sont justes au regard de votre référence.

Un taux s'écrit avec son effectif : « 18 justes sur 20 cas », jamais « 90 % » seul.
"""
import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import sandbox_sqlite  # noqa: E402

TRACES = ICI / "traces" / "traces-pilote-2026-09-25.jsonl"
QUESTIONS = ICI / "questions-i3.json"
BASE = ICI / "data" / "boutique.sqlite"
VERDICTS = ["juste", "faux", "sql_invalide", "sql_refuse", "non_execute", "sans_reference"]
COLONNES_REJEU = [
    "cell_id", "lot", "provider", "model_requested", "family_model", "case_id", "famille_question",
    "nature", "base", "base_sha256", "sql", "statut_execution", "valeur_trace", "valeur_rejouee",
    "valeur_identique", "reference", "verdict", "detail", "date_utc", "latency_ms",
    "tokens_prompt", "tokens_completion", "tokens_reasoning", "cost_native", "attempts",
]


def vide(valeur) -> str:
    return "" if valeur is None else str(valeur)


def entier_ou_rien(valeur):
    if valeur is None or valeur == "":
        return None
    return int(valeur)


def lire_traces(chemin: Path) -> list:
    if chemin.suffix.lower() == ".csv":
        with chemin.open(encoding="utf-8", newline="") as flux:
            lignes = list(csv.DictReader(flux))
        for ligne in lignes:
            ligne["lot"] = int(ligne["lot"])
            ligne["value"] = entier_ou_rien(ligne.get("value"))
        return lignes
    return [json.loads(l) for l in chemin.read_text(encoding="utf-8").splitlines() if l.strip()]


def lire_questions() -> dict:
    donnees = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    return {q["id"]: q for q in donnees["questions"]}


def lire_references(chemin) -> dict:
    """reference-i3.csv : case_id, sql, revenue_cents, controle_par, methode_controle."""
    references = {}
    if chemin is None:
        return references
    with Path(chemin).open(encoding="utf-8", newline="") as flux:
        for ligne in csv.DictReader(flux):
            valeur = (ligne.get("revenue_cents") or "").strip()
            if valeur:
                references[ligne["case_id"].strip()] = int(valeur)
    return references


def comparer(valeur, reference) -> tuple:
    """Égalité stricte des nombres ; un NULL n'est jamais égal à une référence."""
    if reference is None:
        return "sans_reference", "aucune référence pour cette question dans le fichier"
    if valeur is None:
        return "faux", "NULL au lieu de 0" if reference == 0 else "NULL au lieu d'un nombre"
    return ("juste", "") if valeur == reference else ("faux", "valeur différente de la référence")


def rejouer_trace(trace: dict, base: Path, empreinte_base: str, references: dict, questions: dict) -> dict:
    sql = trace.get("sql") or ""
    ligne = {cle: vide(trace.get(cle)) for cle in COLONNES_REJEU if cle in trace}
    ligne.update(nature="rejeu", base=base.name, base_sha256=empreinte_base, sql=sql,
                 famille_question=questions.get(trace["case_id"], {}).get("famille", ""),
                 valeur_trace=vide(trace.get("value")), valeur_rejouee="", valeur_identique="",
                 reference=vide(references.get(trace["case_id"])))
    if not sql:
        if trace.get("statut_execution") == "sql_invalide":
            ligne.update(verdict="sql_invalide", detail=trace.get("detail_execution") or "aucune requête")
        else:
            ligne.update(verdict="non_execute",
                         detail=f"{trace.get('statut_execution')} : {trace.get('detail_execution') or ''}".strip(" :"))
        return ligne
    resultat = sandbox_sqlite.execute_query(base, sql)
    if resultat["rejected"]:
        ligne.update(verdict="sql_refuse", detail=(resultat["reason"] + " " + resultat["detail"]).strip())
    elif not resultat["ok"]:
        ligne.update(verdict="sql_invalide", detail=(resultat["reason"] + " " + resultat["detail"]).strip())
    elif not resultat["shape_ok"]:
        ligne.update(verdict="sql_invalide", detail="forme : " + resultat["detail"])
    elif resultat["columns"] != ["revenue_cents"]:
        ligne.update(verdict="sql_invalide", detail="colonne revenue_cents attendue")
    else:
        valeur = resultat["value"]
        verdict, detail = comparer(valeur, references.get(trace["case_id"]))
        ligne.update(valeur_rejouee=vide(valeur), verdict=verdict, detail=detail,
                     valeur_identique="oui" if vide(valeur) == vide(trace.get("value")) else "non")
    return ligne


def modele(ligne: dict) -> str:
    return f"{ligne['provider']}:{ligne['model_requested']}"


def tableau_modeles(lignes: list) -> list:
    table = {}
    for ligne in lignes:
        cle = (int(ligne["lot"]), modele(ligne))
        rang = table.setdefault(cle, {"lot": cle[0], "modele": cle[1], "cas": 0, **{v: 0 for v in VERDICTS}})
        rang["cas"] += 1
        rang[ligne["verdict"]] += 1
    return [table[c] for c in sorted(table)]


def tableau_familles(lignes: list) -> list:
    table = {}
    for ligne in lignes:
        cle = (int(ligne["lot"]), ligne["famille_question"])
        rang = table.setdefault(cle, {"lot": cle[0], "famille": cle[1], "cellules": 0, "evaluees": 0, "justes": 0,
                                      "non_evaluees": 0})
        rang["cellules"] += 1
        if ligne["verdict"] in ("juste", "faux"):
            rang["evaluees"] += 1
            rang["justes"] += ligne["verdict"] == "juste"
        else:
            rang["non_evaluees"] += 1
    return [table[c] for c in sorted(table)]


def afficher_modeles(rangs: list) -> None:
    entete = f"{'lot':>3} {'modèle':58} {'cas':>4} {'justes':>6} {'faux':>5} {'sql inv.':>8} {'refusés':>7} {'non exéc.':>9} {'sans réf.':>9}"
    print(entete)
    print("-" * len(entete))
    for r in rangs:
        print(f"{r['lot']:>3} {r['modele']:58} {r['cas']:>4} {r['juste']:>6} {r['faux']:>5} {r['sql_invalide']:>8} "
              f"{r['sql_refuse']:>7} {r['non_execute']:>9} {r['sans_reference']:>9}")


def afficher_familles(rangs: list) -> None:
    print()
    entete = f"{'lot':>3} {'famille de questions':58} {'cellules':>8} {'évaluées':>8} {'justes':>6}"
    print(entete)
    print("-" * len(entete))
    for r in rangs:
        print(f"{r['lot']:>3} {r['famille']:58} {r['cellules']:>8} {r['evaluees']:>8} {r['justes']:>6}")


def commande_resume(args) -> int:
    traces = lire_traces(args.traces)
    dates = sorted(t["date_utc"] for t in traces if t.get("date_utc"))
    resume = {
        "fichier": args.traces.name,
        "traces": len(traces),
        "cellules_uniques": len({t["cell_id"] for t in traces}),
        "premiere_date_utc": dates[0] if dates else None,
        "derniere_date_utc": dates[-1] if dates else None,
        "par_lot": {str(lot): n for lot, n in sorted(Counter(t["lot"] for t in traces).items())},
        "modeles_par_lot": {str(lot): len({modele(t) for t in traces if t["lot"] == lot})
                            for lot in sorted({t["lot"] for t in traces})},
        "questions_par_lot": {str(lot): sorted({t["case_id"] for t in traces if t["lot"] == lot})
                              for lot in sorted({t["lot"] for t in traces})},
        "par_fournisseur": dict(sorted(Counter(t["provider"] for t in traces).items())),
        "statut_execution": dict(sorted(Counter(t["statut_execution"] for t in traces).items())),
        "cellules_avec_reprise": sum(int(t.get("attempts") or 1) > 1 for t in traces),
        "cout_natif_renseigne": sum(t.get("cost_native") not in (None, "") for t in traces),
        "nature": dict(Counter(t.get("nature") for t in traces)),
    }
    print(json.dumps(resume, ensure_ascii=False, indent=1))
    return 0


def commande_rejouer(args) -> int:
    traces = lire_traces(args.traces)
    if args.lot:
        traces = [t for t in traces if t["lot"] == args.lot]
    questions = lire_questions()
    references = lire_references(args.references)
    base = args.base.resolve()
    empreinte = hashlib.sha256(base.read_bytes()).hexdigest()[:16]
    lignes = [rejouer_trace(t, base, empreinte, references, questions)
              for t in sorted(traces, key=lambda t: (t["lot"], t["provider"], t["model_requested"], t["case_id"]))]
    afficher_modeles(tableau_modeles(lignes))
    afficher_familles(tableau_familles(lignes))
    if args.sortie:
        with args.sortie.open("w", encoding="utf-8", newline="") as flux:
            ecrivain = csv.DictWriter(flux, fieldnames=COLONNES_REJEU, lineterminator="\n", extrasaction="ignore")
            ecrivain.writeheader()
            ecrivain.writerows(lignes)
    executees = [l for l in lignes if l["valeur_identique"]]
    bilan = {"base": base.name, "base_sha256": empreinte, "traces_rejouees": len(lignes),
             "references_lues": len(references),
             "verdicts": {v: sum(l["verdict"] == v for l in lignes) for v in VERDICTS},
             "requetes_executees": len(executees),
             "valeurs_identiques_a_la_trace": sum(l["valeur_identique"] == "oui" for l in executees),
             "sortie": args.sortie.name if args.sortie else None}
    print()
    print(json.dumps(bilan, ensure_ascii=False))
    return 0


def lire_rejeu(chemin: Path) -> list:
    with chemin.open(encoding="utf-8", newline="") as flux:
        return list(csv.DictReader(flux))


def calculer_accords(lignes: list) -> list:
    groupes = defaultdict(lambda: defaultdict(list))
    references = {}
    for ligne in lignes:
        if ligne["verdict"] not in ("juste", "faux", "sans_reference") or ligne["valeur_rejouee"] == "":
            continue
        cle = (int(ligne["lot"]), ligne["case_id"])
        groupes[cle][int(ligne["valeur_rejouee"])].append(modele(ligne))
        if ligne["reference"] != "":
            references[cle] = int(ligne["reference"])
    accords = []
    for cle in sorted(groupes):
        valeurs = groupes[cle]
        for valeur, modeles in sorted(valeurs.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            if len(modeles) < 2:
                continue
            reference = references.get(cle)
            accords.append({"lot": cle[0], "question": cle[1], "valeur": valeur, "modeles": sorted(modeles),
                            "nombre": len(modeles), "valeurs_distinctes_sur_la_question": len(valeurs),
                            "au_regard_de_la_reference": "sans référence" if reference is None
                            else ("juste" if valeur == reference else "accord erroné")})
    return accords


def commande_accords(args) -> int:
    lignes = lire_rejeu(args.rejeu)
    if args.lot:
        lignes = [l for l in lignes if int(l["lot"]) == args.lot]
    accords = calculer_accords(lignes)
    for accord in accords:
        if args.erreurs_seulement and accord["au_regard_de_la_reference"] != "accord erroné":
            continue
        print(json.dumps(accord, ensure_ascii=False))
    print(json.dumps({"accords": len(accords),
                      "accords_errones": sum(a["au_regard_de_la_reference"] == "accord erroné" for a in accords),
                      "questions_avec_desaccord": len({(a["lot"], a["question"]) for a in accords
                                                       if a["valeurs_distinctes_sur_la_question"] > 1})},
                     ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sous = parser.add_subparsers(dest="commande", required=True)
    resume = sous.add_parser("resume", help="inventaire des traces")
    resume.add_argument("--traces", type=Path, default=TRACES)
    rejouer = sous.add_parser("rejouer", help="rejouer les requêtes et compter les verdicts")
    rejouer.add_argument("--traces", type=Path, default=TRACES)
    rejouer.add_argument("--references", type=Path, help="votre reference-i3.csv rempli")
    rejouer.add_argument("--base", type=Path, default=BASE)
    rejouer.add_argument("--lot", type=int, choices=[1, 2])
    rejouer.add_argument("--sortie", type=Path, help="CSV du rejeu")
    accords = sous.add_parser("accords", help="valeurs partagées par au moins deux modèles")
    accords.add_argument("--rejeu", type=Path, required=True, help="CSV produit par la commande rejouer")
    accords.add_argument("--lot", type=int, choices=[1, 2])
    accords.add_argument("--erreurs-seulement", action="store_true", help="n'afficher que les accords erronés")
    args = parser.parse_args()
    return {"resume": commande_resume, "rejouer": commande_rejouer, "accords": commande_accords}[args.commande](args)


if __name__ == "__main__":
    raise SystemExit(main())
