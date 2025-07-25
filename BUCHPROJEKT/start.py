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
            font-size:20px;
            color:lightgray;
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
        Erkunde Verkaufszahlen, Bewertungen, Genres und mehr.
        Interaktive Grafiken helfen, Trends zu erkennen.
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
        Dieses Projekt wurde im Rahmen des Data Science Institute entwickelt  
            Verwendete Modelle und Methoden:

            -->Explorative Datenanalyse mit Pandas, Seaborn und Matplotlib

            -->Maschinelles Lernen: Logistische Regression

            -->Bewertung der Modelle über Accuracy, Precision, Recall und AUC

            --> Umsetzung als interaktive App mit Streamlit

        Team: Arina, Lena, Julia
        """
    )
