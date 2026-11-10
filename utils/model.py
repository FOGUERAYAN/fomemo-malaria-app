import streamlit as st


@st.cache_resource(show_spinner="Chargement du modèle…")
def load_model(path: str = "models/malaria_model.h5"):
    """Charge le modèle une seule fois par processus (et non à chaque interaction)."""
    import tensorflow as tf

    return tf.keras.models.load_model(path)
