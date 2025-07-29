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

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📊 Wirtschaftsanalyse")
        st.write(
            """
        Diese Analyse untersucht die wirtschaftlichen Einflussfaktoren auf den Umsatz von Büchern auf Basis eines realen Datensatzes. Im Mittelpunkt steht die Frage, welche Merkmale – wie z. B. Bewertung, Anzahl der Rezensionen, Genre oder Verlag – den Bruttoumsatz eines Buches signifikant beeinflussen.

Das Projekt beinhaltet:   eine Datenbereinigung und Fokussierung auf die letzten 20 Jahre, statistische Auswertungen und Visualisierungen zentraler Zusammenhänge, der Einsatz eines Regressionsmodells zur Prognose des Buchumsatzes,  eine detaillierte Bewertung des Einflusses von Nutzerbewertungen, wirtschaftlich interpretierbare Handlungsempfehlungen für Verlage und Autor*innen.

  

    

    

    


   
Ziel ist es, strategische Erkenntnisse für bessere Vermarktung und Programmplanung im Buchmarkt abzuleiten.
        """
        )

    with col2:
        st.markdown("#### 🤖 Empfehlungssystem")
        st.write(
            """
        Lass dir ähnliche Bücher empfehlen – basierend auf Genre, Bewertung & Co.
        """
        )

    with col3:
        st.markdown("####  🎥 🎞️ ⭐  Verfilmungsprognose")
        st.write(
            """
        Willkommen zur Analyse und Vorhersage der Verfilmungswahrscheinlichkeit von Büchern basierend auf historischen Daten.

        Diese Anwendung bietet:

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

        - Explorative Datenanalyse mit Pandas, Seaborn und Matplotlib  
        - Machine Learning: Logistische Regression  
        - Bewertung der Modelle über Accuracy, Precision, Recall und AUC  
        - Umsetzung als interaktive App mit Streamlit  
        - Projektmanagement mit [**SCRUM**](https://github.com/Lena-Wow/abschlussprojekt_Buchmarkt/tree/main/SCRUM)
        - Versionskontrolle & Zusammenarbeit mit [**GitHub**](https://github.com/Lena-Wow/abschlussprojekt_Buchmarkt/tree/main/BUCHPROJEKT)
        - Datenquellen:     [Kaggle](https://www.kaggle.com/), [Goodreads](https://www.goodreads.com/), Buchcover: © [Open Library](https://openlibrary.org/dev/docs/api/covers)

        **Team:** Arina, Lena, Julia
        """
    )
