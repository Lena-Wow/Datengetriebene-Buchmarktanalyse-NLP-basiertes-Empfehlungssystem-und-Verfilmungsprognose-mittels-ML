import streamlit as st
import pandas as pd
import joblib
from sklearn.base import BaseEstimator, TransformerMixin

st.set_page_config(layout="wide")


# Transformer-Klasse
class AuthorRatingMapper(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.rating_map = {"Novice": 1, "Intermediate": 2, "Famous": 3, "Excellent": 4}

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        if "Author_Rating" in X.columns:
            X["Author_Rating"] = X["Author_Rating"].map(self.rating_map)
        return X


# --- Daten für Vorhersage ---
try:
    df_pred = pd.read_csv("new_books_2024.csv", sep=",", encoding="utf-8")
    df_pred.columns = df_pred.columns.str.strip()
except FileNotFoundError:
    st.error("❌ Datei 'new_books_2024.csv' wurde nicht gefunden.")
    st.stop()

# --- Daten für Analyse ---
try:
    df_ana = pd.read_csv(
        "book_data_clean.csv", sep=";", encoding="utf-8", on_bad_lines="warn"
    )
    df_ana.columns = df_ana.columns.str.strip()
except FileNotFoundError:
    st.error("❌ Datei 'book_data_clean.csv' wurde nicht gefunden.")
    st.stop()

# Modell laden
pipeline = joblib.load("logistic_pipeline.pkl")

###########################################################################################
# --- Sidebar Navigation ---
st.sidebar.title("📚 Navigation")
page = st.sidebar.radio(
    "Wähle eine Seite:", ("🔮 Vorhersage", "📊 Analyse", "📚 Buchempfehlung")
)

# --- Seite 1: Vorhersage ---
if page == "🔮 Vorhersage":
    st.title("🎬 Buchverfilmungs-Vorhersage für neue Bücher")

    autor = st.sidebar.selectbox("👤 Wähle einen Autor", df_pred["Author"].unique())
    buecher_von_autor = df_pred[df_pred["Author"] == autor]
    buch = st.sidebar.selectbox(
        "📚 Wähle sein Buch", buecher_von_autor["Book_Name"].unique()
    )

    buchdaten = buecher_von_autor[buecher_von_autor["Book_Name"] == buch].iloc[0:1]

    st.write("### 📖 Details zum ausgewählten Buch:")
    st.write(buchdaten)

    if not buchdaten.empty:
        X_new = buchdaten.drop(columns=["Book_Name"])
        proba = pipeline.predict_proba(X_new)[:, 1][0]
        threshold = 0.4
        pred = "Ja" if proba >= threshold else "Nein"

        st.write(f"**📊 Wahrscheinlichkeit für Verfilmung:** {proba:.2f}")
        st.write(f"**🎥 Verfilmung?** {pred} (bei Schwellenwert {threshold})")

# --- Seite 2: Analyse ---
elif page == "📊 Analyse":
    st.title("📊 Analyse der Bücher (book_data_clean.csv)")

    st.write("### 📚 Gesamtdaten:")
    st.dataframe(df_ana)

    st.write("### 🏷️ Verteilung der Genres:")
    if "Genre" in df_ana.columns:
        genre_counts = df_ana["Genre"].value_counts()
        st.bar_chart(genre_counts)


# --- Seite 3: Buchempfehlung ---
elif page == "📚 Buchempfehlung":
    st.title("📚 Buchempfehlung (Platzhalter)")

    st.write(
        "Diese Seite wird künftig Buchempfehlungen auf Basis ähnlicher Bücher anzeigen."
    )

    st.write("### 🔍 Vorschau: Neue Bücher aus 2024")

    if not df_pred.empty:
        st.dataframe(df_pred[["Book_Name", "Author", "Genre"]].head(10))
    else:
        st.warning("Keine neuen Bücher vorhanden.")
