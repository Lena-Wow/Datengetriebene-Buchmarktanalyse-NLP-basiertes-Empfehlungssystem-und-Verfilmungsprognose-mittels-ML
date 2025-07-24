# empfehlung.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from custom_stopwords import all_stopwords
from sklearn.metrics.pairwise import cosine_similarity

# ---------- DATEN UND MODELL LADEN ----------

@st.cache_data
def load_data():
    books = pd.read_csv("!cleaned_books_latest.csv")  
    return books

@st.cache_resource
def build_model(books):
    tfidf = TfidfVectorizer(stop_words=all_stopwords)
    tfidf_matrix = tfidf.fit_transform(books['clean_description'])  
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return tfidf, cosine_sim


#tfidf_matrix = tfidf.fit_transform(books['description'].fillna(''))
#cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)


books = load_data()
tfidf, cosine_sim = build_model(books)

# ---------- FUNKTION FÜR EMPFEHLUNGEN ----------


def find_similar_books(title, df, stopwords, top_n=5):
    target_row = books[books['title'] == title]

    if target_row.empty:
        return []
    
    target_desc = target_row.iloc[0]['clean_description']

    # A list of descriptions except for the target_desc
    descriptions =books[books['title'] != title]['clean_description'].tolist()

    # TF-IDF Vektorisierung mit target_desc an erster Stelle
    tfidf = TfidfVectorizer(
        stop_words=all_stopwords,
        ngram_range=(1, 2),
        max_df=0.7,
        min_df=3
    )
    tfidf_matrix = tfidf.fit_transform([target_desc] + descriptions)

    # Cosine Similarity: compare target_desc with all other descriptions 
    cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Top N Indizes nach Ähnlichkeit sortieren
    similarities = enumerate(cos_sim)
    similar_books = sorted(similarities, key=lambda x: x[1], reverse=True)[:top_n]

    # Ergebnisse als Liste von (Index, Score, Titel)
    results = [(idx, score, books.iloc[idx]['title']) for idx, score in similar_books]
    
    return results

def print_similar_books(similar_books):
    for i, (book_index, similarity_score, title) in enumerate(similar_books, start=1):
        print(f"{i}. Buch: '{title}' mit Ähnlichkeit: {similarity_score:.2%}")

# Beispiel Nutzung:
target_book = books.iloc[0]  # z. B. erstes Buch.    # EIGENTLICH FILTERED_BOOKS!!!
sim_books = find_similar_books(target_book['clean_description'], books, all_stopwords)
print_similar_books(sim_books)



# ---------- STREAMLIT UI ----------





def show():
    st.subheader("Content-basierte Buchempfehlung")
    
    selected_title = st.selectbox("Wähle ein Buch aus:", sorted(books['title'].unique()))

    if selected_title:
        st.markdown(f"### Dein gewähltes Buch: *{selected_title}*")
        #st.markdown(f"**Autor**{book_author}")
        
        selected_book = books[books['title'] == selected_title].iloc[0]
        isbn = selected_book['isbn']
        cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
        st.image(cover_url, caption=f"ISBN: {isbn}", width=150)

        st.markdown("---")
        st.write("### Ähnliche Bücher:")
        recommendations = find_similar_books(title=selected_title, df=books, stopwords=all_stopwords, top_n=5)

        # Anzahl Spalten (z. B. 5 nebeneinander)
        num_columns = 5
        columns = st.columns(num_columns)


        for idx, book in enumerate(recommendations):
            st.write(book)
            col = columns[idx % num_columns]  # Rotiert durch die Spalten
            with col:
                book_id = book[0]
                score = book[1]
                book_title = book[2]

                # Book's metadata from the books DataFrame
                book_row = books.iloc[book_id]
                book_author = book_row['author']
                book_isbn = book_row['isbn']
                book_genres = book_row['genres']
            
                st.markdown(f"**ID:** {book[0]}")
                st.markdown(f"**Score:** {score:.2f}")
                st.markdown(f"**Titel:** {book_title}")
                st.markdown(f"**Autor** {book_author}")
                cover_url = f"https://covers.openlibrary.org/b/isbn/{book_isbn}-M.jpg"
                st.image(cover_url, width=120)
                st.caption(f"Genres: {book_genres}")






# streamlit run streamlit_mod_app.py







<<<<<<< Updated upstream
        Du wirst z. B. nach deinem Lieblingsgenre, Autor oder Bewertungsniveau gefragt,
        und das System schlägt dir ähnliche Bücher vor.
        """
    )
=======





>>>>>>> Stashed changes
