import streamlit as st


def show():
    st.markdown(
        """
        <style>
        .title {
            font-size:60px;
            font-weight:bold;
            color:#FFD700;
            text-align:center;
            padding-top:30px;
        }
        .subtitle {
            font-size:32px;
            color:#bbbbbb;
            text-align:center;
            padding-bottom:20px;
        }
        .info-box {
            background-color: #111827;
            padding: 20px;
            border-radius: 10px;
            color: white;
            margin: 10px;
        }
        .section-title {
            font-size: 22px;
            color: #4ade80;
            margin-bottom: 10px;
        }
        </style>
        <div class='title'>📚 Book Market: Literatur trifft Data Science</div>
        <div class='subtitle'> Alles rund um Bücher.
        Interaktiv. Intelligent. Buchmarkt mit Datenblick. </div>
        """,
        unsafe_allow_html=True,
    )

    col1, spacer1, col2, spacer2, col3 = st.columns([3, 0.5, 3, 0.5, 3])

    with col1:
        st.markdown("#### 📊 Wirtschaftsanalyse")
        st.write(
            """
        Wirtschaftsanalyse des Buchmarkts

Diese Analyse untersucht die wirtschaftlichen Einflussfaktoren auf den Buchumsatz auf Basis eines realen Datensatzes. Im Fokus steht die Frage, welche Merkmale – wie z. B. durchschnittliche Bewertung, Genre oder Autor*innenstatus – den Bruttoumsatz eines Buches signifikant beeinflussen.
Das Projekt umfasst:

   - die Bereinigung und Analyse von Buchdaten der letzten 20 Jahre,

   - explorative Visualisierungen zu Zusammenhängen zwischen Bewertung, Genre und Umsatz,

   - den Einsatz eines linearen Regressionsmodells zur Untersuchung statistischer Einflüsse,

   - eine interaktive Analyse nach Genre,

   - sowie wirtschaftlich interpretierbare Handlungsempfehlungen für Verlage und Autor*innen.

Ziel ist es, datenbasierte Erkenntnisse für strategische Entscheidungen in der Buchvermarktung und Programmauswahl abzuleiten.
        """
        )

    with col2:
        st.markdown("#### 🤖 Buchempfehlungssystem")
        st.write(
            """
        Personalisierte Buchempfehlungen basierend auf semantischer Analyse von Buchbeschreibungen und individuellen Filtereinstellungen.

        - Inhaltsbasierte Empfehlungen: 
            Bücher finden, die einem ausgewählten Titel inhaltlich ähnlich sind, sortiert nach Relevanz

        - Filterbasierte Empfehlungen: 
            Bücher nach Genre, Autor, Erscheinungsjahr und Bewertung filtern und sortieren
        """
        )

    with col3:
        st.markdown("####  🎥 🎞️ ⭐  Verfilmungsprognose")
        st.write(
            """
        Analyse und Vorhersage der Verfilmungswahrscheinlichkeit von Büchern basierend auf historischen Daten.

        - einen Überblick über die Datengrundlage,

        - explorative Visualisierungen,

        - sowie ein Machine-Learning-Modell zur Vorhersage zukünftiger Buchverfilmungen.
        """
        )

    st.markdown("---")

    st.markdown("#### 📎 Credits")
    st.write(
        """
        Dieses Projekt wurde im Rahmen des Data Science Institute entwickelt.  
        
        Verwendete Modelle und Methoden:

        -Explorative Datenanalyse (Pandas, Seaborn, Matplotlib)
        
        -Lineare Regressionsmodelle zur Untersuchung von Einflussfaktoren auf den Bruttoumsatz

        -Korrelationsanalysen (Pearson)

        -Logistische Regression zur Verfilmungsprognose

        -Modellbewertung mittels Accuracy, Precision, Recall, AUC

        -Semantische Textanalyse mit SentenceTransformers

        -TF-IDF-Vektorisierung & Cosine Similarity

        -Text-Preprocessing inkl. Tokenisierung, Stopword-Filterung (NLTK & scikit-learn)

        -WordClouds zur Visualisierung

        Technologien & Bibliotheken:
        Streamlit · Pandas · NumPy · scikit-learn · Matplotlib · Seaborn · SentenceTransformers · NLTK · PyTorch · requests · ast

        - Projektmanagement mit [**SCRUM**](https://github.com/Lena-Wow/abschlussprojekt_Buchmarkt/tree/main/SCRUM)
        - Versionskontrolle & Zusammenarbeit mit [**GitHub**](https://github.com/Lena-Wow/abschlussprojekt_Buchmarkt/tree/main/BUCHPROJEKT)
        - Datenquellen:     [Kaggle](https://www.kaggle.com/), [Goodreads](https://www.goodreads.com/), Buchcover: © [Open Library](https://openlibrary.org/dev/docs/api/covers), Metadaten-Ergänzung: © [Google Books API](https://developers.google.com/books)

     
        """
    )
    st.markdown(
        """
    ### 👩‍💻 Team & GitHub
    - [Julia auf GitHub](https://github.com/julia-beispiel)  
    - [Lena auf GitHub](https://github.com/lena-wow)  
    - [Arina auf GitHub](https://github.com/arina-ds)  
    """,
        unsafe_allow_html=True,
    )
