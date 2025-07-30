# Buchempfehlung-Visualisierung
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Empfehlung-Buchdaten", layout="wide")


# Daten laden




# Layout: zwei Spalten
col1, col2 = st.columns([2, 2])

# Linke Spalte: Tabelle und Statistik
with col1:
    st.title("📅 BUCHDATEN")
    st.write(f"### 📚 Bereinigte Daten für....., Verlauf über die Jahre )")


# Rechte Spalte: Visualisierung
with col2:
    st.write("")
    st.title("📊 Visualisierung")
