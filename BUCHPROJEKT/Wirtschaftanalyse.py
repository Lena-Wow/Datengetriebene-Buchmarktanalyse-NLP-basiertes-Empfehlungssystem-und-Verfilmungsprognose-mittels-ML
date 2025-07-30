import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import pearsonr

def wirtschaftanalyse():
    st.title("📚 Wirtschaftsanalyse der Buchdaten")

    try:
        df = pd.read_csv("book_data_clean.csv", sep=";", encoding="utf-8")
        df["Average_Rating"] = df["Average_Rating"].round(2)
        df["Gross_Sales_EUR"] = df["Gross_Sales_EUR"].round(2)
        df["Publisher_Revenue_EUR"] = df["Publisher_Revenue_EUR"].round(2)
        df["Rating_Count"] = df["Rating_Count"].astype("Int64")
        df["Publishing_Year"] = df["Publishing_Year"].astype("Int64")
        df["Adapted_to_Film"] = df["Adapted_to_Film"].astype("Int64")
        df.columns = df.columns.str.strip()
    except FileNotFoundError:
        st.error("❌ Datei 'book_data_clean.csv' wurde nicht gefunden.")
        return

    st.markdown("#### 📈 Basisinformationen")
    st.dataframe(df)

    st.markdown("####  Visualisierung: Bewertung vs. Umsatz farbcodiert nach Autor-Rating")
    df_viz = df[df["Publishing_Year"] >= 2005].copy()

    # Autor-Rating mit fester Kategorie-Reihenfolge
    author_order = ["Novice", "Intermediate", "Excellent", "Famous"]
    df_viz["Author_Rating"] = pd.Categorical(df_viz["Author_Rating"], categories=author_order, ordered=True)

    # Plot
    fig, ax = plt.subplots(figsize=(7, 4))
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
        ax=ax,
    )
    ax.set_yscale("log")
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

    # Legende manuell: alle Kategorien sicher einbauen
    from matplotlib.patches import Patch

    colors = sns.color_palette("viridis", n_colors=4)
    legend_elements = [
        Patch(facecolor=colors[i], label=author_order[i])
        for i in range(len(author_order))
    ]

    handles, labels = scatter.get_legend_handles_labels()

    ax.legend(
        handles=handles[1:],
        labels=labels[1:],
        title="Author Rating",
        loc="center left",
        bbox_to_anchor=(1.7, 0.5),
    )

    # ax.legend(handles=handles[1:], labels=labels[1:], title="Author Rating")

    # Autor-Rating mit fester Kategorie-Reihenfolge
    author_order = ["Novice", "Intermediate", "Excellent", "Famous"]
    df_viz["Author_Rating"] = pd.Categorical(
        df_viz["Author_Rating"], categories=author_order, ordered=True
    )

    # Plot
    fig, ax = plt.subplots(figsize=(7, 4))
    scatter = sns.scatterplot(
        data=df_viz,
        x="Average_Rating",
        y="Gross_Sales_EUR",
        hue="Author_Rating",
        palette="viridis",
        hue_order=author_order,
        alpha=0.7,
        edgecolor=None,
        s=20,
        ax=ax,
    )
    ax.set_yscale("log")
    ax.set_xlabel("Durchschnittliche Bewertung", fontsize=9)
    ax.set_ylabel("Bruttoumsatz (EUR, log)", fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.7)

    from matplotlib.patches import Patch
    colors = sns.color_palette("viridis", n_colors=4)
    legend_elements = [Patch(facecolor=colors[i], label=author_order[i]) for i in range(len(author_order))]
    ax.legend(
        handles=legend_elements,
        title="Author Rating",
        bbox_to_anchor=(1.02, 0.5),
        loc="center left",
        fontsize=9,
        title_fontsize=10,
    )

    plt.tight_layout()
    st.pyplot(fig)

    # st.pyplot(fig)

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

        fig, ax = plt.subplots(figsize=(7, 4))
        sns.regplot(
            x="Average_Rating",
            y="Gross_Sales_EUR",
            data=df_corr,
            ci=None,
            ax=ax,
            line_kws={"color": "red"},
        )
        ax.set_yscale("log")
        ax.set_title(
            f"Bruttoumsatz vs. Bewertung\nKorrelationskoeffizient: {correlation:.2f}",
            fontsize=10,
        )
        ax.set_xlabel("Durchschnittliche Bewertung", fontsize=9)
        ax.set_ylabel("Bruttoumsatz (EUR)", fontsize=9)
        ax.grid(True)

        st.pyplot(fig)

    else:
        st.warning("Nicht genügend Daten für Regressionsanalyse verfügbar.")

    st.markdown("####  Interaktive Regressionsanalyse nach Genre")
    df_clean = df.dropna(subset=["Average_Rating", "Gross_Sales_EUR", "Genre"])
    df_clean = df_clean[df_clean["Publishing_Year"] >= 2005]

    genres = sorted(df_clean["Genre"].unique())
    selected_genre = st.selectbox("Wähle ein Genre zur Analyse:", genres)

    genre_df = df_clean[df_clean["Genre"] == selected_genre]

    if len(genre_df) >= 10:
        X = sm.add_constant(genre_df["Average_Rating"])
        y = genre_df["Gross_Sales_EUR"]
        model = sm.OLS(y, X).fit()
        corr = genre_df["Average_Rating"].corr(genre_df["Gross_Sales_EUR"])
        p_val = model.pvalues[1]

        col1, col2, col3 = st.columns(3)
        col1.metric("Korrelationskoeffizient", f"{corr:.3f}")
        col2.metric("p-Wert", f"{p_val:.4f}")
        col3.metric("R²", f"{model.rsquared:.3f}")

        fig, ax = plt.subplots(figsize=(4.5, 2.4))
        sns.regplot(
            x="Average_Rating",
            y="Gross_Sales_EUR",
            data=genre_df,
            ci=None,
            ax=ax,
            line_kws={"color": "darkred"},
            scatter_kws={"s": 12, "alpha": 0.6}
        )
        ax.set_yscale("log")
        ax.set_title(f"{selected_genre} | log(Umsatz) vs. Bewertung", fontsize=9)
        ax.set_xlabel("Durchschnittliche Bewertung", fontsize=8)
        ax.set_ylabel("Bruttoumsatz (log EUR)", fontsize=8)
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Nicht genügend Daten für dieses Genre.")
def show():
    wirtschaftanalyse()
