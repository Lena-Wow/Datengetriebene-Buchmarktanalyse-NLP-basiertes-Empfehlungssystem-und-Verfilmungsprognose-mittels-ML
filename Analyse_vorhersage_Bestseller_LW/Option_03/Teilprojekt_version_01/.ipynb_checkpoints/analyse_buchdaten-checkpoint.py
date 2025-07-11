import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 📥 Bereinigte Datei laden
df = pd.read_csv("book_data_clean.csv", sep=";", encoding="utf-8")

# 🧐 Überblick
print("📊 Vorschau:")
print(df.head())
print("\n🔍 Spalten:")
print(df.columns)
print("\n📈 Statistik:")
print(df.describe(include="all"))

# 🎨 Stil setzen (optional)
sns.set(style="whitegrid")

# 📌 Beispiel 1: Verteilung der Genres
plt.figure(figsize=(12, 6))
df["Genre"].value_counts().head(15).plot(kind="bar", title="Top 15 Genres")
plt.xlabel("Genre")
plt.ylabel("Anzahl Bücher")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 📌 Beispiel 2: Durchschnittliche Bewertung nach Genre
plt.figure(figsize=(12, 6))
genre_rating = (
    df.groupby("Genre")["Average_Rating"].mean().sort_values(ascending=False).head(15)
)
genre_rating.plot(kind="bar", title="Durchschnittliche Bewertung nach Genre")
plt.xlabel("Genre")
plt.ylabel("Ø Bewertung")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 📌 Beispiel 3: Veröffentlichungen pro Jahr
plt.figure(figsize=(10, 5))
df["Publishing_Year"].value_counts().sort_index().plot(
    kind="line", title="Veröffentlichungen pro Jahr"
)
plt.xlabel("Jahr")
plt.ylabel("Anzahl Bücher")
plt.tight_layout()
plt.show()

# 📌 Beispiel 4: Korrelationen
plt.figure(figsize=(10, 6))
sns.heatmap(
    df[
        ["Average_Rating", "Rating_Count", "Gross_Sales_EUR", "Publisher_Revenue_EUR"]
    ].corr(),
    annot=True,
    cmap="coolwarm",
)
plt.title("📊 Korrelationsmatrix")
plt.tight_layout()
plt.show()


# 🔍 Nur relevante Spalten auswählen
pairplot_data = df[[
    "Average_Rating",
    "Rating_Count",
    "Gross_Sales_EUR",
    "Publisher_Revenue_EUR"
]]

#  Optional: NaNs entfernen (Pairplot kann keine NaNs)
pairplot_data = pairplot_data.dropna()

#  Pairplot erstellen
sns.pairplot(pairplot_data, kind="scatter", plot_kws={"alpha": 0.6, "s": 40})
plt.suptitle(" Paarweise Beziehungen", fontsize=16, y=1.02)
plt.tight_layout()
plt.show()