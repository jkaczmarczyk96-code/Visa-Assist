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
st.set_page_config(page_title="Visa Assist", page_icon="🌍", layout="centered")

# =========================
# 🎨 STYLE
# =========================
st.markdown("""
<style>
body {
    background-color:#f4f7fb;
}

.block-container {
    max-width: 900px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    border-left: 6px solid #e30613;
}

.stButton > button {
    background: #1b4f8a;
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

    with st.spinner("Načítám..."):
        result = get(passport, country)

    cz_time = get_cz_time()

    # 🎨 BARVA
    color_map = {
        "green": "#28a745",
        "blue": "#007bff",
        "yellow": "#ffc107",
        "red": "#dc3545"
    }
    color = color_map.get(result.get("visa_color"), "#999")

    # =========================
    # HTML (DŮLEŽITÉ!)
    # =========================
    html = f"""
    <div class="card">
        <h3>📊 Výsledek</h3>

        <p><b>🌍 Země:</b> {country}</p>
        <p><b>🛂 Víza:</b> {result.get("visa_name", "N/A")}</p>
        <p><b>⏳ Délka:</b> {result.get("visa_duration", "N/A")}</p>

        <p><b>🎨 Kategorie:</b> 
        <span style="background:{color};color:white;padding:4px 8px;border-radius:6px;">
        {result.get("visa_color", "N/A")}
        </span>
        </p>

        <p><b>🧠 Zdroj:</b> {result.get("source", "N/A")}</p>

        <hr>

        <p style="font-size:12px;color:#666;">
        🕒 Aktuální čas (CZ): {cz_time.strftime('%Y-%m-%d %H:%M:%S')}
        </p>

        <p style="font-size:12px;color:#666;">
        💾 Uloženo do cache: {result.get("generated_at", "N/A")}
        </p>
    </div>
    """

    # 🔥 KLÍČOVÝ FIX
    st.markdown(html, unsafe_allow_html=True)
