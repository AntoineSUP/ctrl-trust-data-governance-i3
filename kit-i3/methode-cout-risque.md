# Méthode coût et risque, étape par étape

Supports réalisés avec assistance IA (Claude et Codex).

Les appels du 25/09/2026 ont utilisé des routes gratuites. Une décision de mise en service compare pourtant des configurations qui n'ont pas le même coût ni le même risque : un modèle seul, un vote, un vote suivi d'une revue humaine. Cette méthode chiffre une configuration à partir des traces, puis met ce coût en regard de ce que coûte une erreur.

Note de lecture : les montants sont hors taxes. Les prix par million de tokens sont en dollars, comme dans les sources des fournisseurs ; un coût horaire de revue humaine est en euros et ne s'additionne jamais à un montant en dollars.

## Les trois grandeurs, jamais additionnées

| Grandeur | Ce qu'elle mesure | D'où elle vient |
|---|---|---|
| Dépense réelle | Ce qui a été payé pour les appels | Coût natif renvoyé par le fournisseur, s'il existe ; sinon preuve datée du plan et de la route, distincte du champ brut |
| Coût équivalent API | Ce que la même consommation coûterait sur une route facturée au token | Les tokens de la trace multipliés par un prix daté |
| Coût imputé à un abonnement | La part du forfait consommée par l'appel | Le prix du forfait rapporté à la consommation de la période |

Ces trois colonnes restent séparées dans toutes vos tables. Un total ne porte que sur une seule d'entre elles.

## Étape 1 - Relever les tokens dans la trace

Pour l'appel choisi, lire dans `traces/traces-pilote-2026-09-25.csv` : `model_requested`, `tokens_prompt`, `tokens_completion`, `tokens_reasoning`, `cost_native`, `cost_free_assumed`, `latency_ms`, `attempts`, `date_utc`.

Compter les tokens de sortie une seule fois. Quand le fournisseur inclut le raisonnement dans `tokens_completion`, `tokens_reasoning` est une information : ne pas l'ajouter. Quand il le compte à part, l'ajouter aux tokens de sortie. La documentation du fournisseur tranche ce point.

Un compteur vide reste vide. Écrire N/D, jamais zéro : zéro est une mesure, l'absence de mesure n'en est pas une. Dans les traces, `cost_native` vaut 0 sur une partie des appels OpenRouter et reste vide sur tous les appels Groq.

## Étape 2 - Choisir un prix de référence daté

Pour le calcul hors ligne, utiliser les hypothèses pédagogiques suivantes : entrée à 0,15 USD HT par million de tokens et sortie à 0,60 USD HT par million. Ce sont des prix fictifs de calcul, sans engagement d'un fournisseur ni attribution à un modèle. Le portefeuille joint conserve séparément les prix historiques relevés le 28/09/2026, avec leur provenance.

Pour une décision réelle, documenter le prix du modèle exact, sa route, sa devise et sa date sur la source officielle du fournisseur. Une famille commune ne suffit pas à identifier un modèle. Un prix inconnu reste N/D.

## Étape 3 - Calculer un appel

```
équivalent API en USD HT = (tokens_entrée x prix_entrée + tokens_sortie x prix_sortie) / 1 000 000
```

**Exemple fictif**, sans rapport avec une question du kit : modèle de démonstration, 2 000 tokens d'entrée et 300 de sortie, `cost_native` vide.

| Grandeur | Valeur et preuve |
|---|---|
| Coût natif dans la trace | Vide : aucune mesure fournie |
| Dépense réelle | 0 USD HT si le plan gratuit du compte est établi par une preuve datée ; N/D sinon |
| Équivalent API | (2 000 x 0,15 + 300 x 0,60) / 1 000 000 = **0,00048 USD HT**, hypothèses pédagogiques ci-dessus |

Ce calcul suppose du texte simple, sans cache de contexte ni outil facturé à part. Si une trace porte l'une de ces catégories, l'écrire comme hypothèse sous la table.

## Étape 4 - Calculer une configuration

Additionner **tous les appels effectués**, reprises comprises, lorsqu'ils sont mesurés. Ici, `attempts` compte les essais d'une cellule mais seuls les compteurs du dernier état sont fournis. Pour une cellule à plusieurs essais, le coût total reste N/D ; calculer seulement le coût de l'essai documenté. Multiplier ses tokens par `attempts` fabriquerait une mesure. Un vote compte chaque modèle consulté. Une revue humaine compte le temps passé sur chaque demande revue.

| Configuration | Cas traités | Justes / abstentions / erreurs | Appels et reprises | Tokens entrée / sortie | Équivalent API (USD HT) | Revues humaines | Temps de revue |
|---|---:|---|---:|---|---:|---:|---|
| Modèle seul | | | | | | | |
| Vote 2 sur 3 | | | | | | | |
| Vote 2 sur 3 et revue des abstentions | | | | | | | |
| Votre configuration | | | | | | | |

Diviser ensuite l'équivalent par le nombre de demandes traitées pour obtenir un coût par demande. Indiquer à côté les abstentions et les erreurs : une configuration moins chère qui s'abstient souvent ne rend pas le même service.

Une ligne de rejeu conserve les compteurs de l'appel d'origine : elle n'est pas une nouvelle consommation. Si une configuration n'est que partiellement chiffrable, son total est N/D ; indiquer les appels chiffrables sur le total et nommer le sous-total connu.

## Étape 5 - Mettre en regard le coût d'une erreur

Le coût d'un contrôle se compare à ce que coûte l'erreur qu'il évite. Pour chaque usage du périmètre, écrire :

```
erreurs attendues par an = demandes par an x part de réponses fausses acceptées sans contrôle
coût annuel des erreurs  = erreurs attendues par an x coût d'une erreur pour cet usage
coût annuel du contrôle  = demandes contrôlées par an x temps par contrôle x coût horaire
```

La part de réponses fausses vient de votre rejeu, avec son effectif et sa famille de questions ; vingt cas ne donnent qu'un ordre de grandeur, à écrire comme hypothèse. Le coût d'une erreur dépend de l'usage : il est faible pour un tableau de bord relu chaque semaine, élevé pour un chiffre communiqué à l'extérieur ou un montant qui engage une personne. Écrire chaque valeur retenue comme hypothèse, avec sa source ou son auteur.

**Exemple fictif.** 48 000 demandes par an ; hypothèse de 2 réponses fausses acceptées pour 100 demandes ; hypothèse d'un coût de 50 € HT par erreur pour l'usage considéré : 960 erreurs et 48 000 € HT par an. Une revue de 3 minutes à 45 € HT de l'heure, sur 10 % des demandes, coûte 10 800 € HT par an ; elle se justifie si elle évite une part suffisante de ces erreurs. Ces chiffres sont inventés : ils montrent le raisonnement, pas le cas de la boutique.

## Étape 6 - Passer à l'échelle de l'entreprise

Poser le volume annuel, puis multiplier par le coût par demande :

```
20 personnes x 10 demandes par jour x 20 jours ouvrés x 12 mois = 48 000 demandes par an
```

| Coût moyen par demande | Facture annuelle |
|---|---:|
| 0,03 USD HT | 1 440 USD HT |
| 3 USD HT | 144 000 USD HT |
| 30 USD HT | 1 440 000 USD HT |

L'écart entre ces trois lignes ne vient pas du volume, identique, mais du modèle et de la configuration retenus pour chaque demande.

## Ce que cette méthode ne donne pas

Elle ne donne pas la facture d'un fournisseur : la facturation réelle ajoute le cache de contexte, les outils, les remises de volume et les majorations de contexte long. Elle ne donne pas un taux d'erreur général : cela demande des questions répétées et un échantillon représentatif des demandes réelles. Elle ne chiffre que le temps de revue humaine que vous déclarez ; le temps de traitement d'un incident, de mise à jour des références et de suivi des fournisseurs reste à estimer à part.

## Annexe - Erreurs de calcul fréquentes

- Un coût affiché à zéro alors que le tarif n'a pas été renseigné : la colonne reste vide, elle ne vaut pas zéro.
- Des tokens de raisonnement ajoutés à des tokens de sortie qui les contenaient déjà.
- Un équivalent API présenté comme une dépense.
- Un prix sans date, que plus personne ne peut vérifier.
- Un montant en dollars additionné à un montant en euros.
