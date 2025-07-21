# Wirtschaftanalyse.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def show():
    st.subheader("📊 Wirtschaftanalyse der Buchdaten")

    try:
        df = pd.read_csv("book_data_clean.csv", sep=";", encoding="utf-8")
        df.columns = df.columns.str.strip()
    except FileNotFoundError:
        st.error("❌ Datei 'book_data_clean.csv' wurde nicht gefunden.")
        return

    # Beispiel: Basisstatistiken
    st.write("### 📈 Basisinformationen")
    st.write(df.describe())
    st.write(df)
