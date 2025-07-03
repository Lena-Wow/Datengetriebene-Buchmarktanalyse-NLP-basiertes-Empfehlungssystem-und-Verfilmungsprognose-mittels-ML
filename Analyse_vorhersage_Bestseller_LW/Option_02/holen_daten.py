import requests
import pandas as pd


# Bereits definierte Scraping‑Funktion (von oben)
def get_books_google_simple(query, max_results=100):
    books = []
    for start in range(0, max_results, 40):
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&startIndex={start}&maxResults=40"
        resp = requests.get(url)
        if resp.status_code != 200:
            continue
        for item in resp.json().get("items", []):
            info = item.get("volumeInfo", {})
            books.append(
                {
                    "title": info.get("title"),
                    "author": ", ".join(info.get("authors", [])),
                    "year": info.get("publishedDate", "")[:4],
                    "language": info.get("language"),
                    "category": (
                        ", ".join(info.get("categories", []))
                        if info.get("categories")
                        else None
                    ),
                    "avg_rating": info.get("averageRating"),
                    "ratings_count": info.get("ratingsCount"),
                    "page_count": info.get("pageCount"),
                }
            )
    df = pd.DataFrame(books)
    df = df[df["year"].str.isnumeric()]
    df["year"] = df["year"].astype(int)
    return df[df["year"].between(2000, 2024)]


# Beispielaufruf: hol ~200 Bücher aus mehreren Genres
df1 = get_books_google_simple("fiction")
df2 = get_books_google_simple("thriller")
df3 = get_books_google_simple("history")
df = pd.concat([df1, df2, df3], ignore_index=True).drop_duplicates(
    subset=["title", "author"]
)

# CSV speichern
df.to_csv("books_2000_2024_sample.csv", sep=';', index=False)
print(df.head())
print(f"Insgesamt {len(df)} Bücher geladen.")
