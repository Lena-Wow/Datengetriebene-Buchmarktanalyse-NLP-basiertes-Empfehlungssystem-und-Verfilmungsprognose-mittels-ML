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

    # Beispielhafte Auswahl (später vom Modell ersetzt)
    genre = st.selectbox(
        "🎭 Wähle ein Genre",
        ["Fantasy", "Thriller", "Romance", "Science Fiction", "Sachbuch"],
    )
    min_rating = st.slider("⭐ Minimale Bewertung", 0.0, 5.0, 3.5, 0.1)

    st.write(
        f"🔎 Suche nach Büchern im Genre **{genre}** mit Bewertung ab **{min_rating}** ..."
    )

    # Placeholder für empfohlene Bücher (hier: Dummy-Daten)
    recommended_books = pd.DataFrame(
        {
            "Titel": ["(Platzhalter 1)", "(Platzhalter 2)", "(Platzhalter 3)"],
            "Autor": ["Autor A", "Autor B", "Autor C"],
            "Bewertung": [4.2, 4.0, 3.9],
            "Genre": [genre] * 3,
        }
    )

    st.write("### 📘 Empfehlungen:")
    st.dataframe(recommended_books)

    st.info(
        "Das Empfehlungssystem wird bald mit echten Daten und Machine Learning ergänzt!"
    )
