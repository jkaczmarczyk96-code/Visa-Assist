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
# 🎨 STYLE (minimal safe)
# =========================
st.markdown("""
<style>
.block-container {
    max-width: 900px;
}
.stButton > button {
    background: linear-gradient(90deg,#0b2e4a,#1b4f8a);
    color: white;
    border-radius: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================
st.title("🌍 Visa Assist")
st.caption("Rychlá a přehledná kontrola vízových podmínek")

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

    # =========================
    # STATUS MAP
    # =========================
    status_map = {
        "green": ("Visa-free entry", "#2ecc71"),
        "blue": ("Visa on arrival / eVisa", "#3498db"),
        "yellow": ("Electronic authorization required", "#f1c40f"),
        "red": ("Visa required before travel", "#e74c3c")
    }

    label, color = status_map.get(
        result.get("visa_color"),
        ("Unknown status", "#999")
    )

    # =========================
    # CONFIDENCE SCORE
    # =========================
    confidence_map = {
        "Travel Buddy API": 95,
        "TravelBriefing": 80,
        "Rule Engine": 70,
        "Fallback system": 40,
        "Global fallback": 30
    }

    confidence = confidence_map.get(result.get("source"), 50)

    # =========================
    # CARD (SAFE STREAMLIT)
    # =========================
    with st.container(border=True):

        # barevný indikátor
        st.markdown(
            f'<div style="height:8px;border-radius:10px;background:{color};margin-bottom:12px;"></div>',
            unsafe_allow_html=True
        )

        st.subheader(country)
        st.markdown(f"**{label}**")

        st.divider()

        st.write("🛂 Visa type:", result.get("visa_name", "N/A"))
        st.write("⏳ Maximum stay:", result.get("visa_duration", "N/A"))
        st.write("📊 Confidence:", f"{confidence}%")

        st.divider()

        st.caption(f"Source: {result.get('source')}")
        st.caption(f"Updated: {result.get('generated_at')} (CET)")
