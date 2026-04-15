import streamlit as st
import pandas as pd
import plotly.express as px
from engine import get

# ======================
# UI SETUP
# ======================
st.set_page_config(page_title="Visa Assist", layout="wide")

st.markdown("""
<style>
.nadpis {font-size:40px;color:#0B2E59;font-weight:800;}
.pod {color:#E30613;font-size:18px;}
.karta {background:white;padding:20px;border-radius:15px;box-shadow:0 4px 12px rgba(0,0,0,0.08);}
</style>
""", unsafe_allow_html=True)

# ======================
# 100+ ZEMÍ (ZÁKLAD)
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
# HEADER
# ======================
st.markdown('<div class="nadpis">🌍 Visa Assist</div>', unsafe_allow_html=True)
st.markdown('<div class="pod">Víza, pobyt a cestovní informace</div>', unsafe_allow_html=True)

# ======================
# INPUT
# ======================
col1, col2 = st.columns(2)

with col1:
    passport = st.selectbox("Občanství", ["CZ", "SK"])

with col2:
    country = st.selectbox("Cílová země", list(countries.keys()),
                            format_func=lambda x: countries[x])

# ======================
# VÝSLEDEK
# ======================
if st.button("Zkontrolovat víza"):

    data = get(passport, country)

    st.markdown('<div class="karta">', unsafe_allow_html=True)
    st.write("###", countries[country])
    st.write("Víza:", data["visa"])
    st.write("Délka pobytu:", data["days"], "dní")
    st.write("Zdroj:", data["source"])
    st.markdown('</div>', unsafe_allow_html=True)

# ======================
# MAPA
# ======================
st.subheader("Mapa světa")

df = pd.DataFrame([
    {"country": c, "days": get(passport, c)["days"]}
    for c in countries
])

fig = px.choropleth(df, locations="country", locationmode="ISO-3",
                    color="days", color_continuous_scale="Blues")

st.plotly_chart(fig, use_container_width=True)