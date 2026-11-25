#!/usr/bin/env python3
"""Vote k sur n : exemples synthétiques, ou traces historiques d'une question, sans réseau.

Le vote décide sans connaître la référence ; la comparaison avec votre référence
vient après la décision. Le panel garde sa taille n : un membre indisponible, en
erreur ou dont la requête rend NULL reste dans n et ne vote pas. Un accord ne
prouve pas l'exactitude : deux modèles peuvent se tromper ensemble.

    python3 atelier-vote.py                                         # quatre exemples synthétiques
    python3 atelier-vote.py --question C02                          # traces du lot 2, panel par défaut, k = 2
    python3 atelier-vote.py --question C02 --references reference-i3.csv
    python3 atelier-vote.py --toutes --references reference-i3.csv --sortie votes-panel.csv
    python3 atelier-vote.py --toutes --k 2 --panel groq:openai/gpt-oss-120b,groq:openai/gpt-oss-20b,openrouter:stealth/space-bunny-alpha

Panel par défaut : trois familles de modèles distinctes présentes dans le lot 2.
Le vote est fourni ; le travail porte sur le choix du panel et du seuil, sur la
lecture des abstentions et des accords erronés, et sur la conduite à tenir
(acceptation, contrôle, escalade vers une revue humaine).
"""
import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

sys.dont_write_bytecode = True
ICI = Path(__file__).resolve().parent
TRACES = ICI / "traces" / "traces-pilote-2026-09-25.jsonl"
PANEL_DEFAUT = [
    "groq:openai/gpt-oss-120b",
    "openrouter:inclusionai/ling-3.0-flash-sante:free",
    "groq:qwen/qwen3.8-27b",
]
QUESTIONS = [f"C{i:02d}" for i in range(1, 21)]


def vote_k_sur_n(propositions: list, k: int) -> dict:
    """Vote à la majorité stricte : seules les propositions exécutées avec une valeur votent."""
    n = len(propositions)
    if not n // 2 < k <= n:
        raise ValueError("le seuil k doit être une majorité stricte : n // 2 < k <= n")
    membres = [f"{p.provider}:{p.model_requested}" for p in propositions]
    if len(set(membres)) != n:
        raise ValueError("membre en double dans le panel : un doublon n'est pas une seconde voix")
    valides = [p for p in propositions if p.statut == "valeur_obtenue" and p.valeur is not None]
    comptes = Counter(p.valeur for p in valides)
    valeur, voix = comptes.most_common(1)[0] if comptes else (None, 0)
    consensus = voix >= k
    return {"consensus": consensus, "valeur": valeur if consensus else None, "voix": voix,
            "modeles": [f"{p.provider}:{p.model_requested}" for p in valides if p.valeur == valeur]
            if consensus else []}


def suite(decision: dict) -> str:
    if decision["consensus"]:
        return "réponse proposée ; contrôle selon la politique d'escalade avant usage"
    return "abstention ; escalade vers une revue humaine"


def lire_traces(chemin: Path) -> list:
    if chemin.suffix.lower() == ".csv":
        with chemin.open(encoding="utf-8", newline="") as flux:
            lignes = list(csv.DictReader(flux))
        for ligne in lignes:
            ligne["lot"] = int(ligne["lot"])
            ligne["value"] = int(ligne["value"]) if ligne.get("value") not in (None, "") else None
        return lignes
    return [json.loads(l) for l in chemin.read_text(encoding="utf-8").splitlines() if l.strip()]


def lire_references(chemin) -> dict:
    if chemin is None:
        return {}
    with Path(chemin).open(encoding="utf-8", newline="") as flux:
        return {l["case_id"].strip(): int(l["revenue_cents"]) for l in csv.DictReader(flux)
                if (l.get("revenue_cents") or "").strip()}


def propositions_pour(traces: list, question: str, lot: int, panel: list) -> list:
    """Dernier état de chaque membre du panel sur la question ; ni référence ni verdict transmis."""
    retenues = {}
    for trace in traces:
        cle = f"{trace['provider']}:{trace['model_requested']}"
        if trace["case_id"] == question and trace["lot"] == lot and cle in panel:
            retenues[cle] = trace
    propositions = []
    for membre in panel:
        fournisseur, _, modele = membre.partition(":")
        trace = retenues.get(membre, {})
        propositions.append(SimpleNamespace(provider=fournisseur, model_requested=modele,
                                            valeur=trace.get("value"),
                                            statut=trace.get("statut_execution", "absent")))
    return propositions


def evaluer(propositions: list, k: int, reference) -> dict:
    decision = vote_k_sur_n(propositions, k)
    if reference is None:
        issue = "non évaluée"
    elif not decision["consensus"]:
        issue = "abstention"
    else:
        issue = "juste" if decision["valeur"] == reference else "accord erroné"
    return {"decision": decision, "suite": suite(decision), "reference": reference, "issue": issue}


def exemples_synthetiques() -> list:
    """Valeurs inventées, en centimes : ce ne sont pas des résultats sur la base de la boutique."""
    panel = [("demo", "modele-A"), ("demo", "modele-B"), ("demo", "modele-C")]
    sorties = []
    for nom, valeurs, reference in [
        ("accord", [100, 100, 120], 100),
        ("désaccord", [100, 110, 120], 100),
        ("membres indisponibles", [100, None, None], 100),
        ("accord erroné", [0, 0, 100], 100),
    ]:
        propositions = [SimpleNamespace(provider=p, model_requested=m, valeur=v,
                                        statut="valeur_obtenue" if v is not None else "erreur_acces")
                        for (p, m), v in zip(panel, valeurs)]
        sorties.append({"exemple": nom, "nature": "simulation", "n": 3, "k": 2,
                        "valeurs": valeurs, **evaluer(propositions, 2, reference)})
    return sorties


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--question", help="identifiant de la question, par exemple C02")
    parser.add_argument("--toutes", action="store_true", help="les vingt questions du lot 2")
    parser.add_argument("--panel", help="membres fournisseur:modèle séparés par des virgules")
    parser.add_argument("--k", type=int, default=2, help="seuil de voix (majorité stricte)")
    parser.add_argument("--lot", type=int, default=2, choices=[1, 2])
    parser.add_argument("--traces", type=Path, default=TRACES)
    parser.add_argument("--references", type=Path, help="votre reference-i3.csv rempli")
    parser.add_argument("--sortie", type=Path, help="CSV des décisions (avec --toutes)")
    args = parser.parse_args()
    try:
        if not args.question and not args.toutes:
            for sortie in exemples_synthetiques():
                print(json.dumps(sortie, ensure_ascii=False))
            return 0
        panel = [m.strip() for m in (args.panel.split(",") if args.panel else PANEL_DEFAUT) if m.strip()]
        traces = lire_traces(args.traces)
        connus = {f"{t['provider']}:{t['model_requested']}" for t in traces if t["lot"] == args.lot}
        inconnus = [m for m in panel if m not in connus]
        if inconnus:
            raise ValueError(f"membres absents des traces du lot {args.lot} : {inconnus}")
        references = lire_references(args.references)
        questions = QUESTIONS if args.toutes else [args.question]
        if args.lot == 1:
            questions = [q for q in questions if q in {t["case_id"] for t in traces if t["lot"] == 1}]
        decisions = []
        for question in questions:
            resultat = evaluer(propositions_pour(traces, question, args.lot, panel), args.k, references.get(question))
            decisions.append({"question": question, "lot": args.lot, "n": len(panel), "k": args.k, **resultat})
        for d in decisions:
            print(json.dumps(d, ensure_ascii=False))
        if args.toutes:
            bilan = Counter(d["issue"] for d in decisions)
            print(json.dumps({"panel": panel, "k": args.k, "questions": len(decisions),
                              "issues": dict(sorted(bilan.items()))}, ensure_ascii=False))
        if args.sortie:
            with args.sortie.open("w", encoding="utf-8", newline="") as flux:
                ecrivain = csv.writer(flux, lineterminator="\n")
                ecrivain.writerow(["question", "lot", "panel", "n", "k", "consensus", "valeur", "voix",
                                   "modeles_d_accord", "reference", "issue", "suite"])
                for d in decisions:
                    ecrivain.writerow([d["question"], d["lot"], " ".join(panel), d["n"], d["k"],
                                       "oui" if d["decision"]["consensus"] else "non",
                                       "" if d["decision"]["valeur"] is None else d["decision"]["valeur"],
                                       d["decision"]["voix"], " ".join(d["decision"]["modeles"]),
                                       "" if d["reference"] is None else d["reference"], d["issue"], d["suite"]])
    except ValueError as erreur:
        print(str(erreur), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
