import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random


def scrape_amazon_books(start_page=1, end_page=3):
    base_url = (
        "https://www.amazon.de/s?k=bücher&i=stripbooks&rh=n%3A530484031&page={page}"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/58.0.3029.110 Safari/537.3"
    }

    books = []

    for page in range(start_page, end_page + 1):
        print(f"Scraping Seite {page}")
        url = base_url.format(page=page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.find_all("div", {"data-component-type": "s-search-result"})

        for item in items:
            try:
                # Buchname
                title = item.h2.text.strip()

                # Autor (manchmal mehrere, wir nehmen ersten)
                author = (
                    item.find("div", class_="a-row a-size-base a-color-secondary")
                    .text.strip()
                    .split("|")[0]
                )

                # Sale Rank - nicht direkt aufgelistet, daher hier nur Platzhalter
                sale_rank = None

                # Bewertungen & Ratings
                rating_span = item.find("span", class_="a-icon-alt")
                book_avg_rating = (
                    float(rating_span.text.split(" ")[0]) if rating_span else None
                )

                rating_count_span = item.find("span", {"class": "a-size-base"})
                book_ratings_count = (
                    int(rating_count_span.text.replace(".", ""))
                    if rating_count_span
                    else 0
                )

                # Verlagsangaben nicht auf der Übersichtsseite vorhanden => Platzhalter
                publisher = None

                # Grob geschätzte Verkäufe anhand Rang (hier als None)
                gross_sales = None

                # Sprache und Genre fehlen, hier Platzhalter
                language_code = "DE"
                genre = None

                # Verkaufsinformationen fehlen => Platzhalter
                publisher_revenue = None
                sale_price = None
                units_sold = None

                # Veröffentlichungsjahr - meist nicht direkt ersichtlich => None
                publishing_year = None

                # Author rating - schwer zu bekommen, None
                author_rating = None

                books.append(
                    {
                        "Publishing_Year": publishing_year,
                        "Book_Name": title,
                        "Author": author,
                        "Language_Code": language_code,
                        "Author_Rating": author_rating,
                        "Book_Average_Rating": book_avg_rating,
                        "Book_Ratings_Count": book_ratings_count,
                        "Genre": genre,
                        "Gross_Sales": gross_sales,
                        "Publisher_Revenue": publisher_revenue,
                        "Sale_Price": sale_price,
                        "Sale_Rank": sale_rank,
                        "Publisher": publisher,
                        "Units_Sold": units_sold,
                    }
                )
            except Exception as e:
                print(f"Fehler bei Buch: {e}")

        # Wartezeit um Amazon nicht zu überlasten
        time.sleep(random.uniform(5, 10))

    df = pd.DataFrame(books)
    return df


if __name__ == "__main__":
    df_books = scrape_amazon_books(1, 2)
    print(df_books.head())
    df_books.to_csv("amazon_books_nicht_bestseller.csv", index=False)
