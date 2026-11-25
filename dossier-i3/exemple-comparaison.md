# Présenter la comparaison modèle par question

Supports réalisés avec assistance IA (Claude et Codex).

Remplir `comparaison-modele-question.csv` au format CSV UTF-8 : une ligne finale par modèle et par question. Pour le lot 2, cela fait 280 lignes : 14 modèles et 20 questions. Les traces gardent le dernier état de chaque cellule. Le compteur `attempts` indique le nombre d’essais ; les détails et tokens des essais précédents ne sont pas fournis.

| Colonne | Contenu |
|---|---|
| `case_id`, `modele` | Identifiant de la question et couple exact `fournisseur:modèle` |
| `fichier_trace`, `cell_id` | Fichier source et identifiant de la cellule dans la trace |
| `nature` | `historique` pour la trace d'origine, `rejeu` pour votre réexécution, `simulation` pour un exemple inventé |
| `statut` | Verdict du rejeu : `juste`, `faux`, `sql_invalide`, `sql_refuse`, `non_execute` |
| `valeur_centimes_ht`, `reference_centimes_ht` | Valeur obtenue, si elle existe, et votre référence contrôlée |
| `explication` | Cause appuyée sur le SQL ou le message d'erreur, ou lien relatif vers une note qui la démontre |

La matrice modèles par questions est une vue de ce CSV : modèles en lignes, questions en colonnes, statut affiché. Montrer cette vue pendant la séance ; remettre le CSV long. Aucune seconde saisie ni table des causes séparée.

## Exemple fictif de format

L'exemple utilise une question et des modèles inventés. Il ne contient aucune réponse du kit ni aucun résultat mesuré.

```csv
case_id,modele,fichier_trace,cell_id,nature,statut,valeur_centimes_ht,reference_centimes_ht,explication
DEMO-X,demo:modele-A,traces-fictives.csv,demo-cellule-A,simulation,juste,123,123,Exemple fictif de format ; dernier essai 1
DEMO-X,demo:modele-B,traces-fictives.csv,demo-cellule-B,simulation,non_execute,,123,Délai fictif dépassé ; valeur absente ; dernier essai 2
```

## Résumer les modèles

Remplir une ligne par modèle du lot 2 dans `synthese-modeles.csv`. Lire le portefeuille comme source. Indiquer l'indice public avec sa source et sa date, les prix d'entrée et de sortie documentés d'une route payante du même modèle exact, la source et la date des prix, et l'accès utilisé le 25/09/2026. Écrire N/D et son motif quand un indice ou une route payante n'est pas documenté.

Pour chaque famille de questions, donner les réponses justes sur les réponses évaluées, puis les échecs d'accès ou cellules non exécutées, avec la référence du fichier. Une question combinée appartient à sa famille combinée ; l'indiquer quand une lecture par famille élémentaire la compte deux fois. Ces observations soutiennent une hypothèse sur ce lot, pas un classement durable ni un taux d'erreur général. Les prix sont en dollars hors taxes par million de tokens.
