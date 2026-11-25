#!/usr/bin/env python3
"""Règle de routage et d'escalade : décisions sur sept scénarios synthétiques, sans réseau.

Ressources fictives, aucun appel, aucune clé. Les coûts sont des dollars hors taxes
par demande, pour une enveloppe de tokens fixe. Les niveaux de capacité 1 à 3
décrivent l'éligibilité dans cet exercice, pas la qualité générale d'un modèle. La
disponibilité est fournie par le scénario, jamais mesurée chez un fournisseur.

    python3 atelier-routage.py                          # les sept scénarios
    python3 atelier-routage.py --scenario différable    # un scénario

Chaque décision porte une action (exécuter, différer, s'abstenir), la ressource
retenue, la dépense, les contrôles exigés, la raison et la suite donnée. Écrire
d'abord votre propre règle dans `gabarits/politique-escalade.md`, puis comparer.
"""
import argparse
import json

RESSOURCES = [
    {"id": "petit-gratuit", "niveau": 1, "acces": "gratuit", "disponible": True,
     "depense": 0.0, "allocation": 0.0, "recharge_minutes": None},
    {"id": "expert-abonnement", "niveau": 3, "acces": "abonnement", "disponible": True,
     "depense": 0.0, "allocation": 0.04, "recharge_minutes": None},
    {"id": "expert-api", "niveau": 3, "acces": "tokens", "disponible": True,
     "depense": 0.30, "allocation": 0.30, "recharge_minutes": None},
]


def choisir(demande: dict, ressources: list) -> dict:
    """Règle déterministe, avec une raison que le demandeur peut lire et que la trace conserve.

    La capacité déjà payée passe avant toute nouvelle dépense. Une demande qui peut
    attendre attend la recharge d'une capacité incluse. Au réveil, la disponibilité
    se mesure de nouveau : l'heure de recharge ne prouve pas que la capacité est là.
    Une demande à impact élevé exige la vérification des sources et une revue humaine.
    """
    eligibles = [r for r in ressources if r["niveau"] >= demande["difficulte"]]
    controles = ("vérification des sources et revue humaine" if demande["impact_eleve"]
                 else "exécution en lecture seule et contrôle de la valeur")
    revue = "réponse soumise à une revue humaine avant usage" if demande["impact_eleve"] else "réponse utilisable après contrôle"
    incluses = [r for r in eligibles if r["disponible"] and r["depense"] == 0]
    if incluses:
        retenue = min(incluses, key=lambda r: (r["allocation"], r["niveau"], r["id"]))
        return {"action": "exécuter", "ressource": retenue["id"], "depense": 0, "controles": controles,
                "raison": "capacité incluse éligible", "suite": revue}
    en_attente = [r for r in eligibles if not r["disponible"] and r["depense"] == 0
                  and r["recharge_minutes"] is not None
                  and 0 < r["recharge_minutes"] <= demande["delai_minutes"]]
    if en_attente and demande["peut_attendre"]:
        retenue = min(en_attente, key=lambda r: r["recharge_minutes"])
        return {"action": "différer", "ressource": retenue["id"], "depense": 0, "controles": controles,
                "raison": "nouvelle mesure de disponibilité au réveil",
                "reveil_dans_minutes": retenue["recharge_minutes"],
                "suite": "demande conservée et reprise au réveil, demandeur informé du délai"}
    payantes = [r for r in eligibles if r["disponible"] and r["depense"] <= demande["budget"]]
    if payantes:
        retenue = min(payantes, key=lambda r: (r["depense"], r["allocation"], r["id"]))
        return {"action": "exécuter", "ressource": retenue["id"], "depense": retenue["depense"],
                "controles": controles, "raison": "route disponible dans le budget autorisé", "suite": revue}
    return {"action": "s'abstenir", "ressource": None, "depense": 0, "controles": controles,
            "raison": "aucune ressource éligible dans le délai et le budget",
            "suite": "escalade : la demande et sa raison sont transmises au responsable désigné"}


def scenarios() -> list:
    base = {"difficulte": 1, "impact_eleve": False, "peut_attendre": True, "delai_minutes": 120, "budget": 0.30}
    epuisees = [dict(r, disponible=False, recharge_minutes=60) if r["acces"] == "abonnement" else dict(r)
                for r in RESSOURCES]
    return [
        ("simple", base, RESSOURCES),
        ("complexe", {**base, "difficulte": 3}, RESSOURCES),
        ("différable", {**base, "difficulte": 3}, epuisees),
        ("urgent", {**base, "difficulte": 3, "peut_attendre": False, "delai_minutes": 5}, epuisees),
        ("budget épuisé", {**base, "difficulte": 3, "peut_attendre": False, "budget": 0}, epuisees),
        ("impact élevé", {**base, "difficulte": 3, "impact_eleve": True}, RESSOURCES),
        ("capacité inconnue", {**base, "difficulte": 4}, RESSOURCES),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scenario", help="n'afficher que le scénario nommé")
    args = parser.parse_args()
    trouve = False
    for nom, demande, ressources in scenarios():
        if args.scenario and nom != args.scenario:
            continue
        trouve = True
        print(json.dumps({"scenario": nom, "nature": "simulation", "demande": demande,
                          "decision": choisir(demande, ressources)}, ensure_ascii=False))
    if not trouve:
        parser.error("scénario inconnu")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
