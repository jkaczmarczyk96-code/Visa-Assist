import streamlit as st
from engine import get
from countries import COUNTRIES
from datetime import datetime
from zoneinfo import ZoneInfo


def get_cz_time():
    return datetime.now(ZoneInfo("Europe/Prague"))


st.set_page_config(page_title="Visa Assist", page_icon="🌍")

st.title("🌍 Visa Assist")
st.caption("Přehled vízových podmínek")

st.divider()

passport = st.selectbox("🛂 Pas", ["CZ", "SK"])
country = st.selectbox("🌍 Země", COUNTRIES)

debug_mode = st.checkbox("🐞 Developer mode")

if st.button("🔍 Zkontrolovat"):

    result = get(passport, country)

    status_map = {
        "green": ("Visa-free entry", "#2ecc71"),
        "blue": ("Visa on arrival / eVisa", "#3498db"),
        "yellow": ("Authorization required", "#f1c40f"),
        "red": ("Visa required", "#e74c3c")
    }

    label, color = status_map.get(result["visa_color"], ("Unknown", "#999"))

    confidence_map = {
        "Travel Buddy API": 95,
        "TravelBriefing": 80,
        "Rule Engine": 70,
        "Fallback": 40
    }

    confidence = confidence_map.get(result.get("source"), 50)

    with st.container(border=True):

        st.markdown(
            f'<div style="height:8px;background:{color};border-radius:10px;margin-bottom:10px;"></div>',
            unsafe_allow_html=True
        )

        st.subheader(country)
        st.markdown(f"**{label}**")

        st.divider()

        st.write("🛂 Visa type:", result.get("visa_name"))
        st.write("⏳ Maximum stay:", result.get("visa_duration"))
        st.write("📊 Confidence:", f"{confidence}%")

        st.divider()

        st.caption(f"Source: {result.get('source')}")
        st.caption(f"Updated: {result.get('generated_at')}")

    # =========================
    # DEBUG PANEL
    # =========================
    if debug_mode:
        with st.expander("🐞 Debug info"):

            for line in result.get("debug", []):
                st.write(line)

            st.divider()
            st.json(result)
