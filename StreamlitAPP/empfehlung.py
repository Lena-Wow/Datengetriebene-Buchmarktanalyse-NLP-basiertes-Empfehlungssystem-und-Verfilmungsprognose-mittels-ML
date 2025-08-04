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
    books["genre_list"] = books["genre_list"].apply(
        lambda x: ast.literal_eval(x) if pd.notna(x) else []
    )
    return books


@st.cache_resource
def load_model():
    return SentenceTransformer("all-mpnet-base-v2")


@st.cache_data
def compute_embeddings(_model, descriptions):
    return _model.encode(descriptions, convert_to_tensor=True)


books = load_data()
model = load_model()
# ❌ embeddings = compute_embeddings(model, descriptions)  # ENTFERNT

# ---------- FUNCTION FOR RECOMMENDATION ----------


def find_similar_books(title, df, model, embeddings, top_n=5):
    target_row = df[df["title"] == title]
    if target_row.empty:
        return []

    target_desc = target_row.iloc[0]["clean_description"]
    target_embedding = model.encode(target_desc, convert_to_tensor=True)
    cos_sim = util.cos_sim(target_embedding, embeddings)[0]
    top_results = torch.topk(cos_sim, k=top_n + 1)

    results = []
    for score, idx in zip(top_results.values, top_results.indices):
        idx = idx.item()
        score = score.item()
        if df.iloc[idx]["title"] != title:
            results.append((idx, score, df.iloc[idx]["title"]))
        if len(results) == top_n:
            break
    return results


# ---------- FUNCTION FOR BOOK COVER ----------


def get_book_cover(isbn):
    if pd.isna(isbn) or isbn == "":
        return "https://placehold.co/120x180?text=No+Cover&font=roboto"
    cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
    response = requests.get(cover_url)
    if response.status_code == 200 and response.headers.get(
        "Content-Type", ""
    ).startswith("image"):
        return cover_url
    else:
        return "https://placehold.co/120x180?text=No+Cover&font=roboto"


# ---------- STREAMLIT UI ----------


def show():
    st.header("Content-basierte Buchempfehlung")

    option = st.radio(
        "Bücher entdecken",
        ("Ähnlich wie ein bestimmtes Buch", "Über Filter (Genre, Bewertung etc.)"),
        key="empfehlung_option_radio_main",
    )

    st.markdown("#### Du hast folgende Filteroptionen")
    with st.expander("Filter anzeigen / ausblenden"):
        min_rating = st.slider(
            "Minimale durchschnittliche Bewertung",
            0.0,
            5.0,
            3.5,
            0.1,
            key="min_avg_rating",
        )
        selected_year = st.slider(
            "Erscheinungsjahr (optional)",
            1811,
            2018,
            (2000, 2018),
            1,
            key="filter_years",
        )
        selected_genres = st.multiselect(
            "Genres (optional)",
            options=sorted(
                {
                    genre
                    for sublist in books["genre_list"].dropna().tolist()
                    for genre in sublist
                }
            ),
            key="filter_genres",
        )
        selected_author = None
        if option == "Über Filter (Genre, Bewertung etc.)":
            selected_author = st.selectbox(
                "Autor (optional)",
                options=["Alle Autoren"] + sorted(books["author"].unique().tolist()),
                index=0,
                key="filter_author",
            )

    # -------- Option 1: Ähnliche Bücher --------
    if option == "Ähnlich wie ein bestimmtes Buch":
        selected_title = st.selectbox(
            "Wähle ein Buch aus der Liste aus",
            sorted(books["title"].unique()),
            index=None,
            placeholder="Buchtitel eingeben oder auswählen...",
            key="book_selectbox",
        )

        if not selected_title:
            st.info("Bitte wähle ein Buch aus der Liste.")
            return

        selected_book = books[books["title"] == selected_title].iloc[0]
        year = selected_book["publication_year"]
        book_author = selected_book["author"]
        rating = selected_book["avg_rating"]
        book_genres = selected_book["genres"]
        isbn = selected_book["isbn"]
        cover_url = get_book_cover(isbn)

        st.markdown("### Dein gewähltes Buch")
        left_col, right_col = st.columns([1, 4])
        with left_col:
            st.image(cover_url, caption=f"ISBN: {isbn}", width=200)
        with right_col:
            st.markdown(f"### {selected_title} ({year})")
            st.markdown(f"**Autor:** {book_author}")
            st.markdown(f"**Bewertung:** {rating}")
            st.markdown(f"**Genres:** {book_genres}")

        st.markdown("---")
        st.write("### Ähnliche Bücher")

        # ✅ Embeddings werden jetzt erst hier berechnet:
        with st.spinner("Berechne Text-Embeddings..."):
            descriptions = books["clean_description"].tolist()
            embeddings = compute_embeddings(model, descriptions)

        recommendations = find_similar_books(
            title=selected_title, df=books, model=model, embeddings=embeddings, top_n=20
        )

        filtered_recommendations = []
        for idx, score, title in recommendations:
            row = books.iloc[idx]
            if (
                row["avg_rating"] >= min_rating
                and selected_year[0] <= row["publication_year"] <= selected_year[1]
                and all(genre in row["genre_list"] for genre in selected_genres)
            ):
                filtered_recommendations.append((row, score))

        if not filtered_recommendations:
            st.warning("Keine passenden Buchempfehlungen gefunden.")
        else:
            for book_row, score in filtered_recommendations[:5]:
                with st.container():
                    left_col, right_col = st.columns([1, 4])
                    with left_col:
                        st.image(get_book_cover(book_row["isbn"]), width=150)
                    with right_col:
                        st.markdown(
                            f"### {book_row['title']} ({book_row['publication_year']})"
                        )
                        st.markdown(f"**Autor:** {book_row['author']}")
                        st.markdown(f"**Genres:** {book_row['genres']}")
                        st.markdown(f"**Bewertung:** {book_row['avg_rating']}")
                        st.markdown(f"**Ähnlichkeit:** {100 * score:.1f}%")
                st.markdown("---")

    # -------- Option 2: Nur Filter --------
    elif option == "Über Filter (Genre, Bewertung etc.)":
        st.markdown("### Gefilterte Bücherliste")
        filtered_df = books.copy()

        if selected_author != "Alle Autoren":
            filtered_df = filtered_df[filtered_df["author"] == selected_author]

        filtered_df = filtered_df[
            (filtered_df["avg_rating"] >= min_rating)
            & (filtered_df["publication_year"] >= selected_year[0])
            & (filtered_df["publication_year"] <= selected_year[1])
        ]

        if selected_genres:
            filtered_df = filtered_df[
                filtered_df["genre_list"].apply(
                    lambda genre_list: all(
                        selected in genre_list for selected in selected_genres
                    )
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
                        st.image(get_book_cover(row["isbn"]), width=200)
                    with right_col:
                        st.markdown(f"### {row['title']} ({row['publication_year']})")
                        st.markdown(f"**Autor:** {row['author']}")
                        st.markdown(f"**Genres:** {row['genres']}")
                        st.markdown(f"**Bewertung:** {row['avg_rating']}")
                st.markdown("---")


# App starten
show()
