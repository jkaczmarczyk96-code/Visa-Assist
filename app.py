import streamlit as st
import pandas as pd
import plotly.express as px
from engine import get, get_many

# ======================
# UI
# ======================
st.set_page_config(page_title="Cestovní Asistent", layout="wide")

st.title("🌍 Cestovní Asistent (FAST verze)")
st.write("Optimalizovaná verze s cache + API + fallback")

# ======================
# DATA
# ======================
countries = {
    "CZ": "Česká republika",
    "SK": "Slovensko",

    "AT": "Rakousko",
    "DE": "Německo",
    "PL": "Polsko",
    "IT": "Itálie",
    "FR": "Francie",
    "ES": "Španělsko",
    "HR": "Chorvatsko",
    "GR": "Řecko",
    "TR": "Turecko",
    "EG": "Egypt",
    "TN": "Tunisko",
    "MA": "Maroko",

    "AE": "UAE (Dubaj)",
    "QA": "Katar",
    "SA": "Saúdská Arábie",

    "US": "USA",
    "CA": "Kanada",
    "MX": "Mexiko",

    "TH": "Thajsko",
    "VN": "Vietnam",
    "ID": "Indonésie",
    "MY": "Malajsie",
    "SG": "Singapur",
    "JP": "Japonsko",
    "KR": "Jižní Korea",
    "CN": "Čína",
    "IN": "Indie",

    "AU": "Austrálie",
    "NZ": "Nový Zéland",

    "BR": "Brazílie",
    "AR": "Argentina",
    "CL": "Chile",
    "PE": "Peru",

    "ZA": "Jižní Afrika",
    "KE": "Keňa",
    "TZ": "Tanzanie",

    "IS": "Island",
    "NO": "Norsko",
    "SE": "Švédsko",
    "FI": "Finsko",
    "DK": "Dánsko",
    "NL": "Nizozemsko",
    "BE": "Belgie",
    "CH": "Švýcarsko",
    "GB": "Velká Británie",
    "IE": "Irsko"
}

# ======================
# INPUT
# ======================
col1, col2 = st.columns(2)

with col1:
    passport = st.selectbox("Občanství", ["CZ", "SK"])

with col2:
    country = st.selectbox(
        "Země",
        list(countries.keys()),
        format_func=lambda x: countries[x]
    )

# ======================
# DETAIL
# ======================
if st.button("Zkontrolovat víza"):

    with st.spinner("Načítám data..."):
        data = get(passport, country)

    st.success("Hotovo")

    st.write("### Výsledek")
    st.write("Země:", countries[country])
    st.write("Víza:", data["visa"])
    st.write("Délka:", data["days"])
    st.write("Zdroj:", data["source"])


# ======================
# MAPA (OPTIMALIZOVANÁ)
# ======================
st.subheader("Mapa světa (optimalizovaná)")

if st.checkbox("Zobrazit mapu"):

    sample = list(countries.keys())  # můžeš dát [:20] pro ještě rychlejší

    with st.spinner("Načítám mapu..."):
        data_map = get_many(passport, sample)

    df = pd.DataFrame([
        {"country": c, "days": data_map[c]["days"]}
        for c in sample
    ])

    fig = px.choropleth(
        df,
        locations="country",
        locationmode="ISO-3",
        color="days",
        color_continuous_scale="Blues"
    )

    st.plotly_chart(fig, use_container_width=True)
