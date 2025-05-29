import streamlit as st
from utils.database import create_user, verify_user

def show_login_page():
    st.sidebar.markdown("### 🔑 Connexion / Inscription")
    role = st.sidebar.radio("Choisissez votre rôle :", ["Patient", "Admin"], horizontal=True)
    page = st.sidebar.radio("Page :", ["Connexion", "Inscription"], horizontal=True)

    if page == "Connexion":
        name = st.sidebar.text_input("Nom")
        password = st.sidebar.text_input("Mot de passe", type="password")
        if st.sidebar.button("Se connecter"):
            if verify_user(name, password, role):
                st.session_state.authenticated = True
                st.session_state.role = role
                st.success("Connexion réussie")
            else:
                st.error("Nom ou mot de passe invalide.")
    else:
        name = st.sidebar.text_input("Nom complet")
        age = st.sidebar.number_input("Âge", 0, 120)
        address = st.sidebar.text_input("Adresse")
        password = st.sidebar.text_input("Mot de passe", type="password")
        if st.sidebar.button("S'inscrire"):
            create_user(name, age, address, password, role)
            st.success("Inscription réussie. Veuillez vous connecter.")

def get_role():
    return st.session_state.get("role", None)
