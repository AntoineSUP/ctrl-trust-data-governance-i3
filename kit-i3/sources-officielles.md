# Repères pour les situations

Supports réalisés avec assistance IA (Claude et Codex).

Consultation : 19/10/2026. Cette fiche se lit hors ligne ; les liens permettent une actualisation ultérieure. Les situations et les durées proposées par les équipes restent fictives. Les règles de l'école et le canal de rendu sont ceux du cadre I3 remis par l'enseignant.

## Qualifier les données et l'usage

Décrire la finalité, les personnes concernées et la base juridique, puis limiter les données au besoin. Le RGPD prévoit aussi exactitude, durée justifiée et sécurité. Les identifiants remplacés par des codes peuvent encore désigner des personnes ; un remplacement de nom ne suffit pas à anonymiser. Le jeu de cette activité est entièrement synthétique. [CNIL, RGPD, articles 5 et 6](https://www.cnil.fr/fr/reglement-europeen-protection-donnees/chapitre2).

Pour S2, distinguer l'habilitation interne d'un salarié du droit d'accès d'une personne à ses propres données. Pour S4, examiner l'article 22 lorsqu'une décision exclusivement automatisée produit des effets juridiques ou affecte significativement une personne. Ses exceptions et garanties demandent une qualification du cas. [CNIL, RGPD, articles 15 et 22](https://www.cnil.fr/fr/reglement-europeen-protection-donnees/chapitre3).

## Organiser les contrôles

Prévoir des accès limités, un contrôle des prestataires, une sécurité adaptée et l'examen du besoin d'analyse d'impact. Pour une violation de données personnelles, apprécier le risque : notification à l'autorité, si requise, dans les meilleurs délais et si possible sous 72 heures après connaissance ; information des personnes en cas de risque élevé, sous les conditions du texte. [CNIL, RGPD, articles 25, 28, 32 à 35](https://www.cnil.fr/fr/reglement-europeen-protection-donnees/chapitre4).

Une valeur de CA fausse ne suffit pas à caractériser une violation de données : rechercher une atteinte à la confidentialité, l'intégrité ou la disponibilité de données personnelles à la suite d'un incident de sécurité. [CNIL, définition d'une violation](https://www.cnil.fr/fr/definition/violation-de-donnees).

Fixer une durée active par finalité, examiner les besoins d'archivage séparé et organiser l'effacement. Les nombres de jours proposés dans l'exercice ne constituent aucune durée légale générale. [CNIL, durées de conservation](https://www.cnil.fr/fr/passer-laction/les-durees-de-conservation-des-donnees).

## Examiner un usage lié aux salariés

L'annexe III, point 4, du règlement européen sur l'IA vise notamment certains usages affectant la relation de travail et l'évaluation des salariés. Qualifier la finalité réelle et les conditions de l'article 6 avant de classer S4 ; le simple calcul d'un agrégat ne suffit pas à trancher. [Commission européenne, annexe III](https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3), [article 6](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6).

Le calendrier consulté, consolidé au 27/07/2026, distingue l'application générale au 02/08/2026 et celle du chapitre III, sections 1 à 3, sauf article 6(5) : 02/12/2027 pour l'article 6(2) et l'annexe III, 02/08/2028 pour l'article 6(1) et l'annexe I. Le RGPD reste à examiner séparément. [Commission européenne, article 113](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-113).

## Repères techniques

Les scripts utilisent Python et SQLite en local. Le mode SQLite `mode=ro` ouvre une base en lecture seule ; le bac à sable ajoute ses propres restrictions SQL. Ces mécanismes ne constituent pas une gestion d'habilitations par utilisateur. Les versions réellement testées figurent dans la recette enseignante. [SQLite, URI](https://www.sqlite.org/uri.html), [Python, sqlite3](https://docs.python.org/3/library/sqlite3.html).
