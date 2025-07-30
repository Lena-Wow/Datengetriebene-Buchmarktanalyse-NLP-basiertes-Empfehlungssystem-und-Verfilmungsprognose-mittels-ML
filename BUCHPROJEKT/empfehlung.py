# empfehlung.py
import streamlit as st
import pandas as pd
import numpy as np
import ast
import requests
import torch
from sentence_transformers import SentenceTransformer, util

# ---------- DATEN UND MODELLE LADEN ----------


@st.cache_data
def load_data():
    books = pd.read_csv("final_books_pred.csv")

    # genre_list von String zu Type Liste umwandeln
    books['genre_list'] = books['genre_list'].apply(
        lambda x: ast.literal_eval(x) if pd.notna(x) else []
    )

    return books


@st.cache_resource
def load_model():
    # return SentenceTransformer('all-MiniLM-L6-v2')
    return SentenceTransformer('all-mpnet-base-v2')

@st.cache_data
def compute_embeddings(_model, descriptions):
    return _model.encode(descriptions, convert_to_tensor=True)

books = load_data()
model = load_model()
descriptions = books['clean_description'].tolist()
embeddings = compute_embeddings(model, descriptions)

# ---------- FUNCTION FOR RECOMMENDATION ----------

def find_similar_books(title, df, model, embeddings, top_n=5):
    target_row = df[df['title'] == title]

    if target_row.empty:
        return []

    target_desc = target_row.iloc[0]['clean_description']
    target_embedding = model.encode(target_desc, convert_to_tensor=True)

    # Output: Vektor, jeder Eintrag ist die Ähnlichkeit zwischen dem Ziel und einem Buch in der Datenbank (Vektor, weil [0], ohne eine Matrix mit nur einer Zeile)
    cos_sim = util.cos_sim(target_embedding, embeddings)[0]
    top_results = torch.topk(cos_sim, k=top_n + 1)

    results = []
    for score, idx in zip(top_results.values, top_results.indices):
        idx = idx.item()
        score = score.item()
        if df.iloc[idx]['title'] != title:  # eigenes Buch überspringen
            results.append((idx, score, df.iloc[idx]['title']))
        if len(results) == top_n:
            break

    return results

# ---------- FUNCTION FOR BOOK COVER ----------

def get_book_cover(isbn):
    if pd.isna(isbn) or isbn == '':
        # Kein ISBN vorhanden → Standardbild zurückgeben
        return "https://via.placeholder.com/120x180.png?text=No+Cover"

    cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
    
    # Prüfen, ob das Bild existiert
    response = requests.get(cover_url)
    if response.status_code == 200 and response.headers.get("Content-Type", "").startswith("image"):
        return cover_url
    else:
        # Bild nicht gefunden → Standardbild zurückgeben
        # return "https://via.placeholder.com/120x180.png?text=No+Cover"
        return "https://placehold.co/120x180?text=No+Cover&font=roboto"


# ---------- STREAMLIT UI ----------

def show():

    st.header("Content-basierte Buchempfehlung")

# ---------- Auswahl der Empfehlungsart ----------
    st.write("Ratio wird angezeigt")
    option = st.radio(
        "Bücher entdecken",
        ("Ähnlich wie ein bestimmtes Buch", "Über Filter (Genre, Bewertung etc.)"),
        key="empfehlung_option_radio"
    )

# ------------- COMMON FILTERS -------------

    st.markdown("#### Du hast folgende Filteroptionen")
    with st.expander("Filter anzeigen / ausblenden"):

        min_rating = st.slider(
            "Minimale durchschnittliche Bewertung",
            min_value=0.0,
            max_value=5.0,
            value=3.5,
            step=0.1,
            help="Wie viel sollte die minimale Bewertung sein?",
            key="min_avg_rating"
        )

        selected_year = st.slider(
            "Erscheinungsjahr (optional)",
            min_value=1811,
            max_value=2018,
            value=(2000, 2018),
            step=1,
            help="Begrenzt die Auswahl auf Bücher aus bestimmten Jahren.",
            key="filter_years"
        )

        selected_genres = st.multiselect(
            "Genres (optional)",
            options=sorted({genre for sublist in books['genre_list'].dropna().tolist() for genre in sublist}),
            key="filter_genres"
        )
        
        selected_author = None  # Initialisierung

        if option == "Über Filter (Genre, Bewertung etc.)":
            selected_author = st.selectbox(
                "Autor (optional)",
                options=["Alle Autoren"] + sorted(books['author'].unique().tolist()),
                index=0,
                key="filter_author"
            )

        #selected_author = st.selectbox(
            #"Autor (optional)",
            #options=["Alle Autoren"] + sorted(books['author'].unique().tolist()),
            #index=0, #--> Index 0 will be shown ("alle Autoren", if nothing will be selected)
            #key="filter_author"
        #)

# ------------- OPTION 1: BUCH AUSWÄHLEN -------------  

    if option == "Ähnlich wie ein bestimmtes Buch":
        selected_title = st.selectbox(
            "Wähle ein Buch aus der Liste aus", 
            sorted(books['title'].unique()),
            index=None,
            placeholder="Buchtitel eingeben oder auswählen...",
            key="book_selectbox")

        if not selected_title:
            st.info(f"Bitte wähle ein Buch aus der Liste.")
            return

        # Get Book information
        selected_book = books[books['title'] == selected_title].iloc[0]
        year = selected_book['publication_year']
        book_author = selected_book['author']
        rating = selected_book['avg_rating']
        book_genres = selected_book['genres']
        isbn = selected_book['isbn']
        cover_url = get_book_cover(isbn)

        st.markdown("### Dein gewähltes Buch")
            
        with st.container():
            # Zwei Spalten: Bild links, Text rechts
            left_col, right_col = st.columns([1, 4])

            with left_col:
                st.image(cover_url, caption=f"ISBN: {isbn}", width=200)

            with right_col:
                st.markdown(f"### {selected_title} ({year})")
                label_col, value_col = st.columns([1, 3])
                label_col.markdown("**Autor:**")
                value_col.markdown(book_author)

                label_col, value_col = st.columns([1, 3])
                label_col.markdown("**Bewertung:**")
                value_col.markdown(rating)

                label_col, value_col = st.columns([1, 3])
                label_col.markdown("**Genres:**")
                value_col.markdown(book_genres)

        st.markdown("---")
        st.write("### Ähnliche Bücher")
        recommendations = find_similar_books(
            title=selected_title,
            df=books,
            model=model,
            embeddings=embeddings,
            top_n=20
        )

        filtered_recommendations = []
        for idx, score, title in recommendations:
            row = books.iloc[idx]

            # Filter prüfen
            if (
                row['avg_rating'] >= min_rating and
                selected_year[0] <= row['publication_year'] <= selected_year[1] and
                #(selected_main_genre == "Alle Hauptgenres" or row['main_genre'] == selected_main_genre) and
                all(genre in row['genre_list'] for genre in selected_genres)
                #(selected_author == "Alle Autoren" or row['author'] == selected_author)
            ):
                filtered_recommendations.append((row, score))

        if not filtered_recommendations:
            st.warning("Keine passenden Buchempfehlungen gefunden.")
        else:
            for book_row, score in filtered_recommendations[:5]:
                with st.container():
                    left_col, right_col = st.columns([1, 4])
                    with left_col:
                        st.image(get_book_cover(book_row['isbn']), width=150)
                    with right_col:
                        st.markdown(f"### {book_row['title']} ({book_row['publication_year']})")
                        st.markdown(f"**Autor:** {book_row['author']}")
                        st.markdown(f"**Genres:** {book_row['genres']}")
                        st.markdown(f"**Bewertung:** {book_row['avg_rating']}")
                        st.markdown(f"**Ähnlichkeit:** {100 * score:.1f}%")
                st.markdown("---") # Trennlinie zwischen Büchern 


# -------------- OPTION 2: NUR FILTER -------------------
    elif option == "Über Filter (Genre, Bewertung etc.)":
        st.markdown("### Gefilterte Bücherliste")

        filtered_df = books.copy()

        if selected_author != "Alle Autoren":
            filtered_df = filtered_df[filtered_df['author'] == selected_author]

        filtered_df = filtered_df[
            (filtered_df['avg_rating'] >= min_rating) &
            (filtered_df['publication_year'] >= selected_year[0]) &
            (filtered_df['publication_year'] <= selected_year[1])
        ]

        #if selected_main_genre != "Alle Hauptgenres":
            #filtered_df = filtered_df[filtered_df['main_genre'] == selected_main_genre]

        if selected_genres:
            filtered_df = filtered_df[
                filtered_df['genre_list'].apply(
                    lambda genre_list: all(selected in genre_list for selected in selected_genres)
                )
            ]

        filtered_df = filtered_df.sort_values(by="avg_rating", ascending=False)

        st.markdown(f"**{len(filtered_df)} Bücher gefunden**")

        if filtered_df.empty:
            st.warning("Leider keine Bücher gefunden. Bitte passe deine Filter an.")
        else:
            for _, row in filtered_df.iterrows():
                with st.container():
                    left_col, right_col = st.columns([1, 4])
                    with left_col:
                        st.image(get_book_cover(row['isbn']), width=200)
                    with right_col:
                        st.markdown(f"### {row['title']} ({row['publication_year']})")
                        st.markdown(f"**Autor:** {row['author']}")
                        st.markdown(f"**Genres:** {row['genres']}")
                        st.markdown(f"**Bewertung:** {row['avg_rating']}")
                st.markdown("---")

    
show()


# streamlit run streamlit_mod_app.py
