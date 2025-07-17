# Neue Bücher aus 2024 holen
import pandas as pd

data = [
    [2024, "Future Secrets", "Jane Doe", "en", "Famous", 4.3, 250, 150000, "Penguin", "Sci-Fi"],
    [2024, "Love in the Stars", "John Smith", "en", "Intermediate", 3.8, 120, 80000, "Random House", "Romance"],
    [2025, "Mystic Worlds", "Alice Brown", "en", "Novice", 4.5, 60, 20000, "other", "Fantasy"],
    [2024, "Deep History", "Bob Green", "en", "Excellent", 4.7, 500, 300000, "HarperCollins", "Non-Fiction"]
]

columns = [
    "Publishing_Year", "Book_Name", "Author", "Language_Code", "Author_Rating",
    "Average_Rating", "Rating_Count", "Gross_Sales_EUR", "Publisher", "Genre"
]

df = pd.DataFrame(data, columns=columns)
df.to_csv("new_books_2024.csv", index=False)
print(" Datei 'new_books_2024.csv' wurde gespeichert.")


