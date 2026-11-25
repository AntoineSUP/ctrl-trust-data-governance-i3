# Situations de gouvernance

Supports réalisés avec assistance IA (Claude et Codex).

Huit situations à instruire dans le dossier de décision. Chacune précise sa nature : contexte **synthétique** (inventé pour l'exercice), appui sur une **trace historique** (appel réel du 25/09/2026, identifié par sa question et son lot) ou demande de **proposition** de votre équipe. Les personnes, fonctions et chiffres des contextes sont fictifs.

Pour chaque situation, la réponse distingue les faits observés, les hypothèses et la recommandation, et cite ses preuves : trace, requête, règle, source juridique avec sa date de consultation.

## S1. Erreurs concentrées sur une famille de questions

**Nature** : contexte synthétique ; appui sur les traces historiques du lot 2.

**Contexte.** L'équipe marketing de la boutique prévoit d'utiliser l'assistant surtout pour des campagnes visant les clients de 25 ans. Le responsable du projet présente un seul chiffre : la part de réponses justes sur l'ensemble des vingt questions.

**À instruire.**

1. Calculer, à partir de votre rejeu, les réponses justes par famille de questions et par modèle, avec leurs effectifs.
2. Dire si un chiffre global décrit correctement le service rendu pour l'usage prévu.
3. Identifier les clients et les décisions les plus exposés à une erreur.
4. Dire si l'usage de l'âge pour cibler une campagne est nécessaire à la finalité, et quelles données suffisent.

**À produire** : une ligne du registre des risques (`gabarits/registre-risques.csv`) et la restriction ou le contrôle correspondant dans le périmètre d'usage.

## S2. Une demande de liste nominative

**Nature** : contexte synthétique.

**Contexte.** Un stagiaire de l'équipe commerciale demande à l'assistant : « Donne-moi les clients nés en 2001 avec leur date de naissance. » Le bac à sable autorise toute lecture des trois tables et rend jusqu'à dix lignes.

**À instruire.**

1. Dire si cette demande entre dans le périmètre d'usage que vous avez défini.
2. Proposer des profils d'accès par fonction : qui peut obtenir des agrégats, qui peut obtenir des lignes, qui accorde et retire ces droits, à quelle fréquence on les revoit.
3. Proposer une mesure technique qui réduit les données accessibles par défaut.
4. Dire ce que la trace doit conserver d'une telle demande.

**À produire** : la matrice de responsabilités (`gabarits/responsabilites.csv`) et les colonnes « donnée personnelle » et « sensibilité » du dictionnaire.

## S3. Garder les traces « pour toujours »

**Nature** : contexte synthétique ; appui sur la structure des traces historiques.

**Contexte.** L'équipe technique propose de conserver indéfiniment toutes les traces, les échanges complets avec les fournisseurs et des extractions de la base « au cas où un audit les demanderait ».

**À instruire.**

1. Lister les objets à conserver : base et extractions, questions des utilisateurs, messages envoyés, requêtes et valeurs rendues, traces, échanges bruts, références, décisions, fiches incident.
2. Pour chacun, dire s'il contient ou peut contenir des données personnelles.
3. Proposer une durée par objet, justifiée par une finalité, avec les étapes de conservation active, d'archivage et de suppression.
4. Désigner le responsable de la suppression et la preuve de cette suppression.

**À produire** : le cycle de vie (`gabarits/cycle-de-vie.csv`). Les durées sont des propositions de l'équipe, chacune justifiée.

## S4. Calculer les primes des commerciaux

**Nature** : contexte synthétique ; appui sur les traces historiques de C11 et C19, lot 2.

**Contexte.** La direction commerciale veut calculer la prime trimestrielle de chaque commercial à partir des chiffres d'affaires que l'assistant produit, sans relecture, pour gagner du temps. Dans les traces du 25/09/2026, plusieurs modèles rendent la même valeur sur C11, et d'autres la même valeur sur C19.

**À instruire.**

1. Rejouer C11 et C19, comparer les valeurs partagées à votre référence et expliquer la cause dans le SQL.
2. Qualifier ce nouvel usage : en quoi diffère-t-il d'un tableau de bord interne ? Quelles personnes subissent une erreur ?
3. Dire quels textes encadrent un système d'IA utilisé pour des décisions touchant la relation de travail ou l'évaluation des salariés, et une décision fondée exclusivement sur un traitement automatisé. Citer la source officielle et sa date de consultation.
4. Proposer la décision : refus, usage comme brouillon soumis à une référence indépendante et à une validation humaine, ou autre, avec ses conditions.

**À produire** : la fiche de décision (`gabarits/fiche-decision.md`) pour cet usage.

## S5. Envoyer des lignes clients au modèle

**Nature** : contexte synthétique ; appui sur le message historique (section 7 du protocole).

**Contexte.** Pour améliorer les réponses, un développeur propose d'ajouter au message envoyé au modèle cinquante lignes de la table `customers`, identifiants et dates de naissance compris. Le message historique ne contenait que le schéma, les conventions et la question.

**À instruire.**

1. Lister les données qui quittent l'organisation dans chaque version du message.
2. Dire ce qu'il faut vérifier chez le fournisseur avant d'envoyer des données personnelles : conditions d'utilisation, réutilisation des données, lieu de traitement, contrat.
3. Proposer une alternative qui atteint le même objectif sans envoyer de données personnelles.
4. Dire qui autorise une modification du message envoyé, et comment elle est tracée.

**À produire** : une ligne du registre des risques et la règle correspondante dans la politique d'escalade.

## S6. Un chiffre nul affiché pendant deux semaines

**Nature** : contexte synthétique construit sur la trace historique de C11, lot 2.

**Contexte.** Un tableau de bord hebdomadaire affiche le chiffre d'affaires des clients de 25 ans au 01/12/2026, calculé par l'assistant. Il indique 0 € HT pendant deux semaines. Une responsable marketing s'en étonne et le signale ; personne n'avait de contrôle sur cet indicateur.

**À instruire.**

1. Remplir la fiche incident : détection, période, impact, mesures immédiates, cause dans le SQL, actions correctives, communication, retour d'expérience.
2. Qualifier l'incident : erreur de calcul, incident de sécurité ou violation de données personnelles ? Justifier avec la définition officielle.
3. Proposer le contrôle qui aurait détecté l'erreur dès la première semaine.

**À produire** : la fiche incident (`gabarits/fiche-incident.md`).

## S7. Un fournisseur disparaît

**Nature** : appui sur les traces historiques des lots 1 et 2.

**Contexte.** Dans les traces, deux modèles répondent au lot 1, puis ne sont plus servis au lot 2, quelques minutes plus tard. D'autres modèles restent saturés sur la plupart de leurs appels.

**À instruire.**

1. Retrouver ces modèles et leurs statuts dans les traces.
2. Dire ce que devient un vote quand un membre du panel est indisponible, avec `atelier-vote.py` et un panel qui contient l'un d'eux.
3. Proposer la conduite à tenir : panel de secours, abstention, attente, escalade, et le suivi de la disponibilité.
4. Dire quelles informations sur les modèles utilisés doivent être tenues à jour, et par qui.

**À produire** : la section « Conduite si indisponible » de la politique d'escalade et une ligne du registre des risques.

## S8. Une seconde extraction de la base

**Nature** : données synthétiques (variante dégradée, anomalies injectées pour l'exercice).

**Contexte.** La boutique transmet une seconde extraction, `data/variante-degradee/`. Son nombre d'anomalies n'est pas communiqué.

**Contrat fictif de l'extraction.** La boutique réserve ce fichier aux clients majeurs à leur inscription. Une commande appartient à un seul client et survient après son inscription ; ses lignes sont uniques par couple commande-produit. Chaque produit a un prix positif renseigné, chaque quantité est strictement positive et toutes les références client et produit existent. Les dates suivent le format du schéma. L'extraction est supposée exhaustive jusqu'au 02/10/2026 à 08:00 UTC. Ces hypothèses métier servent à écrire les contrôles ; la majorité n'est pas présentée comme une obligation légale générale.

**À instruire.**

1. Écrire des règles qualité contrôlables, chacune avec une requête qui compte ses écarts, et les exécuter avec `controle-qualite.py` sur la base et sur la variante.
2. Pour chaque anomalie trouvée, décrire les lignes concernées et la cause probable.
3. Rejouer les traces sur la variante et repérer les questions dont la valeur change.
4. Dire si une réponse juste au regard de la base reste juste au regard de la réalité de la boutique, et qui doit corriger les données.

**À produire** : les règles qualité (`gabarits/regles-qualite.csv`) avec leurs résultats sur les deux bases, et les colonnes « règle qualité » du dictionnaire.
