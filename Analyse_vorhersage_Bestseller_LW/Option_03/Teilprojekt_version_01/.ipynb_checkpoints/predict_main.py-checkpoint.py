import pandas as pd
from film_prediction_model import train_adaptation_model, predict_film_for_book

# 📥 Bereinigte Datei laden
df = pd.read_csv("book_data_clean.csv", sep=";", encoding="utf-8")

# 🧠 Modell trainieren
model, encoder = train_adaptation_model(df)

# 🔮 Neues Buch testen
buch_neu = {
    "Publishing_Year": 2022,
    "Language_Code": "en",
    "Author_Rating": "4.5/5",
    "Average_Rating": 4.4,
    "Rating_Count": 95000,
    "Gross_Sales_EUR": 1200000,
    "Publisher_Revenue_EUR": 750000,
    "Genre": "Horror",
}

prob = predict_film_for_book(buch_neu, model, encoder)
print(f"🎬 Wahrscheinlichkeit, dass Buch verfilmt wird: {prob:.2%}")
