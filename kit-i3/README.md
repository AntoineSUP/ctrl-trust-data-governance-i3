# Kit du projet I3 : gouverner un assistant de données

Supports réalisés avec assistance IA (Claude et Codex).

Module I3-APP Data Governance & IA responsable, EFREI, apprentis BDML1 et BDML2. Kit du 19/10/2026, version `i3-kit-2026-10-19`.

Le kit contient le cas étudié pendant les trois séances de projet : une base de données fictive, vingt questions de chiffre d'affaires, les traces historiques d'un assistant qui a répondu à ces questions le 25/09/2026, des outils d'analyse et les gabarits du dossier de décision. Tout fonctionne hors ligne, avec Python 3.10 ou plus récent et sa seule bibliothèque standard : aucun compte, aucune clé, aucune connexion réseau.

## Avant le premier encadrement

Compter 35 minutes. Sous Windows, écrire `python` au lieu de `python3` dans toutes les commandes.

| Pas | Geste | Résultat attendu | Temps |
|---|---|---|---|
| 1 | Extraire l'archive dans un dossier vide, puis ouvrir le dossier `kit-i3`. | Le dossier contient `data`, `traces`, `gabarits` et les scripts listés plus bas. | 5 min |
| 2 | Vérifier Python : `python3 --version`. | Python 3.10 ou plus récent. | 5 min |
| 3 | Contrôler le kit : `python3 verifier-kit.py`. | La dernière ligne du résultat porte `"ok": true`. | 2 min |
| 4 | Lire les sections 1 à 4 de `protocole-analyse-traces.md`. | Vous savez ce que contient une trace et ce qu'est une référence indépendante. | 20 min |
| 5 | Afficher l'inventaire des traces : `python3 analyse-traces.py resume`. | Le nombre de traces, de modèles et de statuts s'affiche. | 3 min |

Si le contrôle du pas 3 échoue, extraire de nouveau l'archive dans un dossier vide : un fichier modifié ou incomplet change son empreinte. Si Python manque, l'installer depuis le site officiel de Python ou le gestionnaire de logiciels de votre poste, puis recommencer au pas 2.

## Le cas

| Fichier | Rôle |
|---|---|
| `data/boutique.sqlite` | La base de la boutique fictive : 5 produits, 59 clients, 221 commandes sur 397 lignes. Ne jamais la modifier. |
| `data/product.csv`, `data/customers.csv`, `data/orders.csv` | Les mêmes données en CSV, pour un tableur ou un contrôle à la main. |
| `data/manifest.json` | Empreintes SHA-256 de la base et des CSV, effectifs et contrôles d'intégrité de la base. |
| `schema.sql` | Les trois tables, telles qu'elles ont été envoyées à l'assistant. |
| `data/variante-degradee/boutique-variante.sqlite` | Une seconde extraction fictive de la même boutique, qui contient des anomalies à détecter. |
| `data/variante-degradee/product.csv`, `customers.csv`, `orders.csv` | Les mêmes données dégradées en CSV. |
| `data/variante-degradee/manifest.json` | Description de la variante, empreintes et effectifs. |
| `questions-i3.md`, `questions-i3.json` | Les vingt questions, en français, avec le texte exact envoyé à l'assistant. |
| `reference-i3.csv` | Gabarit de vos vingt références : requête, valeur, contrôleur et méthode de contrôle. |

## Les traces

| Fichier | Rôle |
|---|---|
| `traces/traces-pilote-2026-09-25.jsonl` | 352 traces historiques de l'assistant, une par couple modèle et question, appels réels du 25/09/2026. |
| `traces/traces-pilote-2026-09-25.csv` | Les mêmes traces en CSV, pour un tableur. |

## Les outils hors ligne

| Fichier | Rôle |
|---|---|
| `verifier-kit.py` | Contrôle les empreintes de tous les fichiers du kit, l'intégrité de la base et l'absence de champs de correction dans les traces. |
| `executer-requete.py` | Exécute une requête `SELECT` en lecture seule sur une base du kit et affiche le résultat. |
| `analyse-traces.py` | Rejoue le SQL des traces sur une base, compare à vos références, compte les résultats par modèle et par famille, liste les accords entre modèles. |
| `atelier-vote.py` | Vote k sur n sur des exemples synthétiques ou sur les traces d'une question. |
| `atelier-routage.py` | Décisions d'une règle de routage et d'escalade sur sept scénarios synthétiques. |
| `controle-qualite.py` | Exécute vos règles qualité sur la base et sur la variante dégradée. |
| `sandbox_sqlite.py` | Bac à sable SQLite en lecture seule utilisé par les outils : une instruction, `SELECT` sur les trois tables, dix lignes au plus. |

## Les lectures

| Fichier | Rôle |
|---|---|
| `protocole-analyse-traces.md` | La base, les conventions, le contenu des traces, la référence indépendante, le rejeu, le message envoyé à l'assistant et les vingt questions. |
| `limites-des-vingt-cas.md` | Ce que les vingt cas mesurent, ce qu'ils ne mesurent pas, et les conséquences pour une décision de mise en service. |
| `situations-fictives.md` | Huit situations de gouvernance : biais, droits d'accès, conservation, décision touchant des salariés, données envoyées à un fournisseur, incident, dépendance, qualité. |
| `sources-officielles.md` | Repères juridiques et techniques vérifiés le 19/10/2026, lisibles hors ligne. |
| `methode-cout-risque.md` | La méthode pour chiffrer un appel, une configuration et le coût d'une erreur, sur les traces. |
| `portefeuille-modeles.md`, `portefeuille-modeles-2026-09-28.csv` | Soixante couples modèle et accès relevés le 28/09/2026 : groupes de capacité, voies d'accès, prix datés. |

## Les gabarits du dossier

Le dossier `gabarits/` contient les formulaires du dossier de décision : périmètre d'usage, responsabilités, dictionnaire de données, règles qualité, cycle de vie, registre des risques, politique d'escalade, fiche incident, fiche de décision, comparaisons et synthèses, tests de vote, coûts, contributions, journal des décisions et déclaration d'usage de l'IA générative. Leur index est `gabarits/README.md`. Copier un gabarit dans votre dossier de travail avant de le remplir.

## Nature des contenus

| Nature | Contenus | Règle |
|---|---|---|
| Données synthétiques | Base, variante dégradée, exemples des ateliers, contextes des situations | Inventées : aucune personne réelle, aucune entreprise réelle. |
| Traces historiques | `traces/` | Dernier état de chaque cellule des appels du 25/09/2026 ; requêtes et mesures conservées, champs de correction retirés et statuts traduits. Une mesure absente reste vide ; on ne la complète jamais. |
| Propositions | Vos gabarits remplis, règles, décisions | Chaque élément s'appuie sur une preuve ou porte la mention « hypothèse ». |

## Inventaire

`manifest.json` donne l'empreinte SHA-256 de chaque fichier du kit et la source dont il provient. `verifier-kit.py` le contrôle.

## Démarrer

```bash
cd kit-i3
python3 verifier-kit.py
python3 analyse-traces.py resume
python3 executer-requete.py "SELECT COUNT(*) AS lignes FROM orders"
python3 atelier-vote.py
python3 atelier-routage.py
```

Ensuite, section 4 du protocole : écrire et contrôler vos vingt références dans `reference-i3.csv`, puis lancer `python3 analyse-traces.py rejouer --references reference-i3.csv --sortie rejeu-traces.csv`.
