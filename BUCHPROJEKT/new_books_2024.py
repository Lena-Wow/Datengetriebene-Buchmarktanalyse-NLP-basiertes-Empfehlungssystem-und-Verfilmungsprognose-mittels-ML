import pandas as pd

data = [
    [
        2024,
        "Here One Moment",
        "Liane Moriarty",
        "en",
        "Famous",
        4.0,
        226112,
        65500000,
        "Crown",
        "Thriller",
    ],
    [
        2025,
        "The Last Anniversary",
        "Liane Moriarty",
        "en",
        "Famous",
        3.8,
        162406,
        900000,
        "other",
        "Mystery",
    ],
    [2024, "book1", "autor1", "en", "Famous", 4.3, 250, 150000, "Penguin", "Sci-Fi"],
    [2025, "book2", "autor1", "en", "Famous", 4.3, 250, 150000, "Penguin", "Sci-Fi"],
    [2024, "book1", "autor2", "en", "Famous", 4.3, 250, 150000, "Penguin", "Sci-Fi"],
    [2025, "book2", "autor2", "en", "Famous", 4.3, 250, 150000, "Penguin", "Sci-Fi"],
]

columns = [
    "Publishing_Year",
    "Book_Name",
    "Author",
    "Language_Code",
    "Author_Rating",
    "Average_Rating",
    "Rating_Count",
    "Gross_Sales_EUR",
    "Publisher",
    "Genre",
]

df = pd.DataFrame(data, columns=columns)
df.to_csv("new_books_2024.csv", index=False)
print("✅ Datei 'new_books_2024.csv' wurde aktualisiert.")
