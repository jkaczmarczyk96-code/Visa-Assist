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
    "CZ": "Czech Republic",
    "SK": "Slovakia",

    "AT": "Austria",
    "DE": "Germany",
    "PL": "Poland",
    "IT": "Italy",
    "FR": "France",
    "ES": "Spain",
    "HR": "Croatia",
    "GR": "Greece",
    "TR": "Turkey",
    "EG": "Egypt",
    "TN": "Tunisia",
    "MA": "Morocco",

    "AE": "United Arab Emirates",
    "QA": "Qatar",
    "SA": "Saudi Arabia",

    "US": "United States",
    "CA": "Canada",
    "MX": "Mexico",

    "TH": "Thailand",
    "VN": "Vietnam",
    "ID": "Indonesia",
    "MY": "Malaysia",
    "SG": "Singapore",
    "JP": "Japan",
    "KR": "South Korea",
    "CN": "China",
    "IN": "India",

    "AU": "Australia",
    "NZ": "New Zealand",

    "BR": "Brazil",
    "AR": "Argentina",
    "CL": "Chile",
    "PE": "Peru",

    "ZA": "South Africa",
    "KE": "Kenya",
    "TZ": "Tanzania",

    "IS": "Iceland",
    "NO": "Norway",
    "SE": "Sweden",
    "FI": "Finland",
    "DK": "Denmark",
    "NL": "Netherlands",
    "BE": "Belgium",
    "CH": "Switzerland",
    "GB": "United Kingdom",
    "IE": "Ireland",

    "PT": "Portugal",
    "RO": "Romania",
    "BG": "Bulgaria",
    "HU": "Hungary",
    "SI": "Slovenia",
    "RS": "Serbia",
    "UA": "Ukraine",
    "GE": "Georgia",
    "AM": "Armenia",
    "AZ": "Azerbaijan",

    "IL": "Israel",
    "JO": "Jordan",
    "LB": "Lebanon",
    "OM": "Oman",
    "KW": "Kuwait",
    "BH": "Bahrain",

    "PH": "Philippines",
    "LK": "Sri Lanka",
    "NP": "Nepal",
    "BD": "Bangladesh",
    "PK": "Pakistan",

    "UZ": "Uzbekistan",
    "KZ": "Kazakhstan",
    "MN": "Mongolia",

    "FJ": "Fiji",
    "PG": "Papua New Guinea",
    "VU": "Vanuatu",

    "CU": "Cuba",
    "DO": "Dominican Republic",
    "JM": "Jamaica",
    "BS": "Bahamas",

    "CR": "Costa Rica",
    "PA": "Panama",
    "UY": "Uruguay",
    "PY": "Paraguay",

    "NG": "Nigeria",
    "GH": "Ghana",
    "ET": "Ethiopia",
    "UG": "Uganda",
    "RW": "Rwanda",
    "SN": "Senegal"
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
