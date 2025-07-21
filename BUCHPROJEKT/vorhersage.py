# vorhersage.py
from transformers import AuthorRatingMapper  # ganz oben importieren
import joblib
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import recall_score, confusion_matrix, ConfusionMatrixDisplay


def show():

    st.subheader("🎬 Buchverfilmungs-Vorhersage für die neuen Bücher 2021–2025")

    try:
        df_pred = pd.read_csv("new_books_2024.csv", sep=",", encoding="utf-8")
        df_pred.columns = df_pred.columns.str.strip()
    except FileNotFoundError:
        st.error("❌ Datei 'new_books_2024.csv' wurde nicht gefunden.")
        return

    try:
        df_ana = pd.read_csv("book_data_clean.csv", sep=";", encoding="utf-8")
        df_ana.columns = df_ana.columns.str.strip()
    except FileNotFoundError:
        st.error("❌ Datei 'book_data_clean.csv' wurde nicht gefunden.")
        return

    try:
        pipeline = joblib.load("logistic_pipeline.pkl")
    except FileNotFoundError:
        st.error("❌ Modell-Datei 'logistic_pipeline.pkl' nicht gefunden.")
        return

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
        "📚 Wähle ein Buch", buecher_von_autor["Book_Name"].unique()
    )
    buchdaten = buecher_von_autor[buecher_von_autor["Book_Name"] == buch].iloc[0:1]

    st.write("### 📖 Details zum ausgewählten Buch:")
    st.write(buchdaten)

    if not buchdaten.empty:
        X_new = buchdaten.drop(columns=["Book_Name"])
        proba = pipeline.predict_proba(X_new)[:, 1][0]
        pred = "Ja" if proba >= threshold_slider else "Nein"

    st.write(f"**📊 Wahrscheinlichkeit für Verfilmung:** {proba:.2f}")

    if pred == "Ja":
        st.success(
            f"🎬 **Erfolg!** Dieses Buch wird voraussichtlich verfilmt! Salute! 🥂🍿\n\n"
            f"_(Schwellenwert: {threshold_slider:.2f})_"
        )
        st.balloons()
    else:
        st.warning(
            f"📘 **Aktuell keine Verfilmung wahrscheinlich.** Vielleicht später?\n\n"
            f"_(Schwellenwert: {threshold_slider:.2f})_"
        )

    # === Modell-Performance auf historischen Daten ===
    if "Adapted_to_Film" in df_ana.columns:
        X_hist = df_ana.drop(columns=["Book_Name", "Adapted_to_Film"], errors="ignore")
        y_hist = df_ana["Adapted_to_Film"]

        y_proba_hist = pipeline.predict_proba(X_hist)[:, 1]
        y_pred_hist = (y_proba_hist >= threshold_slider).astype(int)

        recall = recall_score(y_hist, y_pred_hist)
        cm = confusion_matrix(y_hist, y_pred_hist)

        st.write(f"### 📈 Modell-Performance bei Schwellenwert {threshold_slider:.2f}")
        st.write(f"**Recall:** {recall:.2f} (Anteil korrekt erkannter Verfilmungen)")

        fig, ax = plt.subplots(figsize=(0.75, 0.75))
        disp = ConfusionMatrixDisplay(cm, display_labels=["Nicht verfilmt", "Verfilmt"])
        disp.plot(ax=ax, cmap=plt.cm.RdYlGn, colorbar=False)

        ax.set_title("Confusion Matrix", fontsize=6)
        ax.set_xlabel("Vorhergesagte Klasse", fontsize=5)
        ax.set_ylabel("Tatsächliche Klasse", fontsize=5)
        ax.tick_params(axis="both", labelsize=4)
        for text in ax.texts:
            text.set_fontsize(4)

        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("⚠️ Spalte 'Adapted_to_Film' fehlt in den historischen Daten.")
