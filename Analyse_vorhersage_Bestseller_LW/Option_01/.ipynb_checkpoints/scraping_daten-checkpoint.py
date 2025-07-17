import requests
import pandas as pd
from bs4 import BeautifulSoup

# 1. Wikipedia-URL
url = "https://en.wikipedia.org/wiki/List_of_best-selling_books"

# 2. HTML-Inhalt abrufen
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# 3. Alle Tabellen lesen
tables = pd.read_html(response.text)

print(f"✅ Tabellen gefunden: {len(tables)}")

# 4. Alle Tabellen zusammenführen
all_books = pd.DataFrame()
for i, table in enumerate(tables):
    print(f"🔹 Tabelle {i} hat {table.shape[0]} Zeilen")
    all_books = pd.concat([all_books, table], ignore_index=True)

# 5. Spalte 'First published' in Zahl umwandeln
all_books["First published"] = pd.to_numeric(all_books["First published"], errors="coerce")

# 6. Nach Büchern ab 1969 filtern
books_after_1969 = all_books[all_books["First published"] >= 1969]

# 7. Ergebnis anzeigen
print("\n📘 Bücher, die nach 1969 veröffentlicht wurden:")
print(books_after_1969[["Book", "Author(s)", "First published", "Approximate sales", "Genre"]])

# Optional: Als CSV speichern
#books_after_1969.to_csv("bestseller_ab_1969.csv", index=False)
books_after_1969.to_csv("bestseller_ab_1969.csv", sep=';', index=False)