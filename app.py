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
# 🎨 STYLE (EUROP + ANIMACE)
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

/* ANIMATION CARD */
.status-card {
    animation: fadeIn 0.6s ease-in-out;
    transition: all 0.3s ease;
    font-family: Arial, sans-serif;
}

.status-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 18px 40px rgba(0,0,0,0.18);
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* select */
div[data-baseweb="select"] {
    background: white;
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

    # =========================
    # MAPA STAVŮ
    # =========================
    status_map = {
        "green": ("#2ecc71", "🟢 Bez víza"),
        "blue": ("#3498db", "🔵 Víza při příjezdu / eVisa"),
        "yellow": ("#f1c40f", "🟡 eTA / registrace"),
        "red": ("#e74c3c", "🔴 Víza nutná")
    }

    color, label = status_map.get(
        result.get("visa_color"),
        ("#999", "⚪ Neznámé")
    )

    # =========================
    # IKONY
    # =========================
    icon_map = {
        "green": "🟢",
        "blue": "🔵",
        "yellow": "🟡",
        "red": "🔴"
    }

    icon = icon_map.get(result.get("visa_color"), "⚪")

    # =========================
    # HTML CARD
    # =========================
    html = f"""
    <div class="status-card" style="
        background:{color};
        color:white;
        padding:28px;
        border-radius:18px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
        margin-top:20px;
    ">

        <h2 style="margin:0;">{icon} {country}</h2>

        <h3 style="margin:5px 0 15px 0;">
            {label}
        </h3>

        <p style="font-size:16px;margin:6px 0;">
            🛂 {result.get("visa_name", "N/A")}
        </p>

        <p style="font-size:16px;margin:6px 0;">
            ⏳ {result.get("visa_duration", "N/A")}
        </p>

        <hr style="border:none;height:1px;background:rgba(255,255,255,0.3);">

        <p style="font-size:13px;margin:4px 0;">
            🧠 Zdroj: {result.get("source")}
        </p>

        <p style="font-size:12px;margin:4px 0;">
            🕒 CZ čas: {cz_time.strftime('%Y-%m-%d %H:%M:%S')}
        </p>

        <p style="font-size:12px;margin:4px 0;">
            💾 Cache: {result.get("generated_at")}
        </p>

    </div>
    """

    st.markdown(html, unsafe_allow_html=True)
