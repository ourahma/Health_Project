
# Projet Health App 🚑

## Description 📝
Health App est un système de gestion médicale complet destiné aux cabinets médicaux. Il offre une gestion des malades, des rendez-vous, des consultations, des prédictions de maladies, ainsi qu'un suivi des revenus du cabinet. Le projet permet aussi de générer des factures et des rapports médicaux, tout en offrant un tableau de bord pour suivre l'évolution des rendez-vous, les prédictions, et bien plus.

## Fonctionnalités principales ⚙️
- **CRUD des Maladies** : Permet d'ajouter, modifier, supprimer et afficher les maladies.
- **Gestion des Rendez-vous** : Création et validation des rendez-vous.
- **Consultation Médicale** : Lorsqu'un rendez-vous est validé, il devient une consultation et génère une facture et un rapport médical.
- **Prédictions de Maladies** : Prédictions basées sur des critères médicaux pour le diabète et la classification des maladies.
- **Tableau de bord** : Un dashboard permettant de suivre :
  - L'évolution des rendez-vous
  - Les revenus du cabinet
  - L'historique des prédictions
  - Les patients ayant payé le plus

## Prérequis 🔧
Avant de commencer, assurez-vous d'avoir installé les éléments suivants :
- Python 3.x
- Django 5.x
- PostgreSQL (si vous utilisez PostgreSQL comme base de données)
- Pip (pour installer les dépendances)

## Installation 📦
1. Clonez le dépôt GitHub :
    ```bash
    git clone https://github.com/votre_utilisateur/Health-App.git
    cd Health-App
    ```
2. Créez un environnement virtuel et activez-le :
    ```bash
    python -m venv env
    source env/bin/activate  # Sur Linux/Mac
    env\Scriptsctivate  # Sur Windows
    ```
3. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```
4. Appliquez les migrations de base de données :
    ```bash
    python manage.py migrate
    ```
5. Démarrez le serveur de développement :
    ```bash
    python manage.py runserver
    ```

## Structure du projet 📁
Le projet est organisé comme suit :
```
Health-App/
│
├── manage.py                  # Script principal pour exécuter le projet
├── Health_App/                 # Dossier contenant les fichiers de l'application
│   ├── models.py              # Modèles de données
│   ├── views.py               # Logique des vues
│   ├── templates/             # Templates HTML
│   └── static/                # Fichiers statiques (CSS, JS, images)
│
└── requirements.txt           # Liste des dépendances
```

## Utilisation 💡
1. **Se connecter comme Médecin** : Seuls les médecins peuvent ajouter des secrétaires et accéder aux prédictions de maladies.
2. **Ajouter des Secrétaires** : Les secrétaires peuvent être ajoutés par un médecin via le formulaire d'ajout.
3. **Gérer les Maladies** : Vous pouvez ajouter des maladies avec une description, des symptômes et des traitements.
4. **Ajouter des Rendez-vous** : Le médecin peut valider des rendez-vous pour les transformer en consultations.
5. **Génération de Factures et Rapports** : Après chaque consultation, une facture et un rapport médical sont générés.
6. **Consulter le Tableau de Bord** : Le dashboard affiche les statistiques du cabinet médical (évolution des rendez-vous, revenus, etc.).

## Captures d'écran 📸
Voici quelques captures d'écran de l'application pour mieux visualiser son fonctionnement :

- **Page d'Accueil** :
  ![Page d'Accueil](./screenshot/homepage.png)
  
- **Gestion des Maladies** :
  ![Gestion des Maladies](./screenshot/diseases_management.png)

- **Tableau de Bord** :
  ![Tableau de Bord](./screenshot/dashboard.png)

- **Page de Consultation** :
  ![Page de Consultation](./screenshot/consultation_page.png)

## Contribuer 🤝
1. Fork ce repository.
2. Créez une branche pour vos changements : `git checkout -b feature/nom_de_feature`.
3. Commitez vos changements : `git commit -m 'Ajout de feature'`.
4. Poussez vos changements : `git push origin feature/nom_de_feature`.
5. Soumettez une pull request.

## Auteurs 👩‍💻👨‍💻
- **Maroua** : Développement et conception du projet.
  
## Licence 📄
Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.
