# Ce que les vingt cas prouvent, et ce qu'ils ne prouvent pas

Supports réalisés avec assistance IA (Claude et Codex).

Les vingt questions du kit servent de banc d'essai à l'assistant. Une décision de mise en service s'appuie sur ce qu'elles mesurent et nomme ce qu'elles laissent sans preuve. Cette page sert à écrire les sections « Contrôles », « Risques, éthique et biais » et « Décision » du dossier.

## Ce que les vingt cas mesurent

Pour chaque question, les traces permettent de vérifier qu'une requête SQL produite par un modèle rend le bon chiffre d'affaires hors taxes, au centime près, sur une base fictive et sous des conventions écrites.

| Famille | Questions | Nombre |
|---|---|---:|
| Période | C01, C04, C05, C06, C07, C20 | 6 |
| Âge à une date de référence | C02, C08, C09, C11 | 4 |
| Âge au moment de la commande | C10 | 1 |
| Liste de produits | C03, C12, C13, C14 | 4 |
| Combinaisons | C15, C16, C17, C18, C19 | 5 |

Les questions ont été construites pour révéler des erreurs de convention précises : bornes d'une période, âge révolu ou simple différence d'années, oubli de la quantité, NULL au lieu de 0, âge pris au mauvais jour. Les données placent des commandes exactement sur les bornes des périodes et des clients nés autour des dates de référence. Une erreur de convention fausse donc au moins une des vingt valeurs.

Avec une référence indépendante, ce banc d'essai établit des faits vérifiables : tel modèle, tel jour, avec tel message, a rendu telle requête et telle valeur pour telle question.

## Ce qu'ils ne mesurent pas

### Conformité

- Aucune question ne vérifie la base légale, la finalité ou l'information des personnes. Le banc d'essai ne dit pas si l'usage de la date de naissance des clients est justifié pour la décision visée.
- Aucune question ne porte sur les droits d'accès : le bac à sable limite les opérations à la lecture des trois tables, il ne limite ni les colonnes lues ni le profil de la personne qui interroge.
- Le banc d'essai ne dit rien de la conservation des traces, des échanges avec les fournisseurs ni des décisions prises à partir des réponses.

### Équité et biais

- Aucune question ne mesure un effet sur des personnes : l'assistant produit des agrégats, et le banc d'essai ne contient ni décision individuelle ni population protégée.
- L'âge sert de filtre dans 10 questions sur 20. Le segment des clients âgés d'exactement 25 ans compte 6 clients à chacune des dates de référence : une seule erreur de convention sur l'âge déplace tout le chiffre de ce segment. Si les erreurs se concentrent sur une famille de questions, les décisions prises pour ce segment sont plus exposées que les autres ; un taux global le masque.
- Les familles comptent de 1 à 6 questions. Un écart de résultats entre familles constaté sur si peu de cas est une observation à confirmer, pas une mesure de biais.

### Fiabilité générale

- Vingt questions, une base de 59 clients, une seule exécution par modèle et par question, à température 0, un seul jour. « 18 justes sur 20 » décrit ce lot ; ce n'est ni un taux d'erreur général, ni un classement durable, ni une marge d'erreur garantie.
- Les modèles et les routes gratuites changent : deux modèles ont perdu leur route entre le lot 1 et le lot 2, dix minutes plus tard. Les traces décrivent le 25/09/2026.
- Les questions sont des agrégats de chiffre d'affaires. Les traces ne disent rien des questions d'un autre type, ni des explications rédigées en langage naturel, que l'assistant ne produit pas.

### Sécurité

- Le bac à sable protège la base : ouverture en lecture seule, une instruction, `SELECT` sur les trois tables, plafonds de lignes, de travail et de temps. Ses autotests portent sur des requêtes interdites écrites à l'avance.
- Aucune question ne teste une demande malveillante glissée dans le texte de la question, ni l'extraction de données personnelles ligne à ligne par une suite de requêtes autorisées.

## Conséquences pour la décision

| Ce que la décision peut affirmer | Ce qu'elle doit conditionner |
|---|---|
| Sur ces vingt questions, tel panel ou tel modèle rend tant de valeurs justes, avec tant d'abstentions et d'erreurs d'accès. | Un usage hors des familles testées, ou sur une autre base, demande de nouveaux cas et de nouvelles références. |
| Les erreurs observées ont des causes identifiées dans le SQL des traces. | Un usage qui touche des personnes demande une analyse des droits, de la finalité et des effets, hors de ce banc d'essai. |
| Une règle de contrôle donnée aurait détecté, ou non, chaque erreur observée. | La surveillance en service, la revue humaine et le traitement des incidents se définissent dans le dossier ; les traces n'en apportent pas la preuve. |

Chaque limite retenue figure dans le dossier, avec la mesure prévue pour la lever ou la raison de l'accepter.
