import streamlit as st
import pandas as pd
import joblib
from sklearn.base import BaseEstimator, TransformerMixin
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.api.types import CategoricalDtype
from sklearn.metrics import recall_score, confusion_matrix, ConfusionMatrixDisplay

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
###########################################################################################

if page == "🔮 Vorhersage":

    st.subheader("🎬 Buchverfilmungs-Vorhersage für die neue Bücher aus 2021-2025")

    threshold_slider = st.sidebar.slider(
        "🔧 Schwellenwert für Vorhersage",
        0.0,
        1.0,
        0.4,
        0.01,
        help="Ab welcher Wahrscheinlichkeit das Modell eine Verfilmung vorhersagt.",
    )

    autor = st.sidebar.selectbox("👤 Wähle einen Autor", df_pred["Author"].unique())
    buecher_von_autor = df_pred[df_pred["Author"] == autor]
    buch = st.sidebar.selectbox(
        "📚 Wähle sein Buch", buecher_von_autor["Book_Name"].unique()
    )
    buchdaten = buecher_von_autor[buecher_von_autor["Book_Name"] == buch].iloc[0:1]

    st.write("### 📖 Details zum ausgewählten Buch:")
    st.write(buchdaten)

    if not buchdaten.empty:
        # AuthorRatingMapper ist im pipeline integriert, hier nicht extra anwenden
        X_new = buchdaten.drop(columns=["Book_Name"])
        proba = pipeline.predict_proba(X_new)[:, 1][0]
        pred = "Ja" if proba >= threshold_slider else "Nein"

        st.write(f"**📊 Wahrscheinlichkeit für Verfilmung:** {proba:.2f}")
        st.write(
            f"**🎥 Verfilmung?** {pred} (bei Schwellenwert {threshold_slider:.2f})"
        )

    # === Anzeige Modellmetriken basierend auf historischen Daten ===
    if "Adapted_to_Film" in df_ana.columns:
        X_hist = df_ana.drop(columns=["Book_Name", "Adapted_to_Film"], errors="ignore")
        y_hist = df_ana["Adapted_to_Film"]

        # Vorhersagen auf historischen Daten mit gewähltem Schwellenwert
        y_proba_hist = pipeline.predict_proba(X_hist)[:, 1]
        y_pred_hist = (y_proba_hist >= threshold_slider).astype(int)

        recall = recall_score(y_hist, y_pred_hist)
        cm = confusion_matrix(y_hist, y_pred_hist)

        st.write(f"### 📈 Modell-Performance bei Schwellenwert {threshold_slider:.2f}")
        st.write(f"**Recall:** {recall:.2f} (Anteil korrekt erkannter Verfilmungen)")
        st.markdown(
            """
        **Erklärung:**  
        - **Recall** zeigt, wie viele der tatsächlich verfilmten Bücher korrekt erkannt wurden.  
        - Die **Confusion Matrix** zeigt die Verteilung der Vorhersagen:  
          - Oben links: korrekt als nicht verfilmt erkannt  
          - Unten rechts: korrekt als verfilmt erkannt  
          - Oben rechts: fälschlich als verfilmt vorhergesagt  
          - Unten links: fälschlich als nicht verfilmt vorhergesagt
        """
        )
        fig, ax = plt.subplots(figsize=(0.75, 0.75))

        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm, display_labels=["Nicht verfilmt", "Verfilmt"]
        )
        disp.plot(ax=ax, cmap=plt.cm.RdYlGn, colorbar=False)

        # Achsentitel klein setzen
        ax.set_title("Confusion Matrix", fontsize=6)
        ax.set_xlabel("Vorhergesagte Klasse", fontsize=5)
        ax.set_ylabel("Tatsächliche Klasse", fontsize=5)

        # Tick-Schriftgröße verkleinern
        ax.tick_params(axis="both", labelsize=4)

        # Zahlen in der Matrix verkleinern
        for text in ax.texts:
            text.set_fontsize(4)

        plt.tight_layout()
        st.pyplot(fig)

    else:
        st.warning(
            "⚠️ Für Modellmetriken wird die Spalte 'Adapted_to_Film' in historischen Daten benötigt."
        )

###########################################################################################
elif page == "📊 Analyse":
    st.title("📊 Analyse der Bücher (book_data_clean.csv)")

    st.write("### 📚 Gesamtdaten:")
    st.dataframe(df_ana)

    st.write("### 🏷️ Verteilung der Genres:")
    if "Genre" in df_ana.columns:
        genre_counts = df_ana["Genre"].value_counts()
        st.bar_chart(genre_counts)

    if all(
        col in df_ana.columns
        for col in ["Average_Rating", "Gross_Sales_EUR", "Author_Rating"]
    ):
        st.write("### Bewertung vs. Verkäufe, gefärbt nach Autor Rating")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(
            data=df_ana,
            x="Average_Rating",
            y="Gross_Sales_EUR",
            hue="Author_Rating",
            palette="coolwarm",
            alpha=0.7,
            ax=ax,
        )
        ax.set_yscale("log")
        ax.set_title("Bewertung vs. Verkäufe, gefärbt nach Autor Rating")
        st.pyplot(fig)

    if "Author_Rating" in df_ana.columns:
        rating_order = ["Novice", "Intermediate", "Famous", "Excellent"]
        cat_type = CategoricalDtype(categories=rating_order, ordered=True)
        df_ana["Author_Rating"] = df_ana["Author_Rating"].astype(cat_type)

        st.write("### 🌟 Verteilung der Autor-Ratings")
        rating_counts = df_ana["Author_Rating"].value_counts().reindex(rating_order)
        st.bar_chart(rating_counts)

        st.write("### 📈 Durchschnittliche Buchbewertung nach Autor-Rating")
        if "Average_Rating" in df_ana.columns:
            avg_rating = (
                df_ana.groupby("Author_Rating")["Average_Rating"]
                .mean()
                .reindex(rating_order)
            )
            st.line_chart(avg_rating)

        st.write("### 💰 Durchschnittlicher Bruttoumsatz nach Autor-Rating")
        if "Gross_Sales_EUR" in df_ana.columns:
            avg_sales = (
                df_ana.groupby("Author_Rating")["Gross_Sales_EUR"]
                .mean()
                .reindex(rating_order)
            )
            st.bar_chart(avg_sales)

elif page == "📚 Buchempfehlung":
    st.title("📚 Buchempfehlung (Platzhalter)")

    st.write(
        "Diese Seite wird künftig Buchempfehlungen auf Basis ähnlicher Bücher anzeigen."
    )

    st.write("### 🔍 Vorschau: Neue Bücher 2021-2024")

    if not df_pred.empty:
        st.dataframe(df_pred[["Book_Name", "Author", "Genre"]].head(10))
    else:
        st.warning("Keine neuen Bücher vorhanden.")
