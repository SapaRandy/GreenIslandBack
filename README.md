**README professionnel et complet**

---

````markdown
# 🌱 GreenIsland – Backend & API (Django + Firebase)

Ce dépôt contient le backend du projet **GreenIsland**, une API REST construite avec **Django** permettant la gestion et la communication entre une application mobile Flutter, une carte Arduino (UNO R4), et la base de données Firebase.

## 🎯 Objectif

Ce backend assure :
- La centralisation des données envoyées par les capteurs (température, humidité, niveau d’eau)
- La communication entre l’Arduino et l’application mobile
- La gestion des commandes d’arrosage manuel ou automatique
- Le traitement des identifications de plantes via image
- L’accès aux données botaniques et météorologiques

---

## 🧰 Stack technique

| Élément         | Détail                             |
|----------------|------------------------------------|
| Framework      | Django 4.x                         |
| Langage        | Python 3.11                        |
| Base de données| Firebase Firestore                 |
| Authentification | Firebase Auth                    |
| Déploiement    | Render (automatisé via GitHub)     |
| Fichier secrets| `.env` (inclus dans `.gitignore`)  |

---

## 🔗 Principales routes API

| Méthode | Route                         | Description                                      |
|--------|-------------------------------|--------------------------------------------------|
| `POST` | `/plantid/identify`           | Identification de la plante par image            |
| `GET`  | `/plantid/infos`              | Récupération des infos botaniques d’une plante   |
| `POST` | `/plantid/connect`            | Appairage d’une plante avec un appareil connecté |
| `POST` | `/capteurs/`                  | Réception des données capteurs depuis Arduino    |
| `GET`  | `/meteo/`                     | Récupération météo (basée sur la localisation)   |

> 🔐 L’accès aux routes peut être restreint par des vérifications Firebase Auth si activé.

---

## 🧬 Flux de données

```plaintext
Arduino capteurs => POST vers backend (/capteurs) => Firebase
Flutter app <== backend (infos plante, capteurs, météo)

Utilisateur Flutter => POST /plantid/connect => Associe un device à une plante

Photo plante => POST /plantid/identify => IA => Nom + données stockées
````

---

## 📁 Arborescence des dossiers

```bash
GreenIslandBack/
├── api/
│   ├── views.py          # Logique des routes API
│   ├── urls.py           # Routing
│   ├── serializers.py    # (si utilisé)
│   └── models.py         # Si non Firebase
├── settings.py
├── manage.py
├── .env                  # Clés secrètes (non versionné)
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation locale

```bash
# 1. Cloner le projet
git clone https://github.com/SapaRandy/GreenIslandBack.git
cd GreenIslandBack

# 2. Créer un environnement virtuel
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Ajouter le fichier .env
# Exemple de variables :
# FIREBASE_API_KEY=xxxxxxxx
# DB_URL=xxxxxx
# SECRET_KEY=...

# 5. Lancer le serveur
python manage.py runserver
```

---

## 🚀 Déploiement

Le backend est déployé sur [Render](https://render.com), avec déploiement automatique à chaque `push` via GitHub.

---

## ✅ Tests

* Les endpoints critiques ont été testés manuellement via Postman.
* Des logs sont visibles sur Render.
* Des tests unitaires seront ajoutés (ex: pour le parsing des images, vérification des données envoyées).

---

## 📈 Améliorations futures

* Ajout de tests automatisés
* Documentation Swagger/OpenAPI
* Intégration d’un moteur de règles pour l’arrosage intelligent (basé sur la météo ou des seuils dynamiques)
* Logger d’historique des actions

---

## 👥 Contributeurs

* **Randy SAPA** – Développeur Backend & API
* **Fred Ablefonlin** – Développement Frontend (Flutter)
* **Anthony Selin** – Arduino, capteurs & électronique

---

## 📄 Licence

Projet académique réalisé dans le cadre de H3 HITEMA 2024/2025.
Licence : **MIT** (ou à confirmer selon usage futur)

---

## 📬 Contact

Pour toute question technique, ouvrir une issue sur ce dépôt ou contacter [Randy SAPA](https://github.com/SapaRandy).

```
