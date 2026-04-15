import streamlit as st
import pandas as pd
import plotly.express as px
from engine import get, get_country_list

# =========================
# 🌐 NASTAVENÍ STRÁNKY
# =========================
st.set_page_config(
    page_title="Visa Assist",
    layout="wide",
    page_icon="🛂"
)

# =========================
# 🎨 STYL (EUROP ASSISTANCE INSPIRED)
# =========================
st.markdown("""
<style>

.stApp {
    background-color: #F5F8FC;
}

/* HLAVNÍ NADPIS */
.main-title {
    font-size: 44px;
    font-weight: 900;
    color: #0B2E59;
    margin-bottom: 5px;
}

/* PODNADPIS */
.subtitle {
    font-size: 18px;
    color: #E30613;
    font-weight: 500;
    margin-bottom: 25px;
}

/* KARTA VÝSLEDKU */
.card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    border-left: 6px solid #0B2E59;
}

/* TLAČÍTKO */
.stButton>button {
    background-color: #0B2E59;
    color: white;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 600;
    border: none;
}

.stButton>button:hover {
    background-color: #E30613;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 🌍 HLAVIČKA
# =========================
st.markdown('<div class="main-title">🛂 Visa Assist</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Okamžité informace o vízových povinnostech po celém světě</div>', unsafe_allow_html=True)

# =========================
# 🌍 DATA
# =========================
countries = get_country_list()

# =========================
# 📥 VSTUP
# =========================
col1, col2 = st.columns(2)

with col1:
    passport = st.selectbox("Občanství (pas)", ["CZ", "SK"])

with col2:
    country = st.selectbox(
        "Cílová země",
        list(countries.keys()),
        format_func=lambda x: countries[x]
    )

# =========================
# 📊 VÝSLEDEK
# =========================
if st.button("Zkontrolovat vízové podmínky"):

    with st.spinner("Analyzuji vízové podmínky..."):
        data = get(passport, country)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.write("### ✈️ Výsledek cesty")
    st.write("**Cílová země:**", countries[country])
    st.write("**Víza potřebná:**", "Ano" if data["visa"] else "Ne")
    st.write("**Maximální délka pobytu:**", str(data["days"]), "dní")
    st.write("**Zdroj dat:**", data["source"])

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 🌍 MAPA SVĚTA
# =========================
st.markdown("---")
st.subheader("🌍 Přehled světa")

if st.checkbox("Zobrazit mapu vízových podmínek"):

    with st.spinner("Načítám data pro celý svět..."):
        df = pd.DataFrame([
            {"země": c, "víza": 1 if get(passport, c)["visa"] else 0}
            for c in countries.keys()
        ])

    fig = px.choropleth(
        df,
        locations="země",
        locationmode="ISO-3",
        color="víza",
        color_continuous_scale=["#2E86DE", "#E30613"],
        title="Mapa vízových požadavků"
    )

    st.plotly_chart(fig, use_container_width=True)
