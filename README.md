# Projet de Tests Automatisés E-commerce

Ce projet contient une suite de tests automatisés pour une application web e-commerce, développée avec Selenium et Pytest.

## Structure du Projet

```
.
├── config/                 # Configuration du projet
│   ├── __init__.py        # Initialisation et configuration
│   └── config.py          # Paramètres de configuration
├── data/                  # Données de test
├── tests/                 # Suite de tests
│   ├── test_test_add_product.py
│   ├── test_test_add_category.py
│   ├── test_test_orders.py
│   ├── test_test_shopping.py
│   └── ...               # Autres fichiers de test
├── utils/                 # Utilitaires et fonctions communes
│   └── __init__.py
├── requirements.txt       # Dépendances du projet
└── .gitignore            # Fichiers ignorés par Git
```

## Fonctionnalités Testées

Le projet inclut des tests pour les fonctionnalités suivantes :

- **Gestion des Produits**

  - Ajout de produits
  - Édition de produits
  - Suppression de produits
  - Navigation dans la liste des produits

- **Gestion des Catégories**

  - Ajout de catégories
  - Édition de catégories
  - Navigation dans les catégories

- **Gestion des Commandes**

  - Suivi des commandes
  - Statut des commandes
  - Commandes complétées

- **Interface Administrateur**

  - Authentification admin
  - Navigation dans le tableau de bord
  - Statistiques
  - Barre de navigation admin

- **Shopping**
  - Processus d'achat
  - Navigation client

## Prérequis

- Python 3.x
- pip (gestionnaire de paquets Python)

## Installation

1. Cloner le repository :

```bash
git clone [URL_DU_REPO]
cd [NOM_DU_PROJET]
```

2. Créer et activer un environnement virtuel :

```bash
python -m venv .venv
source .venv/bin/activate  # Sur Unix/macOS
# ou
.venv\Scripts\activate     # Sur Windows
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Dépendances Principales

- selenium==4.18.1
- pytest==8.4.0
- webdriver-manager==4.0.1

## Exécution des Tests

Pour exécuter tous les tests :

```bash
pytest
```

Pour exécuter un test spécifique :

```bash
pytest tests/test_test_add_product.py
```

Pour exécuter les tests avec plus de détails :

```bash
pytest -v
```

## Structure des Tests

Les tests sont organisés par fonctionnalité et suivent une nomenclature cohérente :

- `test_test_*.py` : Tests des fonctionnalités principales
- Chaque fichier de test contient des classes de test avec des méthodes de test individuelles

## Contribution

1. Créer une branche pour votre fonctionnalité
2. Ajouter vos tests
3. S'assurer que tous les tests passent
4. Soumettre une pull request

## Notes

- Les tests utilisent Selenium WebDriver pour l'automatisation des tests
- Le projet inclut une configuration pour gérer les différents environnements de test
- Les tests sont conçus pour être indépendants et reproductibles


##install : pip install pytest‑html 
      commande :
      1-  python –m pytest ––html=report.html ––self-contained-html

      ## generer le rapport TP 

      2- python -m pytest tests/test_test_add_product.py tests/test_test_add_category.py tests/test_test_add_category_form.py tests/test_test_edit_product.py tests/test_test_edit_category.py tests/test_test_delete_product.py tests/test_test_delete_category.py tests/test_test_navbar_admin.py tests/test_test_shopping.py --html=report.html --self-contained-html


## command test rapport Allure :
      Installe :  pip install allure-pytest pytest-selenium
                  brew install allure   # ou npm install -g allure-commandline

      commande pour generer le rapport TP: 
      
      Category: 
                  pytest tests/func/category/test_test_add_category.py tests/func/category/test_test_add_category_form.py tests/func/category/test_test_edit_category.py tests/func/category/test_test_delete_category.py --alluredir=allure-results

      Product:   
                  pytest tests/func/product/test_test_add_product.py tests/func/product/test_test_edit_product.py tests/func/product/test_test_delete_product.py --alluredir=allure-results

      Shooping: pytest tests/func/shooping --alluredir=allure-results


      Génère les résultats : pytest tests/ --alluredir=allure-results

      Affiche le rapport : allure serve allure-results

      Nettoyer les anciens résultats Allure: rm -rf allure-results

