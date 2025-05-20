# 🗂️ Task Management API

## 🇫🇷 Présentation

Ce projet est une API RESTful développée avec **Flask**, permettant la **gestion de tâches utilisateur** (CRUD) avec authentification.  
Chaque utilisateur peut créer, consulter, modifier ou supprimer ses propres tâches.

Fonctionnalités :
- Création de comptes utilisateur
- Authentification et gestion de session avec `Flask-Login`
- Création, lecture, mise à jour et suppression (CRUD) des tâches
- Protection des routes selon l'utilisateur connecté
- Recherche de tâches par nom
- Gestion des erreurs (404, 500)

---

## 🇬🇧 Overview

This project is a RESTful API built with **Flask** for managing user-specific tasks with authentication.  
Each user can create, view, update, or delete only their own tasks.

Features:
- User registration and authentication
- Task CRUD operations
- Per-user access control
- Search tasks by name
- Error handling (404, 500)

---

## 🧰 Technologies utilisées / Technologies used

- Python 3
- Flask
- SQLAlchemy
- Flask-Login
- Flask-Migrate
- Flask-Bcrypt
- SQLite (modifiable via config)
- Alembic (migrations)

---

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/ton-utilisateur/task-management.git
cd task-management
```
### Execution
```bash
python run.py
``
