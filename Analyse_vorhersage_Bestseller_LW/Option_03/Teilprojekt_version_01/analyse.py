import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from rapidfuzz import process, fuzz

# ---------------------------------------------------------------
# 🔧 Einstellungen für Datei-Import/-Export
# ---------------------------------------------------------------
CSV_INPUT = "buch_basisdaten.csv"
CSV_OUTPUT = "book_data_clean.csv"
ENCODING = "utf-8"
SEP = ";"  # Semikolon-getrennt

# ---------------------------------------------------------------
# 🧩 Sprache standardisieren
# ---------------------------------------------------------------
language_map = {
    "eng": "en", "en-US": "en", "en-GB": "en", "en-CA": "en", "en-AU": "en",
    "spa": "es", "fre": "fr"
}

def standardize_language(code):
    return language_map.get(code, code)

# ---------------------------------------------------------------
# 🔄 Zahlenfelder bereinigen
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
    "Graphic Novel", "Dystopian", "Classic"
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
# 🧮 Logik zur Korrektur von fehlerhaftem Bruttoumsatz
# ---------------------------------------------------------------
def correct_gross_sales(df):
    corrected_count = 0
    for i, row in df.iterrows():
        gross = row["Gross_Sales_EUR"]
        revenue = row["Publisher_Revenue_EUR"]
        if pd.notna(gross) and pd.notna(revenue):
            if gross < revenue:
                df.at[i, "Gross_Sales_EUR"] = gross * 1000
                corrected_count += 1
    print(f"🔁 Korrigierte Einträge (Gross_Sales_EUR < Publisher_Revenue_EUR): {corrected_count}")
    return df

# ---------------------------------------------------------------
# 🧼 Hauptfunktion zur Datenbereinigung
# ---------------------------------------------------------------
def clean_book_data(df):
    # Verfilmung binär und numerisch
    if "Verfilmt" in df.columns:
        df['Verfilmt'] = df['Verfilmt'].astype(str).str.lower().str.strip()
        df['Verfilmt'] = df['Verfilmt'].replace({
            "ja": 1, "ja?": 1, "yes": 1,
            "nein": 0, "no": 0,
            "-": None, "unclear": None, "nan": None, "": None
        })
        df['Verfilmt'] = df['Verfilmt'].astype("float")

    # Sprache normalisieren
    if "Language_Code" in df.columns:
        df["Language_Code"] = df["Language_Code"].apply(standardize_language)

    # Genre-Normalisierung
    if "Genre_new" in df.columns:
        unique_genres = df["Genre_new"].dropna().unique()
        genre_mapping = generate_genre_mapping(unique_genres)
        df["Genre_standardized"] = df["Genre_new"].map(genre_mapping)
    else:
        df["Genre_standardized"] = None

    # Zahlenfelder bereinigen
    numeric_columns = {
        "Gross_sales/ Bruttoumsatz": "float",
        "Publisher_Revenue": "float",
        "Book_Average_Rating": "float",
        "Book_Ratings_Count": "int"
    }

    for col, typ in numeric_columns.items():
        if col in df.columns:
            df[col] = df[col].apply(lambda x: clean_number(x, typ))

    # Unrealistische Jahreszahlen entfernen
    if "Publishing_Year" in df.columns:
        df = df[df["Publishing_Year"] >= 1925]

    # Spalten englisch benennen
    column_rename_map = {
        "Titel": "Title",
        "Autor": "Author",
        "Sprache": "Language",
        "Language_Code": "Language_Code",
        "Genre_standardized": "Genre",
        "Publishing_Year": "Publishing_Year",
        "Gross_sales/ Bruttoumsatz": "Gross_Sales_EUR",
        "Publisher_Revenue": "Publisher_Revenue_EUR",
        "Book_Average_Rating": "Average_Rating",
        "Book_Ratings_Count": "Rating_Count",
        "Verfilmt": "Adapted_to_Film"
    }
    df = df.rename(columns=column_rename_map)

    # Überflüssige Spalten entfernen
    df = df.drop(columns=["Unnamed: 12", "Genre_new"], errors="ignore")

    # 💰 Bruttoumsatz-Korrektur durchführen
    df = correct_gross_sales(df)

    return df.reset_index(drop=True)

# ---------------------------------------------------------------
# 🚀 Hauptausführung
# ---------------------------------------------------------------
def main():
    try:
        df = pd.read_csv(CSV_INPUT, encoding='latin1', sep=SEP)
        print(f"📄 Datei geladen: {CSV_INPUT}")
    except Exception as e:
        print(f"❌ Fehler beim Laden: {e}")
        return

    df = clean_book_data(df)

    try:
        df.to_csv(CSV_OUTPUT, index=False, encoding=ENCODING, sep=SEP)
        print(f"✅ Gespeichert unter: {CSV_OUTPUT}")
    except PermissionError:
        fallback = "book_data_clean_fallback.csv"
        df.to_csv(fallback, index=False, encoding=ENCODING, sep=SEP)
        print(f"⚠️ Zugriff verweigert. Gespeichert als: {fallback}")

    # Vorschau
    print("\n📊 Datenvorschau:")
    print(df.head())
    print("\n🧾 Spaltenübersicht:")
    print(df.info())
    print("\n📈 Statistikübersicht:")
    print(df.describe(include='all'))

    if "Genre" in df.columns:
        print("\n🎭 Häufigste Genres:")
        print(df["Genre"].value_counts().head(10))

# ---------------------------------------------------------------
# 🧪 Ausführung
# ---------------------------------------------------------------
if __name__ == "__main__":
    main()
