# empfehlung.py
import streamlit as st
import pandas as pd


def show():
    st.subheader("Intelligente Buchempfehlungen")

    st.write(
        """
        🔍 Hier entsteht bald ein Modell, das basierend auf deinen Vorlieben passende Bücher empfiehlt.

        Du wirst z. B. nach deinem Lieblingsgenre, Autor oder Bewertungsniveau gefragt,
        und das System schlägt dir ähnliche Bücher vor.
        """
    )
"""
    # Beispielhafte Auswahl (später vom Modell ersetzt)
    genre = st.selectbox(
        "Entdecke die bestbewerteten Bücher nach Genre",
        ["Fantasy", "Thriller", "Romance", "Science Fiction", "Sachbuch"],
    )
    min_rating = st.slider("Minimale Bewertung", 0.0, 5.0, 3.5, 0.1)

    year_range = st.slider("Veröffentlichungsjahr (von–bis)", 1800, 2018, (1990, 2018))

    st.write(
        f"Suche nach Büchern im Genre **{genre}** mit Bewertung ab **{min_rating}** ..."
    )

    # Placeholder für empfohlene Bücher (hier: Dummy-Daten)
    recommended_books = pd.DataFrame(
        {
            "Titel": ["(Platzhalter 1)", "(Platzhalter 2)", "(Platzhalter 3)"],
            "Autor": ["Autor A", "Autor B", "Autor C"],
            "Bewertung": [4.2, 4.0, 3.9],
            "Genre": [genre] * 3,
        }
    )

    st.write("### 📘 Deine Empfehlungen:")
    st.dataframe(recommended_books)

    st.info(
        "Das Empfehlungssystem wird bald mit echten Daten und Machine Learning ergänzt!"
    )



    # Beispiel-Daten (ersetze das mit deinem echten DataFrame)
    books = pd.DataFrame({
        'title': [
            'Dread Nation',
            'To Win Her Heart',
            'When Crickets Cry'
        ],
        'isbn': [
            '0062570609',
            '0764207571',
            '1595540547'
        ]
    })

    st.title("Buchcover Explorer")

    # Auswahlbox für den Titel
    selected_title = st.selectbox("Wähle ein Buch aus:", books['title'])

    # Hole die zugehörige ISBN
    selected_isbn = books[books['title'] == selected_title]['isbn'].values[0]

    # Erzeuge die URL zum Cover-Bild (Größe: L)
    cover_url = f"https://covers.openlibrary.org/b/isbn/{selected_isbn}-L.jpg"

    # Anzeige
    st.markdown(f"### {selected_title}")
    st.image(cover_url, caption=f"ISBN: {selected_isbn}", width=200)








def get_recommendations(title, cosine_sim=cosine_sim):
    indices = pd.Series(books.index, index=books['title']).drop_duplicates()
    idx = indices.get(title, None)
    if idx is None:
        return []

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    book_indices = [i[0] for i in sim_scores]
    return books.iloc[book_indices]







import streamlit as st

def show():
    st.subheader("Content-basierte Buchempfehlung")

    selected_title = st.selectbox("Wähle ein Buch aus:", sorted(books['title'].unique()))

    if selected_title:
        st.markdown(f"### Dein gewähltes Buch: *{selected_title}*")
        
        selected_book = books[books['title'] == selected_title].iloc[0]
        isbn = selected_book['isbn']
        cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
        st.image(cover_url, caption=f"ISBN: {isbn}", width=150)

        st.markdown("---")
        st.write("### Ähnliche Bücher:")

        recommendations = find_similar_books(
            title=selected_title,
            cosine_sim=cosine_sim,
            top_n=5
        )

        # Anzahl der Spalten (z. B. 3 nebeneinander)
        num_columns = 3
        columns = st.columns(num_columns)

        for idx, (_, book) in enumerate(recommendations.iterrows()):
            col = columns[idx % num_columns]
            with col:
                st.markdown(f"**{book['title']}** von *{book['author']}*")
                img_url = f"https://covers.openlibrary.org/b/isbn/{book['isbn']}-M.jpg"
                st.image(img_url, width=120)
                st.caption(f"📚 Genre: {book['main_genre']}")
                st.caption(f"🧠 Ähnlichkeit: {book['similarity']:.2f}")
                st.markdown("---")





def show():
    st.subheader("Content-basierte Buchempfehlung")
    
    selected_title = st.selectbox("Wähle ein Buch aus:", sorted(books['title'].unique()))

    if selected_title:
        st.markdown(f"### Dein gewähltes Buch: *{selected_title}*")
        
        selected_book = books[books['title'] == selected_title].iloc[0]
        isbn = selected_book['isbn']
        cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
        st.image(cover_url, caption=f"ISBN: {isbn}", width=150)

        st.markdown("---")
        st.write("### Ähnliche Bücher:")
        recommendations = find_similar_books(selected_title)

        for _, book in recommendations.iterrows():
            st.markdown(f"**{book['title']}** von *{book['author']}*")
            cover_url = f"https://covers.openlibrary.org/b/isbn/{book['isbn']}-M.jpg"
            st.image(cover_url, width=120)
            st.caption(f"Genre: {book['main_genre']}")
            st.markdown("---")"""