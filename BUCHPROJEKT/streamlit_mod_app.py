from transformers import AuthorRatingMapper
import streamlit as st
import Verfilmungsprognose
import Wirtschaftanalyse
import empfehlung_Lena_skelett
import start

st.set_page_config(page_title="Book Market", layout="wide")

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
    empfehlung_Lena_skelett.show()
