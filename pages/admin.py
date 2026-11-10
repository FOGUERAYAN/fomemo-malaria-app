import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Configuration
st.set_page_config(page_title="FOMEMO - Admin", layout="wide")

from utils.auth import require_role, sidebar_user_box
from utils.database import list_analyses, list_patient_names

require_role("admin")
sidebar_user_box()

# En-tête avec logo et titre réduit
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.png", width=80)
with col2:
    st.markdown("<h4 style='margin-top: 20px;'>FOMEMO Malaria Diagnosis App - Admin</h4>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Filtres
with st.sidebar:
    st.markdown("## 🔐 Interface Admin")
    selected_patient = st.selectbox("Filtrer par patient", ["Tous"] + list_patient_names())
    use_dates = st.checkbox("Filtrer par période")
    date_range = st.date_input("Période", value=(), disabled=not use_dates)

date_from = date_to = None
if use_dates and len(date_range) == 2:
    date_from, date_to = date_range

rows = list_analyses(
    patient_name=None if selected_patient == "Tous" else selected_patient,
    date_from=date_from,
    date_to=date_to,
)
df = pd.DataFrame(rows, columns=["id", "patient", "filename", "probability", "label", "created_at"])

# Statistiques
st.markdown("### 📈 Statistiques")
if df.empty:
    st.info("Aucune analyse pour ces filtres.")
else:
    positives = int((df["label"] == "Parasitée").sum())
    total = len(df)
    c1, c2, c3 = st.columns(3)
    c1.metric("Analyses", total)
    c2.metric("Parasitées", positives)
    c3.metric("Taux de positivité", f"{positives / total:.0%}")

    fig, ax = plt.subplots(figsize=(4, 4))
    counts = df["label"].value_counts()
    colors = {"Parasitée": "#ff4d4d", "Saine": "#4caf50"}
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%", colors=[colors[l] for l in counts.index])
    ax.axis("equal")
    st.pyplot(fig)

    st.markdown("### 📋 Détail des analyses")
    table = df.rename(
        columns={"patient": "Patient", "filename": "Fichier", "probability": "Probabilité", "label": "Résultat", "created_at": "Date"}
    ).drop(columns="id")
    st.dataframe(table, use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ Exporter en CSV",
        table.to_csv(index=False).encode("utf-8"),
        file_name="resultats_fomemo.csv",
        mime="text/csv",
    )

# Pied de page
st.markdown("""
<br><hr><small style='color: gray;'>Développé avec ❤️ par FOGUE, METAFE, et MOUSSINGA - projet-tutoré 2025</small>
""", unsafe_allow_html=True)
