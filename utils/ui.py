import streamlit as st

FOOTER = (
    "<br><hr><small style='color: gray;'>Développé avec ❤️ par FOGUE, METAFE, et MOUSSINGA "
    "- projet-tutoré 2025</small>"
)


def header(title: str = "FOMEMO Malaria Diagnosis App", logo_width: int = 80) -> None:
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("assets/logo.png", width=logo_width)
    with col2:
        st.markdown(f"<h4 style='margin-top: 20px;'>{title}</h4>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)


def footer() -> None:
    st.markdown(FOOTER, unsafe_allow_html=True)
