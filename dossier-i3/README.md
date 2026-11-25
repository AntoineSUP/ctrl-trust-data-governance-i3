# Gabarits du dossier de décision

Supports réalisés avec assistance IA (Claude et Codex).

Copier ces formulaires dans votre dossier de travail avant de les remplir. Ne renseigner que les champs que vous pouvez appuyer sur une preuve ; une mesure absente reste vide, avec son explication. Écrire N/D et son motif quand une donnée n'est pas documentée. Chaque fichier porte en tête de ligne ou de page l'équipe, la version et la date.

## Index

| Gabarit | Usage | Section du dossier | Jalon |
|---|---|---|---|
| `perimetre-usage.md` | Usage visé, utilisateurs, décisions soutenues et exclues, conséquences d'une erreur, critères de réussite | Périmètre d'usage | J1 |
| `responsabilites.csv` | Qui réalise, approuve, est consulté et informé pour chaque activité ; preuve conservée | Responsabilités | J1 |
| `dictionnaire-donnees.csv` | Définition, unité, clé, règle qualité, source, propriétaire, caractère personnel, sensibilité et conservation de chaque colonne | Données | J1, J2 |
| `regles-qualite.csv` | Règles contrôlables, requête qui compte les écarts, seuil, résultats sur la base et la variante, action en cas d'écart | Données | J2 |
| `cycle-de-vie.csv` | Création, finalité, stockage, accès, conservation, archivage et suppression de chaque objet | Données | J2 |
| `registre-risques.csv` | Risques, causes, conséquences, personnes exposées, cotation, mesures, risque résiduel, suivi | Risques, éthique et biais | J2 |
| `politique-escalade.md` | Contrôle avant acceptation, déclencheurs, niveaux d'escalade, conduite si indisponible, arrêt ou restriction | Incidents et escalade | J2 |
| `fiche-incident.md` | Description, qualification, mesures, cause, actions et retour d'expérience d'un incident | Incidents et escalade | J2 |
| `fiche-decision.md` | Mise en service, mise en service restreinte ou report ; conditions, preuves, limites, révision | Décision | J3 |
| `comparaison-modele-question.csv` | Une ligne finale par modèle et par question, avec verdict et explication | Contrôles | J1 |
| `exemple-comparaison.md` | Définition des colonnes et exemple fictif de comparaison | Contrôles | J1 |
| `synthese-modeles.csv` | Une ligne par modèle du lot 2 : indice public, prix datés, accès, résultats par famille, limites | Contrôles | J1, J2 |
| `tests-vote.csv` | Panels, seuils, valeurs proposées, résultat attendu et obtenu | Contrôles | J2 |
| `comparaison-configurations.csv` | Configurations comparées : justes, faux, abstentions, coûts, revues humaines | Décision | J2, J3 |
| `calcul-cout.csv` | Coût équivalent de chaque essai, avec prix daté et champs manquants | Décision | J2 |
| `contributions.csv` | Registre de contribution individuelle : membre, rôle, élément, emplacement, contrôle | Annexe de preuve | J1, J2, J3 |
| `journal-decisions.csv` | Faits, hypothèses, limites, décisions et recommandations, datés et sourcés | Annexe de preuve | J1, J2, J3 |
| `declaration-ia.md` | Déclaration de tout usage d'IA générative, ou de l'absence d'usage | Annexe de preuve | J3 |

Les jalons sont ceux du sujet de projet : J1 à la fin de l'encadrement 1, J2 à la fin de l'encadrement 2, J3 à la soutenance.

## Règles de remplissage

- Distinguer les natures : donnée synthétique, trace historique, proposition de l'équipe.
- Citer une preuve précise : fichier, ligne, `cell_id`, requête, ou source juridique avec sa date de consultation.
- Ne copier dans aucun gabarit de donnée personnelle réelle, de copie ou de note d'étudiant.
- Garder une ligne par élément : un CSV ne contient jamais deux saisies de la même information.
- Dimensions de qualité utilisées dans `regles-qualite.csv` : complétude, validité, unicité, cohérence, exactitude, actualité. Chaque requête de contrôle rend une ligne et une colonne : le nombre d'écarts ; la ligne `EX01` montre le format.
- Cotation du registre des risques : probabilité et gravité de 1 à 3, criticité égale à leur produit.
