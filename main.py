import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="FOMEMO - Accueil", layout="centered")

# Logo en haut à gauche + titre plus petit
col1, col2 = st.columns([1, 6])
with col1:
    st.image("assets/logo.png", width=90)
with col2:
    st.markdown("<h4 style='margin-top:20px;'>FOMEMO Malaria Diagnosis App</h4>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Barre latérale avec informations
with st.sidebar:
    st.markdown("## 🧪 Bienvenue dans l'application FOMEMO")
    st.info("🧑‍⚕️ Choisissez une option pour vous connecter ou vous inscrire selon votre rôle.")

# Options Patient / Admin
st.markdown("### 👤 Choisissez votre rôle")

choix = st.radio("Vous êtes :", ["Patient", "Admin"], horizontal=True)

# Zone principale pour les formulaires
if choix == "Patient":
    onglet = st.radio("Action :", ["S'inscrire", "Se connecter"], horizontal=True)

    if onglet == "S'inscrire":
        st.markdown("#### 📝 Inscription Patient")
        with st.form("inscription_patient"):
            nom = st.text_input("Nom")
            age = st.number_input("Âge", min_value=0, step=1)
            poids = st.number_input("Poids (kg)", min_value=0.0)
            adresse = st.text_input("Adresse")
            mot_de_passe = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("S'inscrire")
            if submit:
                # Ici tu peux ajouter une vraie logique d'enregistrement
                st.success("Inscription réussie ✅")

    if onglet == "Se connecter":
        st.markdown("#### 🔓 Connexion Patient")
        with st.form("connexion_patient"):
            nom = st.text_input("Nom")
            mot_de_passe = st.text_input("Mot de passe", type="password")
            login = st.form_submit_button("Se connecter")
            if login:
                if nom and mot_de_passe:
                    # Simule une authentification réussie
                    st.session_state["auth_patient"] = True
                    st.success("Connexion réussie ✅")
                    st.switch_page("pages/patient.py")
                else:
                    st.error("Veuillez remplir tous les champs")

elif choix == "Admin":
    onglet = st.radio("Action :", ["S'inscrire", "Se connecter"], horizontal=True)

    if onglet == "S'inscrire":
        st.markdown("#### 📝 Inscription Admin")
        with st.form("inscription_admin"):
            nom = st.text_input("Nom")
            age = st.number_input("Âge", min_value=0, step=1)
            adresse = st.text_input("Adresse")
            admin_id = st.text_input("ID Admin")
            mot_de_passe = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("S'inscrire")
            if submit:
                st.success("Inscription réussie ✅")

    if onglet == "Se connecter":
        st.markdown("#### 🔓 Connexion Admin")
        with st.form("connexion_admin"):
            nom = st.text_input("Nom")
            mot_de_passe = st.text_input("Mot de passe", type="password")
            login = st.form_submit_button("Se connecter")
            if login:
                if nom and mot_de_passe:
                    st.session_state["auth_admin"] = True
                    st.success("Connexion réussie ✅")
                    st.switch_page("pages/admin.py")
                else:
                    st.error("Veuillez remplir tous les champs")

# Pied de page
st.markdown("""
<br><hr><small style='color: gray;'>Développé avec ❤️ par FOGUE, METAFE, et MOUSSINGA - projet-tutoré 2025</small>
""", unsafe_allow_html=True)
