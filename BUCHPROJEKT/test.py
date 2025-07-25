import streamlit as st
import pandas as pd

data = {"year": [1990, 2000, 2500]}
df = pd.DataFrame(data)
df["year1"] = df["year"].apply(lambda x: "{:,}".format(x))
df["year2"] = df["year"].astype(str)
df["year3"] = df["year"].astype("Int64")
df["year4"] = df["year"].astype("float")
df.dtypes
st.dataframe(df)
