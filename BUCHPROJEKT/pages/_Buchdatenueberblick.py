# Buchdatenueberblick
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Buchdaten", layout="wide")

# Daten laden
df_ana = pd.read_csv("book_data_clean.csv", sep=";", encoding="utf-8")
df_ana = df_ana.drop(columns=["Publisher_Revenue_EUR"], errors="ignore")

# Jahrbereich für Slider vorbereiten
min_jahr = int(df_ana["Publishing_Year"].min())
max_jahr = int(df_ana["Publishing_Year"].max())

# Sidebar: Jahr-Slider
jahr_slider = st.sidebar.slider(
    "📅 Jahr auswählen",
    min_value=min_jahr,
    max_value=max_jahr,
    value=(min_jahr, max_jahr),
    step=1,
)

# Sidebar: Auswahl der Grafik
auswahl = st.sidebar.radio(
    "🔘 Welche Grafik möchtest du sehen?",
    [
        "Anzahl Bücher pro Jahr",
        "Bewertung vs. Umsatz (Scatterplot)",
        "Verfilmte Bücher pro Jahr",
    ],
)

# Daten filtern nach Jahr
df_filtered = df_ana[
    (df_ana["Publishing_Year"] >= jahr_slider[0])
    & (df_ana["Publishing_Year"] <= jahr_slider[1])
]

# Layout: zwei Spalten
col1, col2 = st.columns([2, 2])

# Linke Spalte: Tabelle und Statistik
with col1:
    st.title("📅 BUCHDATEN")
    st.write(
        f"### 📚 Bereinigte Daten für ML Model, Verlauf über die Jahre ({jahr_slider[0]}–{jahr_slider[1]})"
    )
    st.dataframe(df_filtered)
    st.markdown("---")
    st.write("**Numerische Basisstatistiken:**")
    st.write(df_filtered.describe())

# Rechte Spalte: Grafik
with col2:
    st.write("")
    st.title("📊 Visualisierung")

    if auswahl == "Anzahl Bücher pro Jahr":
        counts = df_filtered["Publishing_Year"].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(counts.index, counts.values, color="blue")
        ax.set_title(" Anzahl Bücher pro Jahr")
        ax.set_xlabel("Jahr")
        ax.set_ylabel("Anzahl")
        ax.grid(True)
        st.pyplot(fig)

    elif auswahl == "Bewertung vs. Umsatz (Scatterplot)":
        required_cols = {"Average_Rating", "Gross_Sales_EUR", "Author_Rating"}
        if required_cols.issubset(df_filtered.columns):
            # Autor-Rating in numerische Werte umwandeln
            rating_map = {"Novice": 1, "Intermediate": 2, "Excellent": 3, "Famous": 4}
            df_filtered["Author_Rating_Num"] = df_filtered["Author_Rating"].map(
                rating_map
            )

            fig, ax = plt.subplots(figsize=(7, 5))
            scatter = ax.scatter(
                df_filtered["Average_Rating"],
                df_filtered["Gross_Sales_EUR"],
                c=df_filtered["Author_Rating_Num"],
                cmap="viridis",
                alpha=0.7,
                edgecolors="k",
            )

            ax.set_xlabel("Average Rating")
            ax.set_ylabel("Gross Sales (EUR)")
            ax.set_title(" Bewertung vs. Umsatz (Farbskala: Author-Rating)")
            ax.grid(True)

            ax.set_yscale("log")  # <= Hier Log-Skala aktivieren

            cbar = plt.colorbar(scatter, ax=ax)
            # cbar.set_label("Author-Rating (1=Novice … 4=Famous)")
            cbar.set_ticks([1, 2, 3, 4])
            cbar.set_ticklabels(["Novice", "Intermediate", "Excellent", "Famous"])

            st.pyplot(fig)
        else:
            st.warning(
                "Benötigte Spalten ('Average_Rating', 'Gross_Sales_EUR', 'Author_Rating') fehlen."
            )

    elif auswahl == "Verfilmte Bücher pro Jahr":
        if "Adapted_to_Film" in df_filtered.columns:
            adapted_counts = (
                df_filtered[df_filtered["Adapted_to_Film"] == 1]["Publishing_Year"]
                .value_counts()
                .sort_index()
            )
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(adapted_counts.index, adapted_counts.values, color="red")
            ax.set_title(" Anzahl verfilmter Bücher pro Jahr")
            ax.set_xlabel("Jahr")
            ax.set_ylabel("Verfilmungen")
            ax.grid(True)
            st.pyplot(fig)
        else:
            st.warning("Spalte 'Adapted_to_Film' nicht vorhanden.")
