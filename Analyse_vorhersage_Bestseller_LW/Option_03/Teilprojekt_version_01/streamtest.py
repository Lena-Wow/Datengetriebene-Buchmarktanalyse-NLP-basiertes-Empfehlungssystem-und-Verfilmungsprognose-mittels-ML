import warnings
import sys
import streamlit as st


st.set_page_config(page_title="Buch", layout="wide")

st.header("📘 Projekt: Buchverfilmungsvorhersage")

st.sidebar.write("Buch auswählen")
x, y, z = st.columns(3)
x.write("Model 1")
y.write("Model 2")
z.write("Model 3")

start = x.container()

popover = start.popover("das ist ein Popover")
popover.write("geheimer text)")

testbutton = x.toggle("hier klicken")
if testbutton == True:
    x.write("Du hast den Knopf gedrückt")


slider = x.slider("Das ist ein slide", value=(11, 45))
x.write(slider)


auswahl = x.multiselect("mehrere Auswahl", [1, 2, 3])
auswahl2 = x.pills("mehrere Auswahl", [1, 2, 3], selection_mode="multi")

auswahl3 = x.selectbox("auswahl treffen", [1, 2, 3])
