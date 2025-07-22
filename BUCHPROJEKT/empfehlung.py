# empfehlung.py
import streamlit as st
import pandas as pd


def show():
    st.subheader("📚 Intelligente Buchempfehlungen")

    st.write(
        """
        🔍 Hier entsteht bald ein Modell, das basierend auf deinen Vorlieben passende Bücher empfiehlt.

        Du wirst z. B. nach deinem Lieblingsgenre, Autor oder Bewertungsniveau gefragt,
        und das System schlägt dir ähnliche Bücher vor.
        """
    )
