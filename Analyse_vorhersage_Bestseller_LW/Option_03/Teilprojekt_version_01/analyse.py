import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from rapidfuzz import process, fuzz

# ---------------------------------------------------------------
# 🔧 Einstellungen für Datei-Import/-Export
# ---------------------------------------------------------------
CSV_INPUT = "buch_basisdaten.csv"
CSV_OUTPUT = "buch_basisdaten_bereinigt_mit_genres.csv"
ENCODING = "utf-8"
SEP = ";"  # Annahme: Daten sind mit Semikolon getrennt

# ---------------------------------------------------------------
# 🧩 Sprache standardisieren (z. B. "eng", "en-US" → "en")
# ---------------------------------------------------------------
language_map = {
    "eng": "en", "en-US": "en", "en-GB": "en", "en-CA": "en", "en-AU": "en",
    "spa": "es", "fre": "fr"
}

def standardize_language(code):
    return language_map.get(code, code)

# ---------------------------------------------------------------
# 🔄 Funktion zur Bereinigung von Zahlenfeldern
# ---------------------------------------------------------------
def clean_number(value, typ="float"):
    if pd.isna(value):
        return None
    try:
        value = str(value)
        value = (
            value.replace("€", "")
                 .replace("Â", "")
                 .replace("\xa0", "")
                 .replace("\x80", "")
                 .replace(" ", "")
                 .replace(".", "")
                 .replace(",", ".")
                 .strip()
        )
        return int(float(value)) if typ == "int" else float(value)
    except Exception as e:
        print(f"⚠️ Fehler bei Wert: {repr(value)} → {e}")
        return None

# ---------------------------------------------------------------
# 🧠 Genre-Normalisierung mit fuzzy matching
# ---------------------------------------------------------------
standard_genres = [
    "Fantasy", "Science Fiction", "Thriller", "Mystery", "Historical Fiction",
    "Romance", "Fiction", "Biography", "Memoir", "Children’s", "Young Adult",
    "Nonfiction", "Horror", "Adventure", "Philosophy", "Politics", "Satire",
    "Graphic Novel", "Dystopian", "Classic",
]

def generate_genre_mapping(unique_genres):
    mapping = {}
    for genre in unique_genres:
        if pd.isna(genre) or genre == "":
            mapping[genre] = genre
            continue
        result = process.extractOne(genre, standard_genres, scorer=fuzz.token_sort_ratio)
        if result and result[1] > 30:
            mapping[genre] = result[0]
        else:
            mapping[genre] = genre
    return mapping

# ---------------------------------------------------------------
# 🧼 Hauptfunktion zur vollständigen Datenbereinigung
# ---------------------------------------------------------------
def clean_book_data(df):
        # Verfilmung vereinheitlichen
# Verfilmung in binär (1 = Ja, 0 = Nein, None = unklar) umwandeln
    if "Verfilmt" in df.columns:
        df['Verfilmt'] = df['Verfilmt'].astype(str).str.lower().str.strip()
        df['Verfilmt'] = df['Verfilmt'].replace({
            "ja": 1, "ja?": 1, "yes": 1,
            "nein": 0, "no": 0,
            "-": None, "unclear": None, "nan": None, "": None
        })
        df['Verfilmt'] = df['Verfilmt'].astype("float")  # als numerischer Wert für Analyse/ML
    # Sprache vereinheitlichen
    df['Language_Code'] = df['Language_Code'].apply(standardize_language)

    # Genre-Mapping erstellen und anwenden
    if "Genre_new" in df.columns:
        unique_genres = df['Genre_new'].dropna().unique()
        genre_mapping = generate_genre_mapping(unique_genres)
        df['Genre_standardized'] = df['Genre_new'].map(genre_mapping)
    else:
        df['Genre_standardized'] = None

    # Relevante Spalten numerisch bereinigen
    numeric_columns = {
        "Gross_sales/ Bruttoumsatz": "float",
        "Publisher_Revenue": "float",
        "Book_Average_Rating": "float",
        "Book_Ratings_Count": "int"
    }

    for col, typ in numeric_columns.items():
        if col in df.columns:
            df[col] = df[col].apply(lambda x: clean_number(x, typ))

    # Entferne Bücher mit unrealistischen Jahresangaben (vor Jahr 1000)
    if "Publishing_Year" in df.columns:
        df = df[df["Publishing_Year"] >= 1000]

    # Überflüssige Spalten löschen
    df = df.drop(columns=["Unnamed: 12", "Genre_new"], errors="ignore")

    # Index zurücksetzen nach Filterung
    return df.reset_index(drop=True)

# ---------------------------------------------------------------
# 🚀 Skript-Ausführung: Daten laden, bereinigen, speichern
# ---------------------------------------------------------------
def main():
    try:
        df = pd.read_csv(CSV_INPUT, encoding='latin1', sep=SEP)
        print(f"📄 Datei geladen: {CSV_INPUT}")
    except Exception as e:
        print(f"❌ Fehler beim Laden der Datei: {e}")
        return

    df = clean_book_data(df)

    try:
        df.to_csv(CSV_OUTPUT, index=False, encoding=ENCODING, sep=SEP)
        print(f"✅ Bereinigte Datei gespeichert unter: {CSV_OUTPUT}")
    except PermissionError:
        fallback = "buch_basisdaten_output_fallback.csv"
        df.to_csv(fallback, index=False, encoding=ENCODING, sep=SEP)
        print(f"⚠️ Ursprüngliche Datei blockiert. Gespeichert als: {fallback}")

    # Vorschau auf bereinigte Daten
    print("\n📊 Datenvorschau:")
    print(df.head())

    print("\n🧾 Spaltenübersicht:")
    print(df.info())

    print("\n📈 Statistikübersicht:")
    print(df.describe(include='all'))

    # Optional: Verteilung der Genres anzeigen
    if "Genre_standardized" in df.columns:
        print("\n🎭 Häufigste Genres:")
        print(df["Genre_standardized"].value_counts().head(10))

# Anzeigeoptionen anpassen (alle Spalten sichtbar)
df = pd.read_csv("buch_basisdaten_bereinigt_mit_genres.csv", sep=";", encoding="utf-8")
pd.set_option('display.max_columns', None)

# Zeige die ersten 10 Zeilen
print(df.head(10))
# ---------------------------------------------------------------
# 🧪 Ausführung
# ---------------------------------------------------------------
if __name__ == "__main__":
    main()


# Anzeigeoptionen anpassen (alle Spalten sichtbar)
df = pd.read_csv("buch_basisdaten_bereinigt_mit_genres.csv", sep=";", encoding="utf-8")
pd.set_option('display.max_columns', None)

# Zeige die ersten 10 Zeilen
print(df.head(10))

print("Anzahl verschiedener Genres:", df['Genre_standardized'].nunique())
print("Beispielhafte Genres:", df['Genre_standardized'].dropna().unique()[:20])

"""

import matplotlib.pyplot as plt

df['Genre_standardized'].value_counts().head(28).plot(kind='bar', figsize=(12,6), title="Top 20 Genres")
plt.xlabel("Genre")
plt.ylabel("Anzahl Bücher")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()"""