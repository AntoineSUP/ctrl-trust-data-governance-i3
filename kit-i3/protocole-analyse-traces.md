# Protocole : auditer un assistant à partir de ses traces

Supports réalisés avec assistance IA (Claude et Codex).

Module I3-APP Data Governance & IA responsable. Ce protocole fixe le contenu de la base, des questions et des traces, et la manière de les analyser. Il vaut pour les trois séances de projet ; l'énoncé de chaque séance indique la partie travaillée.

## 1. L'assistant étudié

Une boutique fictive envisage de confier à un assistant les questions de chiffre d'affaires de ses équipes. L'assistant reçoit le schéma de la base, des conventions de calcul et une question ; un modèle de langage rédige une requête SQLite ; la requête s'exécute en lecture seule sur la base ; la valeur obtenue devient la réponse.

Le 25/09/2026, un pilote a soumis les questions de ce kit à des modèles gratuits chez deux fournisseurs, Groq (plan gratuit) et OpenRouter (routes gratuites), depuis un seul compte et une requête à la fois. Chaque réponse a été enregistrée dans une trace. Vous n'appelez aucun modèle : vous analysez ces traces, vous les rejouez sur la base et vous en tirez une décision de gouvernance.

## 2. La base et les conventions

La base `data/boutique.sqlite` contient trois tables : 5 produits, 59 clients dont 9 sans commande, 221 commandes réparties sur 397 lignes, de janvier à septembre 2026. Les mêmes données figurent dans les trois CSV du dossier `data/`.

```sql
CREATE TABLE product (
    product_id TEXT PRIMARY KEY,
    price INTEGER NOT NULL CHECK (price >= 0)          -- centimes d'euro, hors taxes
);
CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    insert_date TEXT NOT NULL,                          -- UTC 'YYYY-MM-DD HH:MM:SS'
    birth_date TEXT NOT NULL                            -- 'YYYY-MM-DD'
);
CREATE TABLE orders (                                   -- une ligne par ligne de commande
    date TEXT NOT NULL,                                 -- UTC 'YYYY-MM-DD HH:MM:SS'
    order_id TEXT NOT NULL,
    customer_id TEXT NOT NULL REFERENCES customers(customer_id),
    product_id TEXT NOT NULL REFERENCES product(product_id),
    quantity_product INTEGER NOT NULL CHECK (quantity_product > 0),
    PRIMARY KEY (order_id, product_id)
);
```

La base ne contient que des ventes réalisées : ni retour, ni remise, ni frais. Les identifiants de colonnes restent en anglais : ce sont ceux que l'assistant a reçus.

Conventions de calcul, contraignantes pour l'assistant comme pour vos références :

1. `product.price` est le prix unitaire en centimes d'euro hors taxes, un entier. Le chiffre d'affaires hors taxes vaut `SUM(quantity_product * price)`, un nombre entier de centimes.
2. `orders` contient des lignes de commande, une ligne par couple (`order_id`, `product_id`). Toutes les lignes d'une commande ont le même client et la même date.
3. `orders.date` et `customers.insert_date` sont des horodatages UTC stockés en texte `YYYY-MM-DD HH:MM:SS` ; `customers.birth_date` est une date en texte `YYYY-MM-DD`. On les compare comme du texte ou avec les fonctions de date de SQLite.
4. Une période « du S au E » est fermée à gauche et ouverte à droite : `date >= S AND date < E`.
5. L'âge d'un client un jour D est son âge révolu : né le B, il a N ans le jour D quand son N-ième anniversaire tombe au plus tard le jour D et son (N+1)-ième après D. « Exactement 25 ans » signifie un âge révolu de 25 ans ce jour-là, calculé sur le mois et le jour, jamais sur la seule différence des années.
6. Sauf mention « au moment de la commande », l'âge se calcule à la date de référence écrite dans la question.
7. La requête rend une ligne et une colonne nommée `revenue_cents` ; elle rend 0, et non NULL, quand aucune ligne ne correspond.

L'assistant a reçu ces conventions en anglais, avec le schéma et la question : texte exact en section 7.

## 3. Les traces

`traces/traces-pilote-2026-09-25.jsonl` et sa copie `traces/traces-pilote-2026-09-25.csv` contiennent 352 traces : une par couple modèle et question, dans son dernier état. Elles sont toutes datées du 25/09/2026.

| Lot | Contenu | Traces | Horaire UTC (heure de Paris) |
|---|---|---:|---|
| 1 | 24 modèles sur les trois questions C01, C02 et C03 | 72 | 12:50:20 à 13:13:07 (14:50 à 15:13) |
| 2 | 14 modèles retenus après le lot 1, sur les vingt questions | 280 | 13:15:52 à 14:15:27 (15:15 à 16:15) |

Champs d'une trace :

| Champ | Contenu |
|---|---|
| `cell_id` | Identifiant stable `L<lot>:<fournisseur>:<modèle>:<question>`. |
| `lot`, `date_utc` | Lot et date du dernier essai, en temps universel. |
| `provider`, `model_requested`, `model_returned`, `upstream_provider` | Fournisseur, modèle demandé, modèle déclaré dans la réponse, hébergeur amont s'il est indiqué. |
| `family_model` | Famille du modèle : deux accès à la même famille ne sont pas deux voix indépendantes. |
| `case_id`, `family`, `question` | Question posée, sa famille telle que notée le 25/09/2026 et son texte envoyé. Les familles à jour sont dans `questions-i3.json`. |
| `prompt_sha256`, `prompt_chars` | Empreinte et longueur du message envoyé : identiques pour tous les modèles d'une même question. |
| `params` | Température, plafond de tokens de sortie et réglage du raisonnement. |
| `sql`, `sql_source` | Requête rendue par le modèle ; `fenced` quand elle était dans un bloc de code. |
| `statut_execution`, `detail_execution` | Issue technique de l'appel, tableau ci-dessous. |
| `value` | Valeur obtenue en exécutant la requête sur `data/boutique.sqlite` le 25/09/2026. Vide si rien n'a été exécuté ou si le résultat est NULL. |
| `http_status`, `error`, `finish_reason` | Code HTTP, message d'erreur, raison de fin de génération. |
| `latency_ms` | Durée de l'appel en millisecondes. |
| `tokens_prompt`, `tokens_completion`, `tokens_reasoning`, `tokens_total`, `reasoning_present` | Comptes de tokens déclarés par le fournisseur. Vide signifie non mesuré, jamais zéro. |
| `cost_native`, `cost_free_assumed` | Coût renvoyé par le fournisseur, en dollars, et gratuité supposée de la route. |
| `attempts` | Nombre d'essais de la cellule, reprise comprise : deux au plus. |
| `ratelimit` | En-têtes de limitation de débit de la dernière réponse. |
| `nature` | `historique` : appel réel conservé. Vos rejeux portent la nature `rejeu`, les exemples inventés la nature `simulation`. |

Statuts d'exécution :

| `statut_execution` | Sens |
|---|---|
| `valeur_obtenue` | La requête a été exécutée et a rendu un nombre. |
| `resultat_nul` | La requête a été exécutée et a rendu NULL. |
| `sql_invalide` | Aucune requête exploitable : erreur de syntaxe, ou génération interrompue avant toute requête. |
| `erreur_acces` | Refus du fournisseur : HTTP 400, 403 ou 404. |
| `quota_sature` | Limite de débit (HTTP 429) maintenue après deux essais. |
| `erreur_fournisseur` | Réponse HTTP 200 portant une erreur de l'hébergeur amont. |

Les traces ne contiennent ni la valeur juste ni de verdict. `value` est ce que l'assistant a produit, juste ou faux. Le verdict naît de la comparaison avec votre référence indépendante.

## 4. La référence indépendante

La référence d'une question est le montant obtenu par exécution d'une requête sur la base, puis contrôlé par un autre membre de l'équipe avec une méthode différente. Elle ne vient jamais d'une réponse de l'assistant ni d'un outil d'IA générative.

1. Répartir les vingt questions de `questions-i3.md` entre les membres.
2. Pour chaque question, écrire un `SELECT` SQLite qui rend une ligne et une colonne `revenue_cents`, puis l'exécuter : `python3 executer-requete.py "SELECT ..."`, la ligne de commande `sqlite3` ou un script Python.
3. Faire contrôler la valeur par un autre membre, avec une méthode indépendante : calcul sur les CSV, requête écrite séparément ou calcul à la main sur un sous-ensemble.
4. Consigner dans `reference-i3.csv` la requête (`sql`), la valeur (`revenue_cents`), le contrôleur (`controle_par`) et la méthode de contrôle (`methode_controle`).

Les conventions de la section 2 fixent le sens de chaque question. Une valeur qui dépend d'une autre convention est fausse au regard de cette référence. La séparation entre celui qui écrit et celui qui contrôle est la première règle de gouvernance du projet.

## 5. Rejouer et lire les traces

```bash
python3 analyse-traces.py resume
python3 analyse-traces.py rejouer --references reference-i3.csv --sortie rejeu-traces.csv
python3 analyse-traces.py accords --rejeu rejeu-traces.csv
python3 atelier-vote.py --toutes --references reference-i3.csv
```

`rejouer` réexécute chaque requête dans le bac à sable en lecture seule. Pour chaque trace, il note la valeur rejouée, son égalité avec la valeur de la trace et un verdict :

| Verdict | Sens |
|---|---|
| `juste` | Valeur égale à votre référence. |
| `faux` | Valeur différente, ou NULL. |
| `sql_invalide` | Requête absente, erronée, ou dont la forme n'est pas une ligne et une colonne `revenue_cents`. |
| `sql_refuse` | Requête refusée par le bac à sable : écriture, plusieurs instructions, table interdite, plafond dépassé. |
| `non_execute` | Aucune requête : refus d'accès, quota saturé, erreur du fournisseur. |
| `sans_reference` | Votre référence pour cette question est vide. |

Règles de lecture :

- Un taux s'écrit avec son effectif : « 18 justes sur 20 cas ». Un modèle non exécuté sur une question reste dans l'effectif et se compte à part.
- Un accès refusé n'est pas une réponse fausse ; une réponse fausse n'est pas une indisponibilité.
- Les natures ne se mélangent pas : une ligne `rejeu` garde la latence, les tokens et le coût mesurés le 25/09/2026, pas ceux de votre machine.
- Un accord entre modèles ne prouve pas l'exactitude : `accords` montre les valeurs partagées et les signale comme erronées quand elles diffèrent de votre référence.
- Le rejeu sur `data/variante-degradee/boutique-variante.sqlite` montre ce que la même requête rend sur des données dégradées. Une requête juste sur une base fausse donne un chiffre faux.

## 6. Ce que l'analyse alimente

| Production | Gabarit | Section du dossier de décision |
|---|---|---|
| Vingt références contrôlées | `reference-i3.csv` | Contrôles |
| Comparaison modèle par question | `gabarits/comparaison-modele-question.csv` | Contrôles |
| Synthèse par modèle et par famille | `gabarits/synthese-modeles.csv` | Contrôles, risques |
| Décisions de vote et accords erronés | `gabarits/tests-vote.csv` | Contrôles, incidents et escalade |
| Configurations comparées et coûts | `gabarits/comparaison-configurations.csv`, `gabarits/calcul-cout.csv` | Décision |
| Règles qualité et anomalies | `gabarits/regles-qualite.csv` | Données |

Le dossier complet et ses autres gabarits sont décrits dans `gabarits/README.md`.

## 7. Le message envoyé à l'assistant

Texte exact, en anglais, envoyé à chaque modèle le 25/09/2026. `{schema}` est le contenu de `schema.sql`, `{question}` le texte de la question. Le message système puis le message utilisateur forment l'empreinte `prompt_sha256` de la trace.

Message système :

```text
You write SQLite queries for a small e-commerce database. Reply with exactly one SQLite SELECT statement and nothing else: no explanation, no comments, no markdown other than an optional ```sql fence.
```

Gabarit du message utilisateur (empreinte SHA-256 du gabarit : `c9bb4f7c1548b11c16c4bcec222b694207495023ae93a74329e472a845bffbb1`) :

```text
Schema (SQLite):
{schema}

Conventions (binding):
- product.price is the unit price in euro cents, excluding VAT (an integer). Revenue excluding VAT is SUM(quantity_product * price), an integer number of cents.
- orders holds order lines: one row per (order_id, product_id). All lines of an order share the same customer_id and the same date.
- orders.date and customers.insert_date are UTC timestamps stored as text 'YYYY-MM-DD HH:MM:SS'. customers.birth_date is a date stored as text 'YYYY-MM-DD'. Compare them as text or with SQLite date functions.
- A period "from S to E" is closed on the left and open on the right: date >= S AND date < E.
- A customer's age on a day D is the number of completed years: someone born on B is N years old on D when the N-th anniversary of B is on or before D and the (N+1)-th anniversary is after D. "Exactly 25 years old" means completed age 25 on that day, computed from month and day, never from the year difference alone.
- Unless the question says "at the time of the order", ages are computed on the reference date given in the question.
- The query must return exactly one row and one column named revenue_cents. When no order line matches, return 0 (use COALESCE), not NULL.
- Use only the tables above. One SELECT statement, nothing else.

Question: {question}
```

## 8. Les vingt questions

Mêmes questions que `questions-i3.md`. Chaque paramètre est écrit dans la question : bornes de la période, date de référence de l'âge, liste de produits.

<!-- questions:debut -->
| # | Famille | Question | Texte envoyé à l'assistant |
|---|---|---|---|
| C01 | période | Quel est le chiffre d'affaires hors taxes, en centimes d'euro, des commandes passées du 2026-03-01 00:00:00 au 2026-06-01 00:00:00 ? | What is the revenue excluding VAT, in euro cents, of the orders placed from 2026-03-01 00:00:00 to 2026-06-01 00:00:00? |
| C02 | âge à une date de référence | Quel est le chiffre d'affaires total hors taxes, en centimes d'euro, réalisé par les clients âgés d'exactement 25 ans à la date de référence 2026-09-25 (toutes leurs commandes) ? | What is the total revenue excluding VAT, in euro cents, generated by customers who are exactly 25 years old on the reference date 2026-09-25 (all their orders)? |
| C03 | liste de produits | Quel est le chiffre d'affaires hors taxes, en centimes d'euro, des seuls produits a, b et c, pour les commandes passées du 2026-01-01 00:00:00 au 2026-07-01 00:00:00 ? | What is the revenue excluding VAT, in euro cents, of products a, b and c only, for orders placed from 2026-01-01 00:00:00 to 2026-07-01 00:00:00? |
| C04 | période | Quel est le chiffre d'affaires hors taxes, en centimes d'euro, des commandes passées du 2026-01-01 00:00:00 au 2026-10-01 00:00:00 ? | What is the total revenue excluding VAT, in euro cents, of the orders placed from 2026-01-01 00:00:00 to 2026-10-01 00:00:00? |
| C05 | période | Quel est le chiffre d'affaires hors taxes, en centimes d'euro, des commandes passées du 2026-06-01 00:00:00 au 2026-06-02 00:00:00 ? | What is the revenue excluding VAT, in euro cents, of the orders placed from 2026-06-01 00:00:00 to 2026-06-02 00:00:00? |
| C06 | période | Quel est le chiffre d'affaires hors taxes, en centimes d'euro, des commandes passées du 2025-01-01 00:00:00 au 2026-01-01 00:00:00 ? | What is the revenue excluding VAT, in euro cents, of the orders placed from 2025-01-01 00:00:00 to 2026-01-01 00:00:00? |
| C07 | période | Quel est le chiffre d'affaires hors taxes, en centimes d'euro, des commandes passées du 2026-05-31 00:00:00 au 2026-06-01 00:00:00 ? | What is the revenue excluding VAT, in euro cents, of the orders placed from 2026-05-31 00:00:00 to 2026-06-01 00:00:00? |
| C08 | âge à une date de référence | Quel est le chiffre d'affaires total hors taxes, en centimes d'euro, réalisé par les clients âgés d'exactement 25 ans à la date de référence 2026-09-24 (toutes leurs commandes) ? | What is the total revenue excluding VAT, in euro cents, generated by customers who are exactly 25 years old on the reference date 2026-09-24 (all their orders)? |
| C09 | âge à une date de référence | Quel est le chiffre d'affaires total hors taxes, en centimes d'euro, réalisé par les clients âgés d'exactement 25 ans à la date de référence 2026-09-26 (toutes leurs commandes) ? | What is the total revenue excluding VAT, in euro cents, generated by customers who are exactly 25 years old on the reference date 2026-09-26 (all their orders)? |
| C10 | âge au moment de la commande | Quel est le chiffre d'affaires total hors taxes, en centimes d'euro, des commandes passées par des clients âgés d'exactement 25 ans au moment de la commande ? | What is the total revenue excluding VAT, in euro cents, of the orders placed by customers who were exactly 25 years old at the time of the order? |
| C11 | âge à une date de référence | Quel est le chiffre d'affaires total hors taxes, en centimes d'euro, réalisé par les clients âgés d'exactement 25 ans à la date de référence 2026-12-01 (toutes leurs commandes) ? | What is the total revenue excluding VAT, in euro cents, generated by customers who are exactly 25 years old on the reference date 2026-12-01 (all their orders)? |
| C12 | liste de produits | Quel est le chiffre d'affaires total hors taxes, en centimes d'euro, des seuls produits a, b et c, sur l'ensemble des commandes ? | What is the total revenue excluding VAT, in euro cents, of products a, b and c only, over all orders? |
| C13 | liste de produits | Quel est le chiffre d'affaires hors taxes, en centimes d'euro, des seuls produits a et c, pour les commandes passées du 2026-04-01 00:00:00 au 2026-05-01 00:00:00 ? | What is the revenue excluding VAT, in euro cents, of products a and c only, for orders placed from 2026-04-01 00:00:00 to 2026-05-01 00:00:00? |
| C14 | liste de produits | Quel est le chiffre d'affaires hors taxes, en centimes d'euro, des seuls produits a, b et c, pour les commandes passées du 2026-10-01 00:00:00 au 2026-12-01 00:00:00 ? | What is the revenue excluding VAT, in euro cents, of products a, b and c only, for orders placed from 2026-10-01 00:00:00 to 2026-12-01 00:00:00? |
| C15 | période + âge à une date de référence | Quel est le chiffre d'affaires hors taxes, en centimes d'euro, des commandes passées du 2026-03-01 00:00:00 au 2026-06-01 00:00:00 par des clients âgés d'exactement 25 ans à la date de référence 2026-09-25 ? | What is the revenue excluding VAT, in euro cents, of the orders placed from 2026-03-01 00:00:00 to 2026-06-01 00:00:00 by customers who are exactly 25 years old on the reference date 2026-09-25? |
| C16 | âge à une date de référence + liste de produits | Quel est le chiffre d'affaires total hors taxes, en centimes d'euro, des seuls produits a, b et c, réalisé par les clients âgés d'exactement 25 ans à la date de référence 2026-09-25 ? | What is the total revenue excluding VAT, in euro cents, of products a, b and c only, generated by customers who are exactly 25 years old on the reference date 2026-09-25? |
| C17 | période + âge à une date de référence + liste de produits | Quel est le chiffre d'affaires hors taxes, en centimes d'euro, des seuls produits a, b et c, pour les commandes passées du 2026-01-01 00:00:00 au 2026-07-01 00:00:00 par des clients âgés d'exactement 25 ans à la date de référence 2026-09-25 ? | What is the revenue excluding VAT, in euro cents, of products a, b and c only, for orders placed from 2026-01-01 00:00:00 to 2026-07-01 00:00:00 by customers who are exactly 25 years old on the reference date 2026-09-25? |
| C18 | période + âge au moment de la commande | Quel est le chiffre d'affaires hors taxes, en centimes d'euro, des commandes passées du 2026-05-01 00:00:00 au 2026-06-01 00:00:00 par des clients âgés d'exactement 25 ans au moment de la commande ? | What is the revenue excluding VAT, in euro cents, of the orders placed from 2026-05-01 00:00:00 to 2026-06-01 00:00:00 by customers who were exactly 25 years old at the time of the order? |
| C19 | période + âge à une date de référence + liste de produits | Quel est le chiffre d'affaires hors taxes, en centimes d'euro, du seul produit d, pour les commandes passées du 2026-09-01 00:00:00 au 2026-10-01 00:00:00 par des clients âgés d'exactement 25 ans à la date de référence 2026-09-25 ? | What is the revenue excluding VAT, in euro cents, of product d only, for orders placed from 2026-09-01 00:00:00 to 2026-10-01 00:00:00 by customers who are exactly 25 years old on the reference date 2026-09-25? |
| C20 | période | Quel est le chiffre d'affaires hors taxes, en centimes d'euro, des commandes passées du 2026-06-01 00:00:00 au 2026-09-01 00:00:00 ? | What is the revenue excluding VAT, in euro cents, of the orders placed from 2026-06-01 00:00:00 to 2026-09-01 00:00:00? |
<!-- questions:fin -->

Familles : `période` est un chiffre d'affaires entre deux horodatages ; `âge à une date de référence` retient les clients âgés d'exactement 25 ans à la date écrite dans la question ; `âge au moment de la commande` retient les lignes passées quand le client avait exactement 25 ans ; `liste de produits` limite le chiffre d'affaires aux produits nommés. Un `+` combine les filtres.

## Annexe : règles du parcours

Le parcours se réalise hors ligne : aucun appel de modèle, aucun compte personnel, aucune donnée personnelle réelle. Tout usage d'un outil d'IA générative suit les règles du module et se déclare avec `gabarits/declaration-ia.md` ; les outils autorisés et le canal de remise sont confirmés par l'école.
