import pandas as pd
import streamlit as st
import joblib  # Nicht vergessen zu importieren!
from sklearn.base import BaseEstimator, TransformerMixin


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


# Titel der App
st.title("📚 Buchverfilmungs-Vorhersage für neue Bücher aus 2024")

# CSV-Datei hochladen
uploaded_file = st.file_uploader(
    "📁 Lade eine CSV-Datei mit neuen Büchern hoch", type="csv"
)

# Wenn eine Datei hochgeladen wurde:
if uploaded_file is not None:
    # Lade die Datei direkt aus dem Upload, nicht aus dem Pfad
    new_books_df = pd.read_csv(uploaded_file)

    # Modell laden
    model = joblib.load("logistic_pipeline.pkl")

    # Vorhersagefunktion
    def vorhersage(df_neu, schwelle=0.4):
        probs = model.predict_proba(df_neu)[:, 1]
        pred = (probs >= schwelle).astype(int)
        df_neu["Verfilmung?"] = ["Ja" if p == 1 else "Nein" for p in pred]
        df_neu["Wahrscheinlichkeit (%)"] = (probs * 100).round(1)
        return df_neu

    # Button für Vorhersage
    if st.button("📊 Vorhersage anzeigen"):
        result_df = vorhersage(new_books_df)
        st.write("### 📈 Vorhersageergebnisse:")
        st.dataframe(result_df)
