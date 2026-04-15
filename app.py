import streamlit as st
from engine import get
from countries import COUNTRIES
from datetime import datetime
from zoneinfo import ZoneInfo


# =========================
# 🕒 ČAS (CZ)
# =========================
def get_cz_time():
    return datetime.now(ZoneInfo("Europe/Prague"))


# =========================
# ⚙️ NASTAVENÍ STRÁNKY
# =========================
st.set_page_config(
    page_title="Visa Assist",
    page_icon="🌍",
    layout="centered"
)


# =========================
# HLAVIČKA
# =========================
st.title("🌍 Visa Assist")
st.caption("Přehled vízových podmínek pro cestování")

st.divider()


# =========================
# VSTUPY
# =========================
passport = st.selectbox("🛂 Typ pasu", ["CZ", "SK"])
country = st.selectbox("🌍 Cílová země", COUNTRIES)

debug_mode = st.checkbox("🐞 Vývojářský režim (debug)")


# =========================
# AKCE
# =========================
if st.button("🔍 Zjistit vízové podmínky"):

    with st.spinner("Zjišťuji aktuální podmínky..."):
        result = get(passport, country)

    # =========================
    # MAPA STAVŮ
    # =========================
    status_map = {
        "green": ("Bez víza", "#2ecc71"),
        "blue": ("Vízum při příjezdu / eVisa", "#3498db"),
        "yellow": ("Nutná registrace (eTA / eVisa)", "#f1c40f"),
        "red": ("Vízum nutné před cestou", "#e74c3c")
    }

    label, color = status_map.get(
        result.get("visa_color"),
        ("Neznámý stav", "#999")
    )

    # =========================
    # SPOLEHLIVOST
    # =========================
    confidence_map = {
        "Travel Buddy API": 95,
        "TravelBriefing": 80,
        "Rule Engine": 70,
        "Fallback": 40
    }

    confidence = confidence_map.get(result.get("source"), 50)

    # =========================
    # KARTA VÝSLEDKU
    # =========================
    with st.container(border=True):

        # barevný indikátor
        st.markdown(
            f'<div style="height:8px;background:{color};border-radius:10px;margin-bottom:10px;"></div>',
            unsafe_allow_html=True
        )

        st.subheader(country)
        st.markdown(f"**{label}**")

        st.divider()

        st.write("🛂 Typ víza:", result.get("visa_name", "Neuvedeno"))
        st.write("⏳ Maximální délka pobytu:", result.get("visa_duration", "Neuvedeno"))
        st.write("📊 Spolehlivost:", f"{confidence}%")

        st.divider()

        st.caption(f"Zdroj: {result.get('source')}")
        st.caption(f"Aktualizováno: {result.get('generated_at')}")

    # =========================
    # DEBUG PANEL
    # =========================
    if debug_mode:
        with st.expander("🐞 Debug informace"):

            debug_data = result.get("debug", [])

            if debug_data:
                for line in debug_data:
                    st.write(line)
            else:
                st.write("Žádná debug data")

            st.divider()
            st.caption("Surová data:")
            st.json(result)
