import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
import os

# Chargement du modèle
model = tf.keras.models.load_model("models/malaria_model.h5")
input_shape = model.input_shape[1:4]  # (height, width, channels)

# Configuration de la page
st.set_page_config(page_title="FOMEMO - Patient", layout="centered")

# Logo et titre
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.png", width=80)
with col2:
    st.markdown("""
    <h3 style='margin-top: 18px;'>FOMEMO Malaria Diagnosis App</h3>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Espace principal avec formulaire centré
st.title("🔬 Espace Patient - Analyse du paludisme")

# Upload d'image
uploaded_file = st.file_uploader("📤 Importer une image de cellule sanguine", type=["jpg", "jpeg", "png"], label_visibility="visible")

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="🖼️ Image chargée", use_container_width=True)

    # Redimensionner l'image automatiquement selon le modèle
    image_resized = image.resize((input_shape[1], input_shape[0]))
    image_array = np.array(image_resized) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    prediction = model.predict(image_array)
    result = "🦠 Parasitée (Paludisme détecté)" if prediction[0][0] > 0.5 else "✅ Saine (Aucun signe détecté)"

    st.markdown("### 🩺 Résultat de l'analyse :")
    st.success(result)

# Sidebar avec informations ou instructions supplémentaires
with st.sidebar:
    st.markdown("""
    ## ℹ️ Instructions
    1. Importez une image de cellule sanguine.
    2. Le modèle détecte automatiquement le paludisme.
    3. Visualisez le résultat ci-dessus.
    
    Pour des résultats fiables, utilisez une image bien éclairée.
    """)

st.markdown("<br><hr><small style='color: gray;'>Développé avec ❤️ par FOGUE, METAFE, et MOUSSINGA - projet-tutoré 2025</small>", unsafe_allow_html=True)
