# FOMEMO Malaria Diagnosis App

Application Streamlit d'aide au dépistage du paludisme à partir d'images de cellules sanguines.
Un CNN (Keras, `models/malaria_model.h5`) classe chaque cellule en **parasitée** ou **saine**.

> ⚠️ Outil pédagogique : il ne remplace en aucun cas un diagnostic médical.

## Lancer en local

```bash
python3.10 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run main.py
```

## Structure

| Chemin | Rôle |
|---|---|
| `main.py` | Accueil : connexion / inscription |
| `pages/patient.py` | Espace patient : upload d'image et analyse |
| `pages/admin.py` | Espace admin : statistiques et export |
| `utils/` | Authentification et base de données |
| `models/` | Modèle CNN entraîné |

## Auteurs

FOGUE, METAFE, MOUSSINGA — projet tutoré 2025.
