import streamlit as st
from engine import get
from countries import COUNTRIES
from datetime import datetime
from zoneinfo import ZoneInfo


# =========================
# 🕒 CZ TIME (CET/CEST)
# =========================
def get_cz_time():
    return datetime.now(ZoneInfo("Europe/Prague"))


# =========================
# ⚙️ PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Visa Assist",
    page_icon="🌍",
    layout="centered"
)

# =========================
# 🎨 EUROPE ASSISTANCE STYLE (SIMILAR UX)
# =========================
st.markdown("""
<style>

/* background */
body {
    background-color: #f4f7fb;
}

/* main container spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 900px;
}

/* title */
.title {
    font-size: 38px;
    font-weight: 800;
    color: #0b2e4a;
    margin-bottom: 0;
}

/* subtitle */
.subtitle {
    font-size: 15px;
    color: #5b6b7a;
    margin-bottom: 20px;
}

/* card */
.card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    border-left: 6px solid #e30613; /* red accent */
}

/* button style */
.stButton > button {
    background: #1b4f8a;
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    border: none;
    font-weight: 600;
}

.stButton > button:hover {
    background: #0f3b6d;
    color: white;
}

/* divider */
hr {
    border: none;
    height: 1px;
    background: #e6e9ef;
}

</style>
""", unsafe_allow_html=True)


# =========================
# 🏠 HEADER (ASSISTANCE STYLE)
# =========================
st.markdown("<div class='title'>🌍 Visa Assist</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Rychlá kontrola vízových podmínek pro vaše cesty</div>", unsafe_allow_html=True)

st.divider()


# =========================
# 📥 INPUT SECTION
# =========================
col1, col2 = st.columns(2)

with col1:
    passport = st.selectbox("🛂 Cestovní pas", ["CZ", "SK"])

with col2:
    country = st.selectbox("🌍 Cílová země", COUNTRIES)


# =========================
# 🚀 ACTION
# =========================
if st.button("🔍 Zkontrolovat vízové podmínky"):

    with st.spinner("Načítám aktuální data..."):
        result = get(passport, country)

    cz_time = get_cz_time()

    # =========================
    # 📦 RESULT CARD
    # =========================
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📊 Výsledek kontroly")

    st.write("🌍 Země:", country)
    st.write("🛂 Víza:", result.get("visa_name", "N/A"))
    st.write("⏳ Délka pobytu:", result.get("visa_duration", "N/A"))
    st.write("🎨 Kategorie:", result.get("visa_color", "N/A"))
    st.write("🧠 Zdroj:", result.get("source", "N/A"))

    # CZ TIME (LETNÍ/ZIMNÍ AUTOMAT)
    st.caption(f"🕒 Čas v ČR: {cz_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # API GENERATION TIME
    if result.get("generated_at"):
        st.caption(f"⚙️ Generováno: {result['generated_at']}")

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# FOOTER
# =========================
st.divider()
st.caption("Visa Assist • Travel intelligence engine • CZ/EU time zone enabled")
