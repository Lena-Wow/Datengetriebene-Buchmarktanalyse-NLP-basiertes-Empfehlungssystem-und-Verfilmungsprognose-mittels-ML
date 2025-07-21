
import streamlit as st
import pandas as pd
import joblib
from sklearn.base import BaseEstimator, TransformerMixin
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.api.types import CategoricalDtype

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

# --- Daten für Vorhersage ---
try:
    df_pred = pd.read_csv("new_books_2024.csv", sep=",", encoding="utf-8")
    df_pred.columns = df_pred.columns.str.strip()
except FileNotFoundError:
    st.error("❌ Datei 'new_books_2024.csv' wurde nicht gefunden.")
    st.stop()

# --- Daten für Analyse ---
try:
    df_ana = pd.read_csv("book_data_clean.csv", sep=";", encoding="utf-8", on_bad_lines="warn")
    df_ana.columns = df_ana.columns.str.strip()
except FileNotFoundError:
    st.error("❌ Datei 'book_data_clean.csv' wurde nicht gefunden.")
    st.stop()

pipeline = joblib.load("logistic_pipeline.pkl")

st.sidebar.title("📚 Navigation")
page = st.sidebar.radio(
    "Wähle eine Seite:", ("🔮 Vorhersage", "📊 Analyse", "📈 Wirtschaftsanalyse", "📚 Buchempfehlung")
)

# --- Seite 1: Vorhersage ---
if page == "🔮 Vorhersage":
    st.title("🎬 Buchverfilmungs-Vorhersage für neue Bücher")
    autor = st.sidebar.selectbox("👤 Wähle einen Autor", df_pred["Author"].unique())
    buecher_von_autor = df_pred[df_pred["Author"] == autor]
    buch = st.sidebar.selectbox("📚 Wähle sein Buch", buecher_von_autor["Book_Name"].unique())
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

    if all(col in df_ana.columns for col in ["Average_Rating", "Gross_Sales_EUR", "Author_Rating"]):
        st.write("### Bewertung vs. Verkäufe, gefärbt nach Autor Rating")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df_ana, x="Average_Rating", y="Gross_Sales_EUR", hue="Author_Rating",
                        palette="coolwarm", alpha=0.7, ax=ax)
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
            avg_rating = df_ana.groupby("Author_Rating")["Average_Rating"].mean().reindex(rating_order)
            st.line_chart(avg_rating)

        st.write("### 💰 Durchschnittlicher Bruttoumsatz nach Autor-Rating")
        if "Gross_Sales_EUR" in df_ana.columns:
            avg_sales = df_ana.groupby("Author_Rating")["Gross_Sales_EUR"].mean().reindex(rating_order)
            st.bar_chart(avg_sales)

# --- Seite 3: Wirtschaftsanalyse ---
elif page == "📈 Wirtschaftsanalyse":
    st.title("📈 Wirtschaftsanalyse der Buchverkäufe")

    if "Genre" in df_ana.columns and "Gross_Sales_EUR" in df_ana.columns:
        st.write("### 💰 Gesamter Umsatz nach Genre")
        sales_by_genre = df_ana.groupby("Genre")["Gross_Sales_EUR"].sum().sort_values(ascending=False)
        st.bar_chart(sales_by_genre)

        st.write("### 📊 Durchschnittlicher Umsatz pro Buch nach Genre")
        avg_sales_by_genre = df_ana.groupby("Genre")["Gross_Sales_EUR"].mean().sort_values(ascending=False)
        st.bar_chart(avg_sales_by_genre)

        st.write("### 📈 Top 10 Genres nach Gesamtumsatz")
        top_genres = sales_by_genre.head(10)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=top_genres.values, y=top_genres.index, ax=ax)
        ax.set_xlabel("Gesamtumsatz (EUR)")
        ax.set_title("Top 10 Genres nach Umsatz")
        st.pyplot(fig)

        st.write("### 🔍 Korrelation zwischen Bewertung und Verkäufen")
        if "Average_Rating" in df_ana.columns:
            correlation = df_ana[["Average_Rating", "Gross_Sales_EUR"]].corr().iloc[0, 1]
            st.write(f"Korrelationskoeffizient (Pearson): **{correlation:.2f}**")
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.regplot(data=df_ana, x="Average_Rating", y="Gross_Sales_EUR",
                        scatter_kws={"alpha": 0.6}, line_kws={"color": "red"}, ax=ax)
            ax.set_yscale("log")
            ax.set_title("Zusammenhang zwischen Bewertung und Bruttoumsatz")
            st.pyplot(fig)

            st.write("### 🧠 Interpretation")
            st.markdown("""
            Die Analyse zeigt, dass es **keinen signifikanten linearen Zusammenhang** zwischen der durchschnittlichen Bewertung eines Buchs und dessen Verkaufszahlen gibt.

            🔹 **Mögliche Gründe:**
            - Stark beworbene Bücher oder bekannte Autoren verkaufen sich auch bei mäßigen Bewertungen gut.
            - Nischenbücher mit hohen Bewertungen erzielen unter Umständen nur geringe Umsätze.
            - Genre, Bekanntheit oder Markttrends beeinflussen den Umsatz stärker als die Bewertung.

            📌 **Fazit:** Ein gut bewertetes Buch ist nicht automatisch ein Bestseller – und umgekehrt.
            """)
        else:
            st.warning("Spalten 'Average_Rating' und/oder 'Gross_Sales_EUR' fehlen für die Korrelationsanalyse.")
    else:
        st.warning("Benötigte Spalten 'Genre' und 'Gross_Sales_EUR' fehlen in den Daten.")

# --- Seite 4: Buchempfehlung ---
elif page == "📚 Buchempfehlung":
    st.title("📚 Buchempfehlung (Platzhalter)")
    st.write("Diese Seite wird künftig Buchempfehlungen auf Basis ähnlicher Bücher anzeigen.")
    st.write("### 🔍 Vorschau: Neue Bücher aus 2024")
    if not df_pred.empty:
        st.dataframe(df_pred[["Book_Name", "Author", "Genre"]].head(10))
    else:
        st.warning("Keine neuen Bücher vorhanden.")
