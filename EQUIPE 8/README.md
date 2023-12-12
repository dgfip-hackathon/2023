# Hackathon DGFiP : Quelle collectivité territoriale pour mon entreprise ? (Équipe 8)

Dans le cadre du hackathon du 24 et 25 novembre 2023, nous avons conçu et développé un prototype d'application pour répondre au défi suivant : "Défi 3 - Mesurer l’attractivité fiscale des territoires pour les entreprises".

Merci encore à la DGFiP pour l'organisation de cet événement !

## Notre Équipe

Notre équipe est constituée de :
- Mélodie Lontjens
- Memli Sheremeti
- Louis Mahé
- Thomas Charuel

Nous sommes actuellement étudiants à l'école 42.

## L'Application

### Les Technologies
Nous avons choisi le langage de programmation Python pour développer notre application web.
Pour mettre en place rapidement un prototype, nous utilisons notamment les librairies Dash et Plotly.

### Installation des packages tiers

Pour mettre en place un environnement virtuel Python :
```bash
python -m venv venv
source venv/bin/activate
```

Pour installer les librairies tierces du projet :
```bash
pip install -r requirements.txt
```

### Lancer l'application

```bash
python app.py
```

Pour consulter l'application, rendez-vous sur votre navigateur web à l'url suivante : http://127.0.0.1:8050/


### Filtres

Sur la gauche de l'écran vous avez accès aux filtres suivants :

- Secteur d'activité
- Chiffre d'affaires
- Type de local
- Surface de votre local
- Je suis propriétaire de mes locaux
- Territoire cible pour l'implantation de mon entreprise


### Résultats

- Une carte du territoire cible avec la mise en avant des communes les plus avantageuses fiscalement.
- Un récapitulatif du top 10 des communes les plus attractives.
Fonctionnement

### Fonctionnement

Pour pouvoir présenter un prototype à la fin du hackathon, nous avons fait le choix de faire les calculs "à la main" dans un tableur et non dans l'application.
Les résultats sont donc en dur dans le fichier datasets/results.csv et sont accessibles pour les secteurs d'activité suivants :
- 47.11F Hypermarchés
- 59.13B Édition et distribution vidéo
- 74.20Z Activités photographiques

Avec un peu plus de développement, il est tout à fait possible de mettre en place ce calcul dans le backend de l'application.

### Mot final

Nous tenions à vous remercier pour l'appréciation de ce projet et espérons que notre travail a su répondre à certains de vos besoins.

En cas de questions, n'hésitez pas à nous contacter via nos adresses mails ou LinkedIn.

Nous serions ravis de vous aider.
À bientôt !

Contact:
- mlontjen@student.42.fr
- mshereme@student.42.fr
- lmahe@student.42.fr
- tcharuel@student.42.fr
