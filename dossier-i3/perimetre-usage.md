# Périmètre d'usage de l'assistant

Supports réalisés avec assistance IA (Claude et Codex).

**Équipe :** Ctrl+Trust, BDML2 (Antoine, Jacky, Noé, Adem, Kaïs)
**Version :** v1
**Date :** 2026-11-25
**Rédigé par :** Antoine (responsable de gouvernance)
**Contrôlé par :** Kaïs (porte-parole de la décision)

**Phrase de périmètre.** L'assistant IA aide le contrôleur de gestion à produire, chaque lundi, le tableau de bord interne du chiffre d'affaires HT de la semaine écoulée, par période et par produit, afin de décider s'il convient de signaler une baisse d'activité à la direction. Une erreur pourrait masquer une baisse réelle ou provoquer une fausse alerte, mais reste corrigeable lors du tableau de bord suivant. Pour limiter ce risque, la période et la définition du chiffre sont affichées, les résultats sont comparés à ceux de la semaine précédente et le directeur financier effectue une relecture hebdomadaire avant leur transmission à la direction.

## 1. Usage visé

| Élément | Réponse | Preuve ou hypothèse |
|---|---|---|
| Utilisateurs autorisés (fonctions) | Le contrôleur de gestion (DAF) ; relecture par le directeur financier | Page « Qui fait quoi dans la boutique » |
| Questions admises (familles et exemples) | Chiffre d'affaires HT par période (C01, C04, C05, C06, C07, C20) et par liste de produits (C03, C12, C13, C14) | Énoncé de l'encadrement 1, étape 1 ; limites-des-vingt-cas.md |
| Décisions que la réponse soutient | Décider s'il convient de signaler une baisse d'activité à la direction | Hypothèse : le tableau de bord suit l'évolution du CA HT et sert à signaler les baisses d'activité |
| Décisions exclues | TVA, chiffres envoyés à la banque, commissions des partenaires, prime d'un vendeur salarié, marge par produit, prix et commandes de stock | Cours 1, diapositives 17 et 35 |
| Données mobilisées (tables et colonnes) | orders : date, product_id, quantity_product ; product : price | schema.sql |
| Données exclues | Table customers (identifiant client, date d'inscription, date de naissance) | Minimisation : inutile au calcul du CA HT |
| Moment d'usage (fréquence, délai attendu) | Chaque lundi, pour la semaine écoulée | Hypothèse : du lundi 00:00:00 UTC inclus au lundi suivant 00:00:00 UTC exclu |

## 2. Conséquences d'une réponse erronée

| Usage | Conséquence d'une erreur | Personnes exposées | Gravité (1 à 3) | Contrôle exigé avant usage |
|---|---|---|---:|---|
| Tableau de bord interne | Une baisse réelle passe inaperçue ou une fausse alerte remonte à la direction. Erreur corrigeable au tableau de bord suivant. | Contrôleur de gestion et direction | 1 | Affichage de la période et de la définition du CA HT, comparaison à la semaine précédente et relecture par le directeur financier. |
| Chiffre communiqué à l'extérieur (TVA, banque) | Redressement fiscal, intérêts de retard et majorations. Une erreur de 2 % sur un mois représente environ 13 000 € de TVA mal déclarée. Risque de rupture du prêt de 5 M€ et de remboursement immédiat. | Entreprise, DAF, administration fiscale et banque | 3 | Calcul effectué par la comptabilité ; l'assistant sert uniquement au recoupement. Usage interdit dans le périmètre actuel. |
| Montant qui engage une personne (commissions, primes) | Rémunération incorrecte, préjudice financier et contestation. Le calcul est impossible avec la base actuelle, car orders ne contient aucune colonne vendeur. | Salariés, partenaires et entreprise | 3 | Référence indépendante avant chaque paiement. Usage interdit dans le périmètre actuel. |
| Autre usage : prix et stock | Une erreur sur les ventes entraîne une mauvaise décision de commande, pouvant provoquer des stocks invendus ou des ruptures. | Équipe commerciale, entreprise et clients | 2 | Comparaison avec les ventes du mois précédent avant toute commande. Usage hors périmètre actuel. |

Échelle de gravité retenue : 1 = faible et réversible ; 2 = conséquence opérationnelle ou commerciale significative ; 3 = conséquence financière, réglementaire ou individuelle importante.

## 3. Critères de réussite

_Reportée à l'encadrement 2._

| Critère | Seuil retenu | Effectif sur lequel il est mesuré | Source dans le kit |
|---|---|---|---|
| | | | |

## 4. Exclusions et limites assumées

| Exclusion ou limite | Raison | Condition pour la lever |
|---|---|---|
| Données personnelles des clients (customers) | Inutiles au calcul du CA HT ; principe de minimisation des données | Besoin métier justifié et analyse RGPD |
| Marge par produit | Absence de coûts d'achat dans la base et de questions de test dédiées | Intégration des coûts d'achat et validation de nouveaux tests |
| Prime d'un vendeur salarié | Usage non testé ayant des conséquences individuelles sur la rémunération | Analyse RGPD, gestion des droits d'accès et validation de tests dédiés |
| Commissions des partenaires | Usage non testé pouvant entraîner des conséquences financières | Intégration des règles contractuelles et validation de tests dédiés |
| Usages fiscaux, comptables, déclaratifs ou bancaires | Conséquences financières et réglementaires plus importantes en cas d'erreur | Validation métier spécifique, contrôles renforcés et nouveaux tests |

**Plan de repli.** En cas d'absence de réponse de l'assistant ou d'incohérence du résultat, le contrôleur de gestion recalcule le chiffre d'affaires HT indépendamment de l'assistant.

**Escalade (proposition, à reprendre à l'étape 5).** Dès qu'une absence de réponse ou un écart non expliqué est constaté, le contrôleur de gestion prévient le directeur financier le lundi matin, avant toute diffusion du tableau de bord. Le directeur financier décide de valider, de suspendre ou de reporter la transmission. Délai et seuil : hypothèses à valider en équipe.

## 5. Hypothèses et questions ouvertes

_Reportée à l'encadrement 2._

| Hypothèse ou question | Effet si elle est fausse | Qui la lève | Échéance |
|---|---|---|---|
| | | | |
