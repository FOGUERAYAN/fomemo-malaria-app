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

## Comptes

- **Patient** : inscription libre depuis la page d'accueil.
- **Admin** : l'inscription exige un code d'invitation. Définissez-le via un secret Streamlit
  (`.streamlit/secrets.toml` : `ADMIN_INVITE_CODE = "..."`) ou la variable d'environnement `ADMIN_INVITE_CODE`.
  Sans code configuré, aucun compte admin ne peut être créé.
- Les données sont stockées dans une base SQLite locale (`data/fomemo.db`, chemin modifiable via `FOMEMO_DB`),
  mots de passe hachés (PBKDF2-SHA256 + sel).

## Tests

```bash
pip install pytest numpy pillow && pytest
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
