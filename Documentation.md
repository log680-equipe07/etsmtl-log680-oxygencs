## Modification du code source
Il nous était demandé de modifier le code source de l'application afin de pouvoir la lancer sur n'importe quelle habitation (HOST).

### Variables d'environnement
Pour ce faire, nous avons eu recours à l'utilisation de variables d'environnement que nous avons déposées localement dans un fichier `.env`. En modifiant ces valeurs avec des valeurs valides, il est possible de tester l'application sur n'importque quelle habitation.

### Sauvegarde de données dans la base de données
Il nous était également demandé de sauvegarder des données dans la même base de donnée que celle du laboratoire 1. Ces données étaient:
- Les températures reçues;
- Leurs heures respectives;
- Les actions liés aux changements de température (climatisation, chauffage, none)

Ces données sont récupérées dans notre méthode `save_event_to_database`. Celle-ci s'occupe de les envoyer vers notre base de donnée. Bien sûr, nous avons dû créer une table avec son schéma afin de pouvoir supporter nos requêtes vers la base de données.

Pour ce qui est du module nous aidant à effectuer ces opérations, nous avons opté pour pyscopg2 car cela semblait être un choix commun dans le langage python.
## Conteneurisation des applications

### Image Oxygen CS

### Image Metrics

## Intégration Continue

### Pre-commit

### Pipeline Oxygen CS

### Pipeline Metrics

## Métriqus d'intégration continue