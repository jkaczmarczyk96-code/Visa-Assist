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
    page_title="Visa Assist AI",
    page_icon="🌍",
    layout="centered"
)


# =========================
# 🎨 UI STYLE
# =========================
st.markdown("""
<style>

body {
    background-color: #f4f7fb;
}

.block-container {
    max-width: 900px;
}

.stButton > button {
    background: linear-gradient(90deg,#0b2e4a,#1b4f8a);
    color: white;
    border-radius: 12px;
    font-weight: 600;
    padding: 0.6rem 1.2rem;
    border: none;
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
st.title("🌍 Visa Assist AI")
st.caption("Smart vízový asistent (CZ / SK comparison + AI ready)")

st.divider()


# =========================
# INPUTS
# =========================
country = st.selectbox("🌍 Země", COUNTRIES)

mode = st.radio("📊 Režim", ["Single passport", "Compare CZ vs SK"])


# =========================
# SINGLE MODE
# =========================
if mode == "Single passport":

    passport = st.selectbox("🛂 Pas", ["CZ", "SK"])

    if st.button("🔍 Zkontrolovat"):

        result = get(passport, country)
        cz_time = get_cz_time()

        status_map = {
            "green": ("Visa-free", "#2ecc71"),
            "blue": ("Visa on arrival / eVisa", "#3498db"),
            "yellow": ("eTA / Authorization required", "#f1c40f"),
            "red": ("Visa required", "#e74c3c")
        }

        label, color = status_map.get(result["visa_color"], ("Unknown", "#999"))

        confidence_map = {
            "Travel Buddy API": 95,
            "TravelBriefing": 80,
            "Rule Engine": 70,
            "Fallback system": 40
        }

        confidence = confidence_map.get(result.get("source"), 50)

        # =========================
        # CARD
        # =========================
        st.markdown(f"""
        <div style="
            background:{color};
            padding:28px;
            border-radius:20px;
            color:white;
            box-shadow: 0 12px 35px rgba(0,0,0,0.18);
            margin-top:20px;
        ">

            <h2>{country}</h2>
            <h3>{label}</h3>

            <hr style="border:none;height:1px;background:rgba(255,255,255,0.3);">

            <p><b>Visa type:</b> {result.get("visa_name")}</p>
            <p><b>Max stay:</b> {result.get("visa_duration")}</p>
            <p><b>Confidence:</b> {confidence}%</p>

            <hr style="border:none;height:1px;background:rgba(255,255,255,0.3);">

            <p>Source: {result.get("source")}</p>
            <p>Updated: {result.get("generated_at")}</p>

        </div>
        """, unsafe_allow_html=True)

        # =========================
        # 🤖 AI EXPLAIN (PLACEHOLDER)
        # =========================
        with st.expander("🤖 Explain this result (AI)"):
            st.info(
                f"""
                This result is based on: {result.get('source')}.

                - Visa type: {result.get('visa_name')}
                - Max stay: {result.get('visa_duration')}
                - Status: {label}

                👉 AI explanation layer can be connected here (OpenAI / GPT API).
                """
            )


# =========================
# COMPARE MODE
# =========================
else:

    if st.button("⚖️ Compare CZ vs SK"):

        cz = get("CZ", country)
        sk = get("SK", country)

        def render_card(title, data):
            status_map = {
                "green": ("Visa-free", "#2ecc71"),
                "blue": ("Visa on arrival / eVisa", "#3498db"),
                "yellow": ("eTA required", "#f1c40f"),
                "red": ("Visa required", "#e74c3c")
            }

            label, color = status_map.get(data["visa_color"], ("Unknown", "#999"))

            st.markdown(f"""
            <div style="
                background:{color};
                padding:20px;
                border-radius:16px;
                color:white;
                margin-top:15px;
            ">
                <h3>{title}</h3>
                <p><b>Status:</b> {label}</p>
                <p><b>Visa:</b> {data.get('visa_name')}</p>
                <p><b>Max stay:</b> {data.get('visa_duration')}</p>
                <p><b>Source:</b> {data.get('source')}</p>
            </div>
            """, unsafe_allow_html=True)

        render_card("🇨🇿 Czech Republic passport", cz)
        render_card("🇸🇰 Slovak passport", sk)
