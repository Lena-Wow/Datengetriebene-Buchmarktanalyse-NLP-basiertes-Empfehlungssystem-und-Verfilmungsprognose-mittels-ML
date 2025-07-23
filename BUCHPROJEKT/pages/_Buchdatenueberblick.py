# Buchdatenueberblick
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Buchdatenueberblick", layout="wide")

st.title("📅 BUCHDATEN")

# Daten laden und bereinigen
df_ana = pd.read_csv("book_data_clean.csv", sep=";", encoding="utf-8")
df_ana = df_ana.drop(columns=["Publisher_Revenue_EUR"], errors="ignore")

# Min und Max Jahr bestimmen
min_jahr = int(df_ana["Publishing_Year"].min())
max_jahr = int(df_ana["Publishing_Year"].max())

# Slider in der Sidebar für Jahrbereich
jahr_slider = st.sidebar.slider(
    "📅 Jahr auswählen",
    min_value=min_jahr,
    max_value=max_jahr,
    value=(min_jahr, max_jahr),
    step=1,
)

# Daten filtern nach ausgewähltem Jahrbereich
df_filtered = df_ana[
    (df_ana["Publishing_Year"] >= jahr_slider[0])
    & (df_ana["Publishing_Year"] <= jahr_slider[1])
]

# Layout: zwei Spalten (links Tabelle, rechts Grafik)
col1, col2 = st.columns([3, 2])

with col1:
    st.write(
        f"### 📚 Trainingsdaten für das ML-Model / Verfilmungvorhersage({jahr_slider[0]}–{jahr_slider[1]}, bereinigt)"
    )
    st.write("")
    st.dataframe(df_filtered)

    st.write("**Numerische Basisstatistiken:**")
    st.write(df_filtered.describe())

with col2:
    st.write("### 📈 Anzahl Bücher pro Jahr (Liniendiagramm)")
    # Anzahl Bücher je Jahr berechnen
    counts = df_filtered.groupby("Publishing_Year").size()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(
        counts.index, counts.values, linestyle="-", color="blue"
    )  # kein marker mehr
    ax.set_xlabel("Jahr")
    ax.set_ylabel("Anzahl Bücher")
    # ax.set_title("Anzahl der Bücher pro Jahr")
    ax.grid(True)

    st.pyplot(fig)
