import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuration
st.set_page_config(page_title="FOMEMO - Admin", layout="wide")

from utils.auth import require_role, sidebar_user_box

require_role("admin")
sidebar_user_box()

# En-tête avec logo et titre réduit
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.png", width=80)
with col2:
    st.markdown("<h4 style='margin-top: 20px;'>FOMEMO Malaria Diagnosis App - Admin</h4>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Barre latérale informative
with st.sidebar:
    st.markdown("""
    ## 🔐 Interface Admin

    📊 Visualisez les résultats de diagnostic ici :
    - Filtrez par patient et date
    - Exportez les données en CSV
    """)

    selected_patient = st.selectbox("Filtrer par patient", ["Tous", "Patient A", "Patient B"])
    selected_date = st.date_input("Filtrer par date")
    if st.button("Exporter en CSV"):
        df = pd.DataFrame({
            "Nom": ["Patient A", "Patient B"],
            "Résultat": ["Positif", "Négatif"],
            "Date": ["2025-05-28", "2025-05-27"]
        })
        os.makedirs("data", exist_ok=True)
        df.to_csv("data/export_resultats.csv", index=False)
        st.success("✅ Fichier exporté dans /data/export_resultats.csv")

# Contenu principal
st.markdown("### 📈 Statistiques globales")

data = pd.DataFrame({
    'Résultat': ['Positif', 'Négatif'],
    'Nombre': [32, 68]
})

fig, ax = plt.subplots()
ax.pie(data['Nombre'], labels=data['Résultat'], autopct='%1.1f%%', colors=['#ff4d4d', '#4caf50'])
ax.axis('equal')
st.pyplot(fig)

# Pied de page
st.markdown("""
<br><hr><small style='color: gray;'>Développé avec ❤️ par FOGUE, METAFE, et MOUSSINGA - projet-tutoré 2025</small>
""", unsafe_allow_html=True)
