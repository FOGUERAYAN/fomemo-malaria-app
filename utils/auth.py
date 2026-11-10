"""Gestion de session Streamlit : connexion, déconnexion et gardes de page."""
import hmac
import os

import streamlit as st

from utils.database import verify_user


def admin_invite_code():
    """Code d'invitation requis pour créer un compte admin (secrets Streamlit ou variable d'env)."""
    try:
        code = st.secrets.get("ADMIN_INVITE_CODE")
    except Exception:
        code = None
    return code or os.environ.get("ADMIN_INVITE_CODE")


def check_invite_code(given: str) -> bool:
    expected = admin_invite_code()
    return bool(expected) and hmac.compare_digest(given or "", expected)


def login(name: str, password: str, role: str) -> bool:
    user = verify_user(name, password, role)
    if user is None:
        return False
    st.session_state["user"] = user
    return True


def logout() -> None:
    st.session_state.pop("user", None)


def current_user():
    return st.session_state.get("user")


def require_role(role: str) -> dict:
    """À appeler en haut de chaque page protégée : arrête la page si l'accès n'est pas autorisé."""
    user = current_user()
    if user is None or user["role"] != role:
        st.warning("🔒 Accès refusé : veuillez vous connecter avec le bon rôle.")
        st.page_link("main.py", label="← Retour à la connexion")
        st.stop()
    return user


def sidebar_user_box() -> None:
    user = current_user()
    if user:
        st.sidebar.markdown(f"👤 Connecté : **{user['name']}** ({user['role']})")
        if st.sidebar.button("Se déconnecter"):
            logout()
            st.switch_page("main.py")
