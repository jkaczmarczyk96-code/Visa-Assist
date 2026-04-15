import streamlit as st
from engine import get

st.set_page_config(page_title="Visa Assist", layout="wide", page_icon="🛂")


# =========================
# 🎨 STYLE (SHERPA STYLE)
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #F5F8FC;
}

.title {
    font-size: 42px;
    font-weight: 900;
    color: #0B2E59;
}

.subtitle {
    color: #E30613;
    font-size: 16px;
    margin-bottom: 20px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    border-left: 6px solid #0B2E59;
}

.green {color: #1AAE6F; font-weight: bold;}
.yellow {color: #F4B400; font-weight: bold;}
.red {color: #E30613; font-weight: bold;}

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================
st.markdown('<div class="title">🛂 Visa Assist</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sherpa-style visa intelligence engine</div>', unsafe_allow_html=True)


# =========================
# INPUT
# =========================
col1, col2 = st.columns(2)

with col1:
    passport = st.selectbox("Passport", ["CZ", "SK"])

with col2:
    country = st.text_input("Destination country (ISO)", "US")


# =========================
# RESULT
# =========================
if st.button("Check visa"):

    data = get(passport, country)

    color = data.get("visa_color", "yellow")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.write("### ✈️ Travel result")

    st.write("Visa:", data.get("visa_name"))
    st.write("Duration:", data.get("visa_duration"))
    st.write("Country:", data.get("country"))

    # COLOR INDICATOR
    st.markdown(f"Status: <span class='{color}'>{color.upper()}</span>", unsafe_allow_html=True)

    # REGISTRATION
    if data.get("registration"):
        st.warning(f"⚠ Mandatory registration: {data['registration']}")

    # EXCEPTIONS
    if data.get("exceptions"):
        st.error("⚠ Exception rules apply")

    st.write("Source:", data.get("source"))

    st.markdown('</div>', unsafe_allow_html=True)
