## Quelques instructions
### [Oxygen CS](#oxygen-cs)
Pour run le container, simplement executer `docker run -e TOKEN=b9824c123708eeeb1146 -e HOST=http://159.203.50.162 turbowarrior/oxygen_cs-app:latest` après avoir pull l'image à partir du DockerHub
Note: parfois, la connexion ne se fait pas, reessayer la commande 3 à 5 fois pour être certain que la connexion se fasse.

### [Metrics](#metrics)
Pour run le container, simplement exécuter la commande `docker run -p 8080:80 -e ASPNETCORE_URLS="http://+:80" metrics-app` après avoir pull l'image à partir de DockerHub
Ensuite, naviguer vers `http://localhost:8080/swagger/` pour avoir accès à l'application

## [Modification du code source](#modification-du-code-source)
Il nous était demandé de modifier le code source de l'application afin de pouvoir la lancer sur n'importe quelle habitation (HOST).

### [Variables d'environnement](#variables-denvironnement)
Pour ce faire, nous avons eu recours à l'utilisation de variables d'environnement que nous avons déposées localement dans un fichier `.env`. En modifiant ces valeurs avec des valeurs valides, il est possible de tester l'application sur n'importe quelle habitation. Ces valeurs d'environnement comprennent le HOST (l'habitation) et le TOKEN.

Veuillez noté qu'à la base, 5 valeurs d'environnement doivent être utilisées. Premièrement le HOST et le TOKEN, tels que mentionnés dans le paragraphe ci-haut, puis finalement T_MAX (température maximale), T_MIN (température minimale) et DATABASE_URL (pour se connecter à notre BD). Les 3 dernières variables sont entrés directement dans le code source. Les variables HOST et TOKEN peuvent être définie localement, mais lorsque qu'on roule l'application avec un conteneur Docker basé sur une de nos images, il faut les écrire en argument. L'image ci-dessous permet de voir cette pratique:

<img width="1129" alt="Screenshot 2024-03-10 at 8 20 29 AM" src="https://github.com/log680-equipe07/oxygencs-grp01-eq07/assets/56934372/a978bbbd-2271-4964-b26b-35cf80d795e2">

### [Sauvegarde de données dans la base de données](#sauvegarde-de-données-dans-la-base-de-données)
Il nous était également demandé de sauvegarder des données dans la même base de donnée que celle du laboratoire 1. Ces données étaient:
- Les températures reçues;
- Leurs heures respectives;
- Les actions liés aux changements de température (climatisation, chauffage, none)

Ces données sont récupérées dans notre méthode `save_event_to_database`. Celle-ci s'occupe de les envoyer vers notre base de donnée. Bien sûr, nous avons dû créer une table avec son schéma afin de pouvoir supporter nos requêtes vers la base de données.

Pour ce qui est du module nous aidant à effectuer ces opérations, nous avons opté pour pyscopg2 car cela semblait être un choix commun en ce qui concerne la gestion des bases de données PostGreSQL pour un projet en python.

### [Tests unitaires](#tests-unitaires)
Pour ce qui est des tests unitaires liés à cette application, nous avons utilisé unittest. Puisque la complexité d'Oxygen CS n'était pas au rendez-vous et que le but du laboratoire n'est pas de couvrir l'entièreté de l'application en fond et en comble, nous nous en sommes tenus à des tests qui traitaient des points généraux dans le code source. Cela comprend donc le changement d'action selon la température mesuré, soit TurnOnAc et TurnOnHeater, et la gestion des données vers la base de données. En effet, en utilisant Magic Mock, il est possible de tester le comportement de la gestion de nos données, y compris le soulèvement d'exception en cas d'erreur d'envoie vers la base de donnée.

## [Conteneurisation des applications](#conteneurisation-des-applications)
Deux fichiers d'image Dockerfile furent créées afin de pouvoir rouler l'application dans n'importe quel environnement. Cette étape était nécessaire afin de pouvoir construire des images dans nos Pipelines d'intégration et de les push sur DockerHub.

### [Image Oxygen CS](#image-oxygen-cs)
La première image était pour l'application HVAC. Nous avons décidé de demeurer avec le code source de base en python. Au départ, notre image se trouver à 1 Gb. Grâce à des choix judicieux tels que l'utilisation d'une image de base de petite taille (python:3.12.2-alpine3.19) puis notamment un multi-stage build permettant de seulement installer les packages nécessaires lors du runtime. La taille de  image finale compressée tourne autour de 27 Mb à 29 Mb. Nous investiguons constamment en des moyens de réduire cette la taille de cette image afin qu'elle soit en dessous de 25 Mb.

<img width="897" alt="Screenshot 2024-03-10 at 3 50 35 AM" src="https://github.com/log680-equipe07/oxygencs-grp01-eq07/assets/56934372/57a320c3-1516-4909-9fe2-947a8d3ed7d5">

### [Image Metrics](#image-metrics)
Pour ce qui est de l'application Metrics, nous avons une image non compressé avec une taille de 229.92 Mb, puisque l'impact de cette taille est moindre, nous avons décidé de la laisser de cette taille.
![image](https://github.com/log680-equipe07/oxygencs-grp01-eq07/assets/56934372/3c334084-79ac-465e-8043-00d737c72495)


## [Intégration Continue](#intégration-continue)

### [Pre-commit](#pre-commit)
Pour ce qui du pre-commit, il nous était demandé d'ajouter des git hooks pour les tâches suivantes:
- Étapes de linting/Analyse statique de code
  Pour ce hook, nous avons utilisé pylint, ce choix semblait idéal notamment dû au manque de complexité de notre application. Une beauté de pylint est que le module fait une analyse de code qui est complexe, mais adapté à notre niveau de complexité tel que mentionné.
- Formattage
  Pour ce qui est du formattage, nous avons utilisé un autre module assez populaire, soit black. Encore une fois, le manque de complexité de l'application permet de faire des choix d'implémentation commun.
- Tests unitaires
  Pour ce hook, nous avons tout simplement fait référence à notre commande entré dans notre Pipfile dans la section [script] pour s'assurer que les tests étaient roulés aussi bien que manuellement.

Ci-dessous se trouve une screenshot montrant que notre application possède bel et bien un pre-commit.
<img width="570" alt="Screenshot 2024-03-10 at 3 53 02 AM" src="https://github.com/log680-equipe07/oxygencs-grp01-eq07/assets/56934372/590d5d9a-226f-4a1e-9e6b-6180a5149001">

### [Pipeline Oxygen CS](#pipeline-oxygen-cs)

En ce qui concerne notre pipeline d'intégration continue pour Oxygen CS, nous avons utilisé un workflow de GitHub Actions, nous nous sommes assurés que ce pipeline n'était exécuté que lorsque des évènements avaient lieux sur la branche main.

Un exemple d'un build ayant été avec succès est fourni en capture d'écran ci-dessous, les différentes étapes y sont affichées. À noté que si un job échoue soit pour notamment les tests unitaires, le pylint ou bien le formattage, le build échoue à l'étape concernée et n'est pas complété.

<img width="1042" alt="Screenshot 2024-03-10 at 4 01 10 AM" src="https://github.com/log680-equipe07/oxygencs-grp01-eq07/assets/56934372/2731ddfd-48b9-44ac-b17b-cc5cf0df8b07">

Voici un exemple de les différents builds disponibles sur DockerHub:
![image](https://github.com/log680-equipe07/oxygencs-grp01-eq07/assets/56934372/fd68dbaf-37cf-4841-acf4-17df1145aa15)


### [Pipeline Metrics](#pipeline-metrics)
La même logique fut utilisée en ce qui concerne le pipeline pour Metrics, voici le résultat obtenu sur DockerHub:

![image](https://github.com/log680-equipe07/oxygencs-grp01-eq07/assets/56934372/064f167e-e37e-4e32-9e53-05d567cd00fb)

## [Métriques d'intégration continue](#métriques-dintégration-continue)
L'ajout des métriques de pipeline dans l'application Metrics implique l'ajout de toutes les entités permettant de réduire le couplage de notre application et de la rendre plus résiliente face aux changements et erreurs pouvant survenir.
Nous avons donc ajouté:
- un nouveau PipelineService, qui gère la désérialisation de notre réponse de l'api de Graphql GitHub
- un nouveau modèle DTO pour les informations du pipeline, qui nous permet de faciliter la désérialisation
- un nouveau modèle d'information de pipeline, pour pouvoir manipuler avec aises une liste d'informations basées sur le data reçu de GitHub
- un nouveau contrôleur de pipeline, pour gérer nos nouvelles routes et montrer l'information nécessaire. Comprend la plupart des services nécessaire à son fonctionnement sous forme de dependency injection
- un nouveau modèle d'information représenter le pipeline snapshot, celui-ci comprend:
  - Guid     -> identificateur unique de l'instance du tableau, représente la clé primaire
  - RepoName -> nom du repo dont on cherche les informations
  - Successes -> nombre de builds ayant réussis
  - Failures  -> nombre de builds ayant échoués
  - AverageBuildTime -> moyenne de temps d'exécution pour tous les builds


Pour ce qui est des métriques d'intégration continue, nous avons opté pour celles données en exemple dans l'énoncé de laboratoire, soit:

- temps d'exécution pour un build donné;
- temps moyen d'execution pour l'ensemble de builds pour une période donnée;
- quantité de builds réussis pour une période donnée;
- quantité de builds échoués pour une période donnée;

Il n'était pas spécifier d'utiliser graphQL pour effectuer nos requêtes sur Metrics, mais puisque nous l'avions fait au laboratoire 1, nous avons décidé de poursuivre avec cet API.
Il a prouvé difficile de concevoir une requête directement claire avec ce dont nous avions de besoin car l'API GraphQL ne supporte pas encore les requêtes directe de GitHub Actions. Mais l'important est la tenacité de ses résultats.

Nous avons décidé d'implémenter nos 4 métriques dans 4 routes distinctes. Nous avons également ajouté une cinquième route qui représente l'envoie de données du pipeline vers notre base de données. La description de ces données est fournie dans la section Pipeline Metrics

Voici un exemple de notre nouvelle table avec une seule instance pour le moment (1 seul test).
![image](https://github.com/log680-equipe07/oxygencs-grp01-eq07/assets/56934372/99be66c1-7780-4bd6-995d-8ced054c08c2)

