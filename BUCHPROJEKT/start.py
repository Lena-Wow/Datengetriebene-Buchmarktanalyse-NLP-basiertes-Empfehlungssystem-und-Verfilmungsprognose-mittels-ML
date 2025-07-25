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
        <div class='title'>📚 Book Market .....</div>
        <div class='subtitle'> Alles rund um Bücher.
        Interaktiv. Intelligent. Buchmarkt mit Datenblick. </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("#### 📊 Wirtschaftanalyse")
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
        st.markdown("#### 🏆 Verfilmungsprognose")
        st.write(
            """
        Wird ein Buch verfilmt? Teste es mit unserem Modell.
        """
        )

    st.markdown("---")

    st.markdown("#### 📎 Credits")
    st.write(
        """
        - Dieses Projekt wurde im Rahmen des Data Science Institute entwickelt  
        - Datengrundlage: Buchverkäufe,  eigene Analysen  .........
        - Modelle: Logistic Regression, ..............
        """
    )
