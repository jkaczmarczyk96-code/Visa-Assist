import streamlit as st
from engine import get
from countries import COUNTRIES

# =========================
# ⚙️ PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Visa Assist",
    page_icon="🌍",
    layout="centered"
)

# =========================
# 🎨 SIMPLE CLEAN UI STYLE
# =========================
st.markdown("""
    <style>
    body {
        background-color: #f5f7fb;
    }
    .main-title {
        font-size: 36px;
        font-weight: 700;
        color: #1f4e79;
    }
    .subtext {
        color: #666;
        font-size: 14px;
    }
    .card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# 🏠 HEADER
# =========================
st.markdown("<div class='main-title'>🌍 Visa Assist</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Zkontroluj vízové podmínky během pár sekund</div>", unsafe_allow_html=True)

st.divider()

# =========================
# 📥 INPUTS
# =========================
passport = st.selectbox("🛂 Pas:", ["CZ", "SK"])

country = st.selectbox("🌍 Cílová země:", COUNTRIES)

# =========================
# 🚀 ACTION
# =========================
if st.button("🔍 Zkontrolovat vízové podmínky"):

    with st.spinner("Načítám data..."):
        result = get(passport, country)

    # =========================
    # 🧾 OUTPUT CARD
    # =========================
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📊 Výsledek")

    st.write("🌍 Země:", country)
    st.write("🛂 Víza:", result.get("visa_name", "N/A"))
    st.write("⏳ Délka pobytu:", result.get("visa_duration", "N/A"))
    st.write("🎨 Kategorie:", result.get("visa_color", "N/A"))
    st.write("🧠 Zdroj:", result.get("source", "N/A"))

    # ✔ FIX: datum vždy z engine
    if result.get("generated_at"):
        st.caption(f"🕒 Generováno: {result['generated_at']}")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 🧠 FOOTER
# =========================
st.divider()
st.caption("Visa Assist • Powered by Travel APIs + fallback engine")
