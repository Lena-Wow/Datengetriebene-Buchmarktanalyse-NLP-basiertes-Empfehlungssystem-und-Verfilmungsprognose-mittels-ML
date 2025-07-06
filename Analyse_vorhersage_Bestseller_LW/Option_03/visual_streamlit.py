import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Daten laden
pfad = "D:\\awrDATEN\\lena\\DATA SCIENCE INSTITUTE\\abschlussprojekt_Buchmarkt\\Analyse_vorhersage_Bestseller_LW\\Option_03\\zusammengefuegt.csv"
df = pd.read_csv(pfad)

# Titel der App
st.title("📚 Buchpublikationsdaten – Kurzübersicht")

# Vorschau auf die Datenstream
st.subheader("🧾 Vorschau auf die Daten")
st.dataframe(df.head())

# Spaltenübersicht
st.subheader("🧮 Spaltenübersicht")
st.write(df.columns.tolist())

# Auswahl einer Spalte zur Visualisierung
st.subheader("📊 Spaltenbasierte Visualisierung")
spalte = st.selectbox(
    "Wähle eine Spalte zur Anzeige",
    df.select_dtypes(include=["object", "category"]).columns,
)

# Zähle die Häufigkeit der Werte in dieser Spalte
if spalte:
    st.write(f"Häufigkeit der Werte in **{spalte}**:")
    st.bar_chart(df[spalte].value_counts())

# (Optional) Korrelationen zwischen numerischen Werten zeigen
numerisch = df.select_dtypes(include=["float64", "int64"])
if not numerisch.empty:
    st.subheader("📈 Korrelationen (numerische Merkmale)")
    fig, ax = plt.subplots()
    sns.heatmap(numerisch.corr(), annot=True, cmap="Blues", ax=ax)
    st.pyplot(fig)
