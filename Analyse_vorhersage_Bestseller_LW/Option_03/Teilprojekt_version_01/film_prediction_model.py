from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np


# ---------------------------------------------------------------
# 📘 1. Funktion: Modell trainieren
# ---------------------------------------------------------------
def train_adaptation_model(df):
    # Nur relevante Spalten
    features = [
        "Publishing_Year",
        "Language_Code",
        "Author_Rating",
        "Average_Rating",
        "Rating_Count",
        "Gross_Sales_EUR",
        "Publisher_Revenue_EUR",
        "Genre",
    ]
    df = df[features + ["Adapted_to_Film"]].dropna()

    # Autor-Rating bereinigen (z.B. "4.3/5" → 4.3)
    def extract_rating(r):
        try:
            return float(str(r).split("/")[0])
        except:
            return None

    df["Author_Rating"] = df["Author_Rating"].apply(extract_rating)

    # Kategorische Features umwandeln
    cat_cols = ["Language_Code", "Genre"]
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    X_cat = encoder.fit_transform(df[cat_cols])
    cat_feature_names = encoder.get_feature_names_out(cat_cols)

    # Numerische Features
    num_cols = [
        "Publishing_Year",
        "Author_Rating",
        "Average_Rating",
        "Rating_Count",
        "Gross_Sales_EUR",
        "Publisher_Revenue_EUR",
    ]
    X_num = df[num_cols].values

    # Kombinieren
    X = np.hstack((X_num, X_cat))
    y = df["Adapted_to_Film"].values

    # Modell trainieren
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    print("✅ Modell erfolgreich trainiert!")
    return model, encoder


# ---------------------------------------------------------------
# 📘 2. Funktion: Vorhersage für ein neues Buch
# ---------------------------------------------------------------
def predict_film_for_book(book_data, model, encoder):
    # Autor-Rating extrahieren (falls im Format "4.3/5")
    try:
        book_data["Author_Rating"] = float(
            str(book_data["Author_Rating"]).split("/")[0]
        )
    except:
        book_data["Author_Rating"] = None

    # Feature-Reihenfolge sicherstellen
    cat_cols = ["Language_Code", "Genre"]
    num_cols = [
        "Publishing_Year",
        "Author_Rating",
        "Average_Rating",
        "Rating_Count",
        "Gross_Sales_EUR",
        "Publisher_Revenue_EUR",
    ]

    # One-Hot-Encoding der Kategorien
    X_cat = encoder.transform([[book_data[c] for c in cat_cols]])
    X_num = np.array([[book_data[c] for c in num_cols]])

    # Kombinieren
    X = np.hstack((X_num, X_cat))

    # Vorhersage
    prob = model.predict_proba(X)[0][1]  # Wahrscheinlichkeit für Klasse 1 (Verfilmt)
    return prob
