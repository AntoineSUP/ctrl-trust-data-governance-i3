# Portefeuille des modèles

Supports réalisés avec assistance IA (Claude et Codex).

Relevé du 28/09/2026 du registre de modèles d'une petite entreprise : **soixante couples modèle et accès**, classés en cinq groupes de capacité. Le tableau sert à lire une offre et à calculer un coût. Le parcours I3 n'appelle aucun modèle : les traces du kit ont été produites le 25/09/2026 avec des modèles gratuits de Groq et d'OpenRouter, dont plusieurs figurent dans ce tableau.

Note de lecture : les prix sont hors taxes, en dollars par million de tokens pour les routes facturées au token, en euros par million de tokens pour le coût effectif d'un abonnement.


Ce tableau conserve ses soixante lignes du 28 septembre 2026, y compris des routes depuis retirées. Si un modèle des traces est absent du tableau, documenter son accès, son indice public et ses prix dans `gabarits/synthese-modeles.csv`, avec source et date ; une donnée non documentée reste N/D.

## Ce qu'une ligne décrit

Une ligne associe **un modèle** et **une voie d'accès**. Le même modèle apparaît plusieurs fois quand plusieurs fournisseurs le servent : sa capacité ne change pas, son prix, son quota et sa disponibilité changent. C'est pourquoi la clé porte les deux, sous la forme `modele#fournisseur`.

| Colonne | Ce qu'elle donne |
|---|---|
| Groupe | Le groupe de capacité, de G1 à G5, attribué par l'entreprise |
| Clé modèle et accès | L'identifiant interne du couple, `modele#fournisseur` |
| Identifiant d'appel | Le nom exact à écrire dans la requête de ce fournisseur |
| Voie d'accès | Abonnement à quota, achat de tokens, plan gratuit ou calcul local |
| Statut | Retenu en production, candidat à l'essai, écarté |
| Indice public | Score de bancs d'essai publics, relevé le 28/09/2026 |
| Entrée et sortie | Prix affiché par le fournisseur, par million de tokens |
| Coût effectif | Ce que coûte réellement le million de tokens de cette voie d'accès |
| Contexte | Nombre de tokens que le modèle accepte dans une requête |

## Les cinq groupes de capacité

| Groupe | Lignes | Ce que l'entreprise y confie | Indice public observé |
|---|---:|---|---|
| G1 | 9 | Jugement, livrable qui engage l'entreprise | 47,0 à 57,6 |
| G2 | 14 | Production courante | 9,3 à 47,0 |
| G3 | 12 | Tri, extraction, résumé | 11,3 à 41,8 |
| G4 | 7 | Préparation de contexte, classement | 5,5 à 15,4 |
| G5 | 13 | Accès gratuits et calculs déterministes | 9,0 à 33,7 |

Le groupe n'est pas une mesure : c'est une décision d'exploitation qui combine la capacité observée, le prix et la voie d'accès. Un modèle de G3 peut porter un indice public supérieur à un modèle de G2 servi par une voie plus chère. Cinq lignes n'ont pas de groupe : elles sont écartées ou en attente de classement.

## Lire l'indice public

L'indice agrège des bancs d'essai publics et classe les modèles entre eux. Il ne dit pas si un modèle réussit une question donnée : cela se mesure sur ses propres cas, contre une référence. Une case vide signifie que l'indice n'a pas été relevé pour cette ligne, pas qu'il vaut zéro.

Entre les deux extrémités du portefeuille, l'indice varie d'un facteur six et le prix d'entrée d'un facteur mille. La capacité ne se paie donc pas proportionnellement.

## Les quatre voies d'accès

| Voie | Lignes | Ce que l'entreprise paie | Ce qui limite l'usage |
|---|---:|---|---|
| Abonnement | 16 | Un forfait mensuel | Un quota qui se recharge par fenêtre de temps |
| Achat de tokens | 31 | Chaque token consommé | Le budget |
| Plan gratuit | 12 | Rien | Requêtes et tokens par minute et par jour |
| Calcul local | 1 | Rien | Ce qu'un script déterministe sait faire |

Le coût effectif traduit ces voies dans la même unité. Pour une route facturée au token, il reprend le prix affiché converti en euros. Pour un abonnement, il rapporte le prix du forfait à la consommation de la période : le même modèle coûte alors vingt fois moins par million de tokens que sur sa route payante, tant que le quota suffit.

## Le tableau complet

| Groupe | Clé modèle et accès | Identifiant d'appel | Fournisseur d'appel | Voie d'accès | Statut | Indice public | Entrée, USD HT/M | Sortie, USD HT/M | Coût effectif entrée, EUR/M | Coût effectif sortie, EUR/M | Contexte, tokens |
|---|---|---|---|---|---|---|---|---|---|---|---|
| G1 | claude-fable-5-1#claude | claude-fable-5-1 | claude | abonnement | retenu | 53.4 | 10 | 50 | 0.4295 | 2.1475 | 1000000 |
| G1 | claude-fable-5-1#openrouter | anthropic/claude-fable-5.1 | openrouter | payant | candidat | 53.4 | 10 | 50 | 8.7696 | 43.8481 | 1000000 |
| G1 | claude-opus-5#claude | claude-opus-5 | claude | abonnement | retenu | 50.8 | 5 | 25 | 0.2148 | 1.0738 | 1000000 |
| G1 | claude-opus-5#openrouter | anthropic/claude-opus-5 | openrouter | payant | candidat | 50.8 | 5 | 25 | 4.3848 | 21.9241 | 1000000 |
| G1 | claude-opus-5-5#claude | claude-opus-5-5 | claude | abonnement | retenu | 57.6 | 4 | 20 | 0.1718 | 0.859 | 1000000 |
| G1 | gpt-5.6-sol#openrouter | openai/gpt-5.6-sol | openrouter | payant | candidat | 47 | 2 | 10 | 1.7539 | 8.7696 | 1050000 |
| G1 | gpt-6-astra#codex | gpt-6-astra | codex | abonnement | retenu | 52.7 | 10 | 50 | 0.6316 | 3.1578 | 272000 |
| G1 | gpt-6-astra#openrouter | openai/gpt-6-astra | openrouter | payant | candidat | 52.7 | 10 | 50 | 8.7696 | 43.8481 | 1050000 |
| G1 | muse-spark-1.3#openrouter | meta/muse-spark-1.3 | openrouter | payant | candidat |  | 1.25 | 4.25 | 1.0962 | 3.7271 | 1048576 |
| G2 | claude-sonnet-5#claude | claude-sonnet-5 | claude | abonnement | retenu | 38.2 | 2 | 10 | 0.0859 | 0.4295 | 1000000 |
| G2 | deepseek-v4-pro#openrouter | deepseek/deepseek-v4-pro | openrouter | payant | candidat | 30.4 | 0.95526 | 1.91052 | 0.8377 | 1.6755 | 1048576 |
| G2 | deepseek-v4-pro-0813#openrouter | deepseek/deepseek-v4-pro-0813 | openrouter | payant | candidat |  | 0.2523 | 3.5 | 0.2213 | 3.0694 | 1048576 |
| G2 | gemini-3.1-pro-preview#google | google/gemini-3.1-pro-preview | google | abonnement | retenu | 29.7 | 2 | 12 | 1.7539 | 10.5235 | 1048576 |
| G2 | gemini-3.1-pro-preview#openrouter | google/gemini-3.1-pro-preview | openrouter | payant | candidat | 29.7 | 2 | 12 | 1.7539 | 10.5235 | 1048576 |
| G2 | glm-5.3#openrouter | z-ai/glm-5.3 | openrouter | payant | candidat | 44.8 | 0.37 | 1.14 | 0.3245 | 0.9997 | 1310720 |
| G2 | gpt-5.5#codex | gpt-5.5 | codex | abonnement | retenu | 38.4 | 5 | 30 | 0.3158 | 1.8947 | 272000 |
| G2 | gpt-5.6-sol#codex | gpt-5.6-sol | codex | abonnement | retenu | 47 | 4 | 20 | 0.2526 | 1.2631 | 272000 |
| G2 | gpt-5.6-terra#codex | gpt-5.6-terra | codex | abonnement | retenu | 42.1 | 2 | 12 | 0.1263 | 0.7579 | 272000 |
| G2 | grok-4.6#openrouter | x-ai/grok-4.6 | openrouter | payant | candidat | 44.3 | 2 | 6 | 1.7539 | 5.2618 | 500000 |
| G2 | kimi-k3#openrouter | moonshotai/kimi-k3 | openrouter | payant | candidat | 43.6 | 3 | 15 | 2.6309 | 13.1544 | 1048576 |
| G2 | mistral-large-2512#openrouter | mistralai/mistral-large-2512 | openrouter | payant | candidat | 9.3 | 0.5 | 1.5 | 0.4385 | 1.3154 | 262144 |
| G2 | mistral-medium-3-5#openrouter | mistralai/mistral-medium-3-5 | openrouter | payant | candidat |  | 1.5 | 7.5 | 1.3154 | 6.5772 | 262144 |
| G2 | qwen3.8-max-0902#openrouter | qwen/qwen3.8-max-0902 | openrouter | payant | candidat | 45.4 | 2 | 6 | 1.7539 | 5.2618 | 1000000 |
| G3 | claude-haiku-4-5#claude | claude-haiku-4-5 | claude | abonnement | retenu |  | 1 | 5 | 0.043 | 0.2148 | 200000 |
| G3 | deepseek-v3.2#openrouter | deepseek/deepseek-v3.2 | openrouter | payant | candidat |  | 0.28 | 0.42 | 0.2455 | 0.3683 | 163840 |
| G3 | deepseek-v4.1-flash#openrouter | deepseek/deepseek-v4.1-flash | openrouter | payant | candidat | 39.5 | 0.035 | 0.29 | 0.0307 | 0.2543 | 1048576 |
| G3 | gemini-3.6-flash#google | google/gemini-3.6-flash | google | abonnement | retenu | 34 | 0.75 | 3.75 | 0.6577 | 3.2886 | 1048576 |
| G3 | gemini-3.8-flash#google | google/gemini-3.8-flash | google | abonnement | retenu | 40.9 | 0.75 | 3.75 | 0.6577 | 3.2886 | 1048576 |
| G3 | gemini-3.8-flash#openrouter | google/gemini-3.8-flash | openrouter | payant | candidat | 40.9 | 0.75 | 3.75 | 0.6577 | 3.2886 | 1048576 |
| G3 | glm-5.3-flash#openrouter | z-ai/glm-5.3-flash | openrouter | payant | candidat | 41.8 | 0.15 | 0.5 | 0.1315 | 0.4385 | 1310720 |
| G3 | gpt-5.6-luna#codex | gpt-5.6-luna | codex | abonnement | retenu | 37.3 | 0.2 | 1.2 | 0.0126 | 0.0758 | 272000 |
| G3 | gpt-5.6-luna#openrouter | openai/gpt-5.6-luna | openrouter | payant | candidat | 37.3 | 0.2 | 1.2 | 0.1754 | 1.0524 | 1050000 |
| G3 | gpt-6-luna#openrouter | openai/gpt-6-luna | openrouter | payant | candidat | 37.3 | 0.1 | 0.5 | 0.0877 | 0.4385 | 1050000 |
| G3 | mistral-small-2603#openrouter | mistralai/mistral-small-2603 | openrouter | payant | candidat | 11.3 | 0.15 | 0.6 | 0.1315 | 0.5262 | 262144 |
| G3 | qwen3.8-flash#openrouter | qwen/qwen3.8-flash | openrouter | payant | candidat |  | 0.15 | 0.47 | 0.1315 | 0.4122 | 1000000 |
| G4 | deepseek-v4-flash-0731#openrouter | deepseek/deepseek-v4-flash-0731 | openrouter | payant | candidat |  | 0.021 | 0.32 | 0.0184 | 0.2806 | 1310720 |
| G4 | gemini-3.1-flash-lite#google | google/gemini-3.1-flash-lite | google | abonnement | retenu |  | 0.25 | 1.5 | 0.2192 | 1.3154 | 1048576 |
| G4 | gemma-4-31b-it#openrouter | google/gemma-4-31b-it | openrouter | payant | candidat | 15.4 | 0.09 | 0.34 | 0.0789 | 0.2982 | 262144 |
| G4 | gpt-oss-120b#openrouter | openai/gpt-oss-120b | openrouter | payant | candidat | 11.6 | 0.15 | 0.6 | 0.1315 | 0.5262 | 131072 |
| G4 | ministral-8b-2512#openrouter | mistralai/ministral-8b-2512 | openrouter | payant | candidat | 5.5 | 0.15 | 0.15 | 0.1315 | 0.1315 | 262144 |
| G4 | nemotron-3.5-lightning#openrouter | nvidia/nemotron-3.5-lightning | openrouter | payant | candidat | 12.9 | 0.08 | 0.2 | 0.0702 | 0.1754 | 1000000 |
| G4 | qwen3.7-flash#openrouter | qwen/qwen3.7-flash | openrouter | payant | candidat |  | 0.03 | 0.13 | 0.0263 | 0.114 | 1000000 |
| G5 | gemma-4-31b-it:free#openrouter | google/gemma-4-31b-it:free | openrouter | gratuit | candidat |  | 0 | 0 | 0 | 0 | 262144 |
| G5 | glm-5.2:free#openrouter | z-ai/glm-5.2:free | openrouter | gratuit | écarté |  | 0 | 0 | 0 | 0 | 32768 |
| G5 | gpt-oss-120b#groq | openai/gpt-oss-120b | groq | gratuit | candidat | 11.6 | 0 | 0 | 0 | 0 | 131072 |
| G5 | gpt-oss-20b#groq | openai/gpt-oss-20b | groq | gratuit | candidat | 9 | 0 | 0 | 0 | 0 | 131072 |
| G5 | gpt-oss-safeguard-20b#groq | openai/gpt-oss-safeguard-20b | groq | gratuit | candidat |  | 0 | 0 | 0 | 0 | 131072 |
| G5 | inkling:free#openrouter | thinkingmachines/inkling:free | openrouter | gratuit | candidat |  | 0 | 0 | 0 | 0 | 1048576 |
| G5 | ling-3.0-flash-vl:free#openrouter | inclusionai/ling-3.0-flash-vl:free | openrouter | gratuit | écarté |  | 0 | 0 | 0 | 0 | 262144 |
| G5 | nemotron-3-ultra-550b-a55b:free#openrouter | nvidia/nemotron-3-ultra-550b-a55b:free | openrouter | gratuit | candidat |  | 0 | 0 | 0 | 0 | 1000000 |
| G5 | nemotron-3.5-lightning:free#openrouter | nvidia/nemotron-3.5-lightning:free | openrouter | gratuit | candidat |  | 0 | 0 | 0 | 0 | 1000000 |
| G5 | nex-n2.5-pro:free#openrouter | nex-agi/nex-n2.5-pro:free | openrouter | gratuit | écarté |  | 0 | 0 | 0 | 0 | 262144 |
| G5 | qwen3.8-27b#groq | qwen/qwen3.8-27b | groq | gratuit | candidat | 33.7 | 0 | 0 | 0 | 0 | 131072 |
| G5 | script#script | script | script | local | retenu |  | 0 | 0 | 0 | 0 |  |
| G5 | stealth/space-bunny-alpha#openrouter | stealth/space-bunny-alpha | openrouter | gratuit | candidat |  | 0 | 0 | 0 | 0 | 1000000 |
|  | gpt-6-luna#codex | gpt-6-luna | codex | abonnement | écarté | 37.3 |  |  |  |  | 272000 |
|  | gpt-6-sol#codex | gpt-6-sol | codex | abonnement | écarté | 47.5 |  |  |  |  | 272000 |
|  | hy4-preview#openrouter | tencent/hy4-preview | openrouter | payant | écarté |  | 0.834 | 2.501 | 0.7314 | 2.1933 | 1048576 |
|  | muse-spark-1.3-contributor#openrouter | meta/muse-spark-1.3-contributor | openrouter | payant | écarté |  | 0.1 | 0.2 | 0.0877 | 0.1754 | 1048576 |
|  | xiaomi/mimo-v2.6-flash#openrouter | xiaomi/mimo-v2.6-flash | openrouter | payant | candidat |  | 0.14 | 0.28 | 0.1228 | 0.2455 | 1048576 |

## Sources

- Registre de modèles au 28/09/2026, empreinte SHA-256 `7ac6eb9bb7fc70ab`, soixante lignes.
- Prix des routes facturées au token : catalogue public du fournisseur agrégateur, relu le 29/09/2026.
- Indices publics : page de classements publics du même agrégateur, relevée le 28/09/2026.
- Taux de conversion euro contre dollar : taux de référence de la Banque centrale européenne du 25/09/2026, 1,1403 dollar par euro.

Les catalogues et les prix changent d'une semaine à l'autre. Relire les sources avant de réutiliser un chiffre de ce tableau.
