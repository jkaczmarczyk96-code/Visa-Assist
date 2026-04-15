import streamlit as st
from engine import get
from countries import COUNTRIES_100


# =========================
# 🌐 PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Visa Assist",
    layout="wide",
    page_icon="🛂"
)


# =========================
# 🎨 SHERPA STYLE UI
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #F5F8FC;
}

.title {
    font-size: 44px;
    font-weight: 900;
    color: #0B2E59;
}

.subtitle {
    font-size: 16px;
    color: #E30613;
    margin-bottom: 25px;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.08);
    border-left: 6px solid #0B2E59;
}

.badge-green {
    color: #1AAE6F;
    font-weight: bold;
}

.badge-yellow {
    color: #F4B400;
    font-weight: bold;
}

.badge-red {
    color: #E30613;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================
st.markdown('<div class="title">🛂 Visa Assist</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-time visa intelligence engine (Sherpa style)</div>', unsafe_allow_html=True)


# =========================
# INPUTS
# =========================
col1, col2 = st.columns(2)

with col1:
    passport = st.selectbox("Passport", ["CZ", "SK"])

with col2:
    country = st.selectbox(
        "Destination country",
        list(COUNTRIES_100.keys()),
        format_func=lambda x: COUNTRIES_100[x]
    )


# =========================
# ACTION
# =========================
if st.button("Check visa"):

    result = get(passport, country)

    visa = result.get("visa_name", "Unknown")
    duration = result.get("visa_duration", "N/A")
    source = result.get("source", "UNKNOWN")
    color = result.get("visa_color", "yellow")

    # =========================
    # OUTPUT CARD
    # =========================
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.write("### ✈️ Travel result")

    st.write("🌍 Country:", COUNTRIES_100[country])
    st.write("🛂 Visa type:", visa)
    st.write("⏱ Duration:", duration)

    # COLOR STATUS
    if color == "green":
        st.markdown("Status: 🟢 Visa-free", unsafe_allow_html=True)
    elif color == "blue":
        st.markdown("Status: 🔵 Visa on arrival / eVisa", unsafe_allow_html=True)
    elif color == "yellow":
        st.markdown("Status: 🟡 eTA / conditional entry", unsafe_allow_html=True)
    else:
        st.markdown("Status: 🔴 Visa required", unsafe_allow_html=True)

    # SOURCE
    st.write("📡 Source:", source)

    st.markdown('</div>', unsafe_allow_html=True)
