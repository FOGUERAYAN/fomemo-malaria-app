import streamlit as st
from utils.auth import check_invite_code, login
from utils.database import create_user
from utils.ui import footer, header

st.set_page_config(page_title="FOMEMO - Accueil", layout="centered")

header()

# Barre latérale avec informations
with st.sidebar:
    st.markdown("## 🧪 Bienvenue dans l'application FOMEMO")
    st.info("🧑‍⚕️ Choisissez une option pour vous connecter ou vous inscrire selon votre rôle.")

# Options Patient / Admin
st.markdown("### 👤 Choisissez votre rôle")

choix = st.radio("Vous êtes :", ["Patient", "Admin"], horizontal=True)
role = choix.lower()
onglet = st.radio("Action :", ["Se connecter", "S'inscrire"], horizontal=True)

if onglet == "S'inscrire":
    st.markdown(f"#### 📝 Inscription {choix}")
    with st.form(f"inscription_{role}"):
        nom = st.text_input("Nom")
        age = st.number_input("Âge", min_value=0, max_value=120, step=1)
        poids = st.number_input("Poids (kg)", min_value=0.0) if role == "patient" else None
        adresse = st.text_input("Adresse")
        if role == "admin":
            code = st.text_input("Code d'invitation admin", type="password")
        mot_de_passe = st.text_input("Mot de passe (8 caractères minimum)", type="password")
        submit = st.form_submit_button("S'inscrire")
    if submit:
        if role == "admin" and not check_invite_code(code):
            st.error("Code d'invitation admin invalide ou non configuré.")
        else:
            try:
                create_user(nom, mot_de_passe, role, age=int(age), weight=poids, address=adresse)
                st.success("Inscription réussie ✅ Vous pouvez maintenant vous connecter.")
            except ValueError as e:
                st.error(str(e))
else:
    st.markdown(f"#### 🔓 Connexion {choix}")
    with st.form(f"connexion_{role}"):
        nom = st.text_input("Nom")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Se connecter")
    if submit:
        if login(nom, mot_de_passe, role):
            st.switch_page(f"pages/{role}.py")
        else:
            st.error("Nom ou mot de passe incorrect.")

footer()
