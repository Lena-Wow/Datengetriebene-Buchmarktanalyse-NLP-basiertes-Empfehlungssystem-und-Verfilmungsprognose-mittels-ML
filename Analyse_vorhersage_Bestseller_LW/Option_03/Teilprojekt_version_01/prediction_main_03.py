import streamlit as st
import pandas as pd
import joblib
from sklearn.base import BaseEstimator, TransformerMixin

st.set_page_config(layout="wide")


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


# Modell laden (einmalig)
pipeline = joblib.load("logistic_pipeline.pkl")

st.title("Buchverfilmungs-Vorhersage für neue Bücher aus 2024")

try:
    df_new_books = pd.read_csv("new_books_2024.csv", sep=",", encoding="utf-8")
except FileNotFoundError:
    st.error("❌ Datei 'neue_buecher_2024.csv' wurde nicht gefunden.")
    st.stop()


df_new_books.columns = df_new_books.columns.str.strip()

selected_book = st.sidebar.selectbox(
    "Wähle ein Buch aus", df_new_books["Book_Name"].unique()
)
book_data = df_new_books[df_new_books["Book_Name"] == selected_book].iloc[0:1]

st.write("### Details zum ausgewählten Buch:")
st.write(book_data)

if not book_data.empty:
    X_new = book_data.drop(columns=["Book_Name"])

    # Vorhersage
    proba = pipeline.predict_proba(X_new)[:, 1][0]
    st.write(f"**Vorhersage Wahrscheinlichkeit für Verfilmung:** {proba:.2f}")

    threshold = 0.4
    pred = "Ja" if proba >= threshold else "Nein"
    st.write(f"**Verfilmung?** {pred} (bei Schwellenwert {threshold})")
