# Wirtschaftanalyse.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import os
from scipy.stats import pearsonr


def show():
    st.subheader("📊 Wirtschaftanalyse der Buchdaten")

    try:
        df = pd.read_csv("book_data_clean.csv", sep=";", encoding="utf-8")
        df.columns = df.columns.str.strip()

        # publishing year korrigieren und als ganze Zahl anzeigen
        if "Publishing_Year" in df.columns:
            df["Publishing_Year"] = pd.to_numeric(
                df["Publishing_Year"], errors="coerce"
            ).astype("Int64")

    except FileNotFoundError:
        st.error("❌ Datei 'book_data_clean.csv' wurde nicht gefunden.")
        return

    # Beispiel: Basisstatistiken
    st.write("### 📈 Basisinformationen")
    st.dataframe(df.style.format({"Publishing_Year": "{:.0f}"}))

    # 📉 Regressionsanalyse: Bewertung vs. Bruttoumsatz (gesamt)
    st.write("### 📉 Regressionsanalyse: Bewertung vs. Bruttoumsatz (Gesamt)")

    df["Average_Rating"] = pd.to_numeric(df["Average_Rating"], errors="coerce")
    df["Gross_Sales_EUR"] = pd.to_numeric(df["Gross_Sales_EUR"], errors="coerce")
    df_corr = df.dropna(subset=["Average_Rating", "Gross_Sales_EUR"])

    if not df_corr.empty:
        correlation, p_value = pearsonr(
            df_corr["Average_Rating"], df_corr["Gross_Sales_EUR"]
        )
        st.write(f"**Korrelationskoeffizient:** {correlation:.3f}")
        st.write(
            f"**p-Wert:** {p_value:.4f} ({'signifikant' if p_value < 0.05 else 'nicht signifikant'})"
        )

        X = sm.add_constant(df_corr["Average_Rating"])
        y = df_corr["Gross_Sales_EUR"]
        model = sm.OLS(y, X).fit()

        st.write("**Regressionsmodell:**")
        st.write(
            f"Gross Sales = {model.params[0]:.2e} + {model.params[1]:.2e} * Average Rating"
        )
        st.write(f"**R²-Wert:** {model.rsquared:.3f}")

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.regplot(
            x="Average_Rating",
            y="Gross_Sales_EUR",
            data=df_corr,
            ci=None,
            ax=ax,
            line_kws={"color": "red"},
        )
        ax.set_title(
            f"Bruttoumsatz vs. Bewertung\nKorrelationskoeffizient: {correlation:.2f}"
        )
        ax.set_xlabel("Durchschnittliche Bewertung")
        ax.set_ylabel("Bruttoumsatz (EUR)")
        ax.grid(True)
        st.pyplot(fig)

        st.markdown(
            """
        #### 📌 Zusammenfassung
        - Es besteht ein **statistisch signifikanter**, aber **schwacher positiver Zusammenhang** zwischen Bewertung und Umsatz.
        - Der **R²-Wert** zeigt, dass nur ein sehr kleiner Anteil der Umsatzvarianz durch die Bewertung erklärt wird.
        - Weitere Einflussfaktoren sollten untersucht werden (z. B. Genre, Bekanntheit, Marketing).
        """
        )

    else:
        st.warning("Nicht genügend Daten für Regressionsanalyse verfügbar.")

    # 🔍 Regressionsanalyse nach Genre
    st.write("### 🎭 Regressionsanalyse nach Genre")

    df_clean = df.dropna(subset=["Average_Rating", "Gross_Sales_EUR", "Genre"])
    genres = df_clean["Genre"].unique()

    for genre in genres:
        genre_df = df_clean[df_clean["Genre"] == genre]
        if len(genre_df) < 10:
            continue

        X = sm.add_constant(genre_df["Average_Rating"])
        y = genre_df["Gross_Sales_EUR"]
        model = sm.OLS(y, X).fit()
        corr = genre_df["Average_Rating"].corr(genre_df["Gross_Sales_EUR"])

        st.write(f"#### 📚 {genre}")
        st.write(f"- Korrelationskoeffizient: **{corr:.3f}**")
        st.write(f"- p-Wert: **{model.pvalues[1]:.4f}**")

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.regplot(
            x="Average_Rating", y="Gross_Sales_EUR", data=genre_df, ci=None, ax=ax
        )
        ax.set_title(f"{genre}\nKorrelation: {corr:.2f}")
        ax.set_xlabel("Durchschnittliche Bewertung")
        ax.set_ylabel("Bruttoumsatz (EUR)")
        st.pyplot(fig)
