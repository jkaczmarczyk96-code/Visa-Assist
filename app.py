import streamlit as st
from engine import get
from countries import COUNTRIES
from datetime import datetime
from zoneinfo import ZoneInfo


# =========================
# 🕒 CZ TIME
# =========================
def get_cz_time():
    return datetime.now(ZoneInfo("Europe/Prague"))


# =========================
# ⚙️ PAGE
# =========================
st.set_page_config(
    page_title="Visa Assist",
    page_icon="🌍",
    layout="centered"
)


# =========================
# 🎨 STYLE (bez HTML card)
# =========================
st.markdown("""
<style>

body {
    background-color: #f4f7fb;
}

/* container */
.block-container {
    max-width: 900px;
}

/* button */
.stButton > button {
    background: linear-gradient(90deg,#0b2e4a,#1b4f8a);
    color: white;
    border-radius: 12px;
    font-weight: 600;
    padding: 0.6rem 1.2rem;
    border: none;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    background: #e30613;
    transform: scale(1.02);
}

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================
st.title("🌍 Visa Assist")
st.caption("Rychlá kontrola vízových podmínek")

st.divider()


# =========================
# INPUT
# =========================
passport = st.selectbox("🛂 Pas", ["CZ", "SK"])
country = st.selectbox("🌍 Země", COUNTRIES)


# =========================
# ACTION
# =========================
if st.button("🔍 Zkontrolovat vízové podmínky"):

    with st.spinner("Načítám aktuální data..."):
        result = get(passport, country)

    cz_time = get_cz_time()

    status_map = {
        "green": "🟢 Bez víza",
        "blue": "🔵 Víza při příjezdu / eVisa",
        "yellow": "🟡 eTA / registrace",
        "red": "🔴 Víza nutná"
    }

    icon_map = {
        "green": "🟢",
        "blue": "🔵",
        "yellow": "🟡",
        "red": "🔴"
    }

    visa_color = result.get("visa_color", "yellow")

    label = status_map.get(visa_color, "⚪ Neznámé")
    icon = icon_map.get(visa_color, "⚪")


    # =========================
    # UI CARD (Streamlit native)
    # =========================
    with st.container(border=True):

        st.markdown(f"## {icon} {country}")
        st.markdown(f"### {label}")

        st.write("🛂 **Visa type:**", result.get("visa_name", "N/A"))
        st.write("⏳ **Duration:**", result.get("visa_duration", "N/A"))

        st.divider()

        st.caption(f"🧠 Zdroj: {result.get('source')}")
        st.caption(f"🕒 CZ čas: {cz_time.strftime('%Y-%m-%d %H:%M:%S')}")
        st.caption(f"💾 Cache: {result.get('generated_at')}")
