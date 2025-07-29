import streamlit as st  # <- Muss als erster Streamlit-Befehl kommen

st.set_page_config(page_title="Book Market", layout="wide")  # <- Direkt danach

# Jetzt andere Imports
from transformers import AuthorRatingMapper
import Verfilmungsprognose
import Wirtschaftanalyse
import empfehlung
import start

st.sidebar.title("📘 Projekt-Navigation")
st.sidebar.info("📚 Buchmarkt analysieren – Empfehlungen & Filmchance inklusive.")
page = st.sidebar.radio(
    "Wähle eine Funktion:",
    ["Startseite", "Wirtschaftsanalyse", "Empfehlungssystem", "Verfilmungsprognose"],
)

if page == "Startseite":
    start.show()
elif page == "Verfilmungsprognose":
    Verfilmungsprognose.show()
elif page == "Wirtschaftsanalyse":
    Wirtschaftanalyse.show()
elif page == "Empfehlungssystem":
    empfehlung.show()
