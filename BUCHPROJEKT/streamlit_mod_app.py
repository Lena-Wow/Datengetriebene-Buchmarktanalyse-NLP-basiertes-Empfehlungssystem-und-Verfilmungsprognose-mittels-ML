from transformers import AuthorRatingMapper
import streamlit as st
import vorhersage
import Wirtschaftanalyse
import empfehlung_Lena_skelett
import start

st.set_page_config(page_title="Book Market", layout="wide")

st.sidebar.title("📘 Buchmarkt Toolbox")
st.sidebar.info("Entdecke Buchdaten mit Filtern, Visualisierung & Vorhersage")
page = st.sidebar.radio(
    "Wähle eine Funktion:",
    ["Startseite", "Wirtschaftsanalyse", "Empfehlungssystem", "Vorhersage"],
)

if page == "Startseite":
    start.show()
elif page == "Vorhersage":
    vorhersage.show()
elif page == "Wirtschaftsanalyse":
    Wirtschaftanalyse.show()
elif page == "Empfehlungssystem":
    empfehlung_Lena_skelett.show()
