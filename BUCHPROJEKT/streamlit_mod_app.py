from transformers import AuthorRatingMapper
import streamlit as st
import vorhersage
import Wirtschaftanalyse
import empfehlung_Lena_skelett


st.set_page_config(layout="wide")
st.sidebar.title("📚 Navigation")

page = st.sidebar.radio(
    "Seite auswählen", ("🔮 Vorhersage", "📊 Wirtschaftanalyse", "📚 Empfehlung")
)

st.title("📚 Buchanalyse Projekt")

if page == "🔮 Vorhersage":
    vorhersage.show()
elif page == "📊 Wirtschaftanalyse":
    Wirtschaftanalyse.show()
elif page == "📚 Empfehlung":
    empfehlung_Lena_skelett.show()
