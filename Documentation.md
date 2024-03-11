## Modification du code source
Il nous était demandé de modifier le code source de l'application afin de pouvoir la lancer sur n'importe quelle habitation (HOST).

### Variables d'environnement
Pour ce faire, nous avons eu recours à l'utilisation de variables d'environnement que nous avons déposées localement dans un fichier `.env`. En modifiant ces valeurs avec des valeurs valides, il est possible de tester l'application sur n'importe quelle habitation. Ces valeurs d'environnement comprennent le HOST (l'habitation) et le TOKEN.

Veuillez noté qu'à la base, 5 valeurs d'environnement doivent être utilisées. Premièrement le HOST et le TOKEN, tels que mentionnés dans le paragraphe ci-haut, puis finalement T_MAX (température maximale), T_MIN (température minimale) et DATABASE_URL (pour se connecter à notre BD). Les 3 dernières variables sont entrés directement dans le code source. Les variables HOST et TOKEN peuvent être définie localement, mais lorsque qu'on roule l'application avec un conteneur Docker basé sur une de nos images, il faut les écrire en argument. L'image ci-dessous permet de voir cette pratique:

<img width="1129" alt="Screenshot 2024-03-10 at 8 20 29 AM" src="https://github.com/log680-equipe07/oxygencs-grp01-eq07/assets/56934372/a978bbbd-2271-4964-b26b-35cf80d795e2">

### Sauvegarde de données dans la base de données
Il nous était également demandé de sauvegarder des données dans la même base de donnée que celle du laboratoire 1. Ces données étaient:
- Les températures reçues;
- Leurs heures respectives;
- Les actions liés aux changements de température (climatisation, chauffage, none)

Ces données sont récupérées dans notre méthode `save_event_to_database`. Celle-ci s'occupe de les envoyer vers notre base de donnée. Bien sûr, nous avons dû créer une table avec son schéma afin de pouvoir supporter nos requêtes vers la base de données.

Pour ce qui est du module nous aidant à effectuer ces opérations, nous avons opté pour pyscopg2 car cela semblait être un choix commun en ce qui concerne la gestion des bases de données PostGreSQL pour un projet en python.

### Tests unitaires
Pour ce qui est des tests unitaires liés à cette application, nous avons utilisé unittest. Puisque la complexité d'Oxygen CS n'était pas au rendez-vous et que le but du laboratoire n'est pas de couvrir l'entièreté de l'application en fond et en comble, nous nous en sommes tenus à des tests qui traitaient des points généraux dans le code source. Cela comprend donc le changement d'action selon la température mesuré, soit TurnOnAc et TurnOnHeater, et la gestion des données vers la base de données. En effet, en utilisant Magic Mock, il est possible de tester le comportement de la gestion de nos données, y compris le soulèvement d'exception en cas d'erreur d'envoie vers la base de donnée.

## Conteneurisation des applications
Deux fichiers d'image Dockerfile furent créées afin de pouvoir rouler l'application dans n'importe quel environnement. Cette étape était nécessaire afin de pouvoir construire des images dans nos Pipelines d'intégration et de les push sur DockerHub.

### Image Oxygen CS
La première image était pour l'application HVAC. Nous avons décidé de demeurer avec le code source de base en python. Au départ, notre image se trouver à 1 Gb. Grâce à des choix judicieux tels que l'utilisation d'une image de base de petite taille (python:3.12.2-alpine3.19) puis notamment un multi-stage build permettant de seulement installer les packages nécessaires lors du runtime. La taille de  image finale compressée tourne autour de 27 Mb à 29 Mb. Nous investiguons constamment en des moyens de réduire cette la taille de cette image afin qu'elle soit en dessous de 25 Mb.

<img width="897" alt="Screenshot 2024-03-10 at 3 50 35 AM" src="https://github.com/log680-equipe07/oxygencs-grp01-eq07/assets/56934372/57a320c3-1516-4909-9fe2-947a8d3ed7d5">

### Image Metrics
Pour ce qui est de l'application Metrics, nous avons


## Intégration Continue

### Pre-commit
Pour ce qui du pre-commit, il nous était demandé d'ajouter des git hooks pour les tâches suivantes:
- Étapes de linting/Analyse statique de code
  Pour ce hook, nous avons utilisé pylint, ce choix semblait idéal notamment dû au manque de complexité de notre application. Une beauté de pylint est que le module fait une analyse de code qui est complexe, mais adapté à notre niveau de complexité tel que mentionné.
- Formattage
  Pour ce qui est du formattage, nous avons utilisé un autre module assez populaire, soit black. Encore une fois, le manque de complexité de l'application permet de faire des choix d'implémentation commun.
- Tests unitaires
  Pour ce hook, nous avons tout simplement fait référence à notre commande entré dans notre Pipfile dans la section [script] pour s'assurer que les tests étaient roulés aussi bien que manuellement.

Ci-dessous se trouve une screenshot montrant que notre application possède bel et bien un pre-commit.
<img width="570" alt="Screenshot 2024-03-10 at 3 53 02 AM" src="https://github.com/log680-equipe07/oxygencs-grp01-eq07/assets/56934372/590d5d9a-226f-4a1e-9e6b-6180a5149001">

### Pipeline Oxygen CS

En ce qui concerne notre pipeline d'intégration continue pour Oxygen CS, nous avons utilisé un workflow de GitHub Actions, nous nous sommes assurés que ce pipeline n'était exécuté que lorsque des évènements avaient lieux sur la branche main.

Un exemple d'un build ayant été avec succès est fourni en capture d'écran ci-dessous, les différentes étapes y sont affichées. À noté que si un job échoue soit pour notamment les tests unitaires, le pylint ou bien le formattage, le build échoue à l'étape concernée et n'est pas complété.

<img width="1042" alt="Screenshot 2024-03-10 at 4 01 10 AM" src="https://github.com/log680-equipe07/oxygencs-grp01-eq07/assets/56934372/2731ddfd-48b9-44ac-b17b-cc5cf0df8b07">

Suite au succès du pipeline, il est possible de run le conteneur de l'image créée:

<img width="1129" alt="Screenshot 2024-03-10 at 8 20 29 AM" src="https://github.com/log680-equipe07/oxygencs-grp01-eq07/assets/56934372/a978bbbd-2271-4964-b26b-35cf80d795e2">


### Pipeline Metrics

## Métriques d'intégration continue
Pour ce qui est des métriques d'intégration continue, nous avons opté pour celles données en exemple dans l'énoncé de laboratoire, soit:

- temps d'exécution pour un build donné;

- temps moyen d'execution pour l'ensemble de builds pour une période donnée;
  
- quantité de builds réussis pour une période donnée;

- quantité de builds échoués pour une période donnée;

Il n'était pas spécifier d'utiliser graphQL pour effectuer nos requêtes sur Metrics, mais puisque nous l'avions fait au laboratoire 1, nous avons décidé de poursuivre avec cet API.
Il a prouvé difficile de concevoir une requête directement claire avec ce dont nous avions de besoin. mais l'important est la tenacité de ses résultats.




