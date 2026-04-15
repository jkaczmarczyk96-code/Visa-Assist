import streamlit as st
import pandas as pd
import plotly.express as px
from engine import get

st.set_page_config(page_title="Cestovní Asistent", layout="wide")

st.title("🌍 Cestovní Asistent")
st.write("Víza pro občany ČR a SR")

countries = {
    "CZ": "Česká republika",
    "SK": "Slovensko",
    "DE": "Německo",
    "FR": "Francie",
    "IT": "Itálie",
    "ES": "Španělsko",
    "US": "USA",
    "JP": "Japonsko",
    "TH": "Thajsko",
    "AU": "Austrálie"
}

col1, col2 = st.columns(2)

with col1:
    passport = st.selectbox("Občanství", ["CZ", "SK"])

with col2:
    country = st.selectbox("Země", list(countries.keys()),
                           format_func=lambda x: countries[x])

if st.button("Zkontrolovat víza"):

    data = get(passport, country)

    st.write("### Výsledek")
    st.write("Země:", countries[country])
    st.write("Víza:", data["visa"])
    st.write("Délka pobytu:", data["days"])
    st.write("Zdroj:", data["source"])


st.subheader("Mapa")

df = pd.DataFrame([
    {"country": c, "days": get(passport, c)["days"]}
    for c in countries
])

fig = px.choropleth(df, locations="country", locationmode="ISO-3",
                    color="days", color_continuous_scale="Blues")

st.plotly_chart(fig)
