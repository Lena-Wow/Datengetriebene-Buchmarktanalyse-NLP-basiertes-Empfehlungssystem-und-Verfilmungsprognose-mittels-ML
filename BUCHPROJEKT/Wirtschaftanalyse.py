import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import pearsonr


def wirtschaftanalyse():
    st.markdown("### 📊 Wirtschaftsanalyse der Buchdaten")

    try:
        df = pd.read_csv("book_data_clean.csv", sep=";", encoding="utf-8")
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #  FORMATIERUNG: Werte  runden ( floats)
        df["Average_Rating"] = df["Average_Rating"].round(2)
        df["Gross_Sales_EUR"] = df["Gross_Sales_EUR"].round(2)
        df["Publisher_Revenue_EUR"] = df["Publisher_Revenue_EUR"].round(2)

        #  FORMATIERUNG: Ganze Zahlen korrekt setzen
        df["Rating_Count"] = df["Rating_Count"].astype("Int64")
        df["Publishing_Year"] = df["Publishing_Year"].astype("Int64")
        df["Adapted_to_Film"] = df["Adapted_to_Film"].astype("Int64")

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        df.columns = df.columns.str.strip()

        # publishing year korrigieren und als ganze Zahl anzeigen
        # if "Publishing_Year" in df.columns:
        # df["Publishing_Year"] = pd.to_numeric(
        # df["Publishing_Year"], errors="coerce"s
        # ).astype("Int64")

    except FileNotFoundError:
        st.error("❌ Datei 'book_data_clean.csv' wurde nicht gefunden.")
        return

    st.markdown("#### 📈 Basisinformationen")
    st.dataframe(df)

    # --------------------------------------------
    # Zusätzliche Visualisierung: Bewertung vs. Umsatz farbcodiert nach Author_Rating
    st.markdown("####  Bewertung vs. Umsatz mit Farbcodierung nach Autor-Rating")

    df_viz = df[df["Publishing_Year"] >= 2005].copy()
    author_order = ["Novice", "Intermediate", "Excellent", "Famous"]
    df_viz["Author_Rating"] = pd.Categorical(
        df_viz["Author_Rating"], categories=author_order, ordered=True
    )

    fig, ax = plt.subplots(figsize=(2.5, 1.5))
    scatter = sns.scatterplot(
        data=df_viz,
        x="Average_Rating",
        y="Gross_Sales_EUR",
        hue="Author_Rating",
        palette="viridis",
        hue_order=author_order,
        alpha=0.7,
        edgecolor=None,


        s=3,

        # s=1,

        ax=ax
    )
    ax.set_yscale('log')
    ax.set_xlabel("Durchschnittliche Bewertung", fontsize=5)
    ax.set_ylabel("Bruttoumsatz (EUR)", fontsize=5)
   
    #  ax.set_title(
        # 'Bewertung vs. Umsatz (Farbcodierung: Autor-Rating)')



        # ax=ax,
    
    # ax.set_yscale("log")
    # ax.set_xlabel("Durchschnittliche Bewertung", frontsize=5)
    # ax.set_ylabel("Bruttoumsatz (EUR)", frontsize=5)

    # ax.set_title("Bewertung vs. Umsatz (Farbcodierung: Autor-Rating)")



    ax.grid(True)



    handles, labels = scatter.get_legend_handles_labels()




    ax.legend(handles=handles[1:], labels=labels[1:], title='Author Rating', loc='center left',
    bbox_to_anchor=(1.7, 0.5) )

    # ax.legend(handles=handles[1:], labels=labels[1:], title="Author Rating")

    st.pyplot(fig)

    st.markdown("#### 📉 Regressionsanalyse: Bewertung vs. Bruttoumsatz (Gesamt)")
    df_corr = df.dropna(subset=["Average_Rating", "Gross_Sales_EUR"])
    df_corr = df_corr[df_corr["Publishing_Year"] >= 2005]

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

        st.write(
            f" Interpretation: Die Analyse zeigt keinen statistisch gesicherten Zusammenhang "
            f"(p = {p_value:.4f}), der Korrelationswert ist sehr schwach (r = {correlation:.3f}), "
            f"und das Modell erklärt mit R² = {model.rsquared:.3f} nur einen sehr kleinen Teil der Umsatzunterschiede."
        )

        fig, ax = plt.subplots(figsize=(2.0, 1.0))
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
        ####  Zusammenfassung
     
        """
        )
    else:
        st.warning("Nicht genügend Daten für Regressionsanalyse verfügbar.")

    st.markdown("####  Regressionsanalyse nach Genre")
    df_clean = df.dropna(subset=["Average_Rating", "Gross_Sales_EUR", "Genre"])
    df_clean = df_clean[df_clean["Publishing_Year"] >= 2005]
    genres = df_clean["Genre"].unique()

    for genre in genres:
        genre_df = df_clean[df_clean["Genre"] == genre]
        if len(genre_df) < 10:
            continue

        X = sm.add_constant(genre_df["Average_Rating"])
        y = genre_df["Gross_Sales_EUR"]
        model = sm.OLS(y, X).fit()
        corr = genre_df["Average_Rating"].corr(genre_df["Gross_Sales_EUR"])

        st.write(f"####  {genre}")
        st.write(f"- Korrelationskoeffizient: **{corr:.3f}**")
        st.write(f"- p-Wert: **{model.pvalues[1]:.4f}**")

        fig, ax = plt.subplots(figsize=(2.8, 1.6))
        sns.regplot(
            x="Average_Rating", y="Gross_Sales_EUR", data=genre_df, ci=None, ax=ax
        )
        ax.set_title(f"{genre}\nKorrelation: {corr:.2f}")
        ax.set_xlabel("Durchschnittliche Bewertung")
        ax.set_ylabel("Bruttoumsatz (EUR)")
        st.pyplot(fig)

    st.markdown("####  Umsatzanalyse nach Genre")

    if "Genre" in df.columns and "Gross_Sales_EUR" in df.columns:
        genre_sales = (
            df.groupby("Genre")["Gross_Sales_EUR"].sum().sort_values(ascending=False)
        )
        genre_sales_df = genre_sales.reset_index()
        genre_sales_df.columns = ["Genre", "Total_Gross_Sales_EUR"]

        st.markdown("####Gesamtumsatz nach Genre")
        st.dataframe(genre_sales_df)

        st.markdown("####Visualisierung der Umsätze")
        fig, ax = plt.subplots()
        ax.barh(genre_sales_df["Genre"], genre_sales_df["Total_Gross_Sales_EUR"])
        ax.invert_yaxis()
        ax.set_xlabel("Gesamtumsatz in EUR")
        ax.set_ylabel("Genre")
        ax.set_title("Buchumsätze nach Genre")
        st.pyplot(fig)
    else:
        st.error("Die Datei muss die Spalten 'Genre' und 'Gross_Sales_EUR' enthalten.")


def show():
    wirtschaftanalyse()
