import streamlit as st
from engine import get
from countries import COUNTRIES_100


# =========================
# ⚙️ PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Visa Assist",
    layout="wide",
    page_icon="🛂"
)


# =========================
# 🎨 EUROP ASSISTANCE STYLE
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #F3F6FA;
    color: #1B1F2A;
    font-family: Arial;
}

/* HERO */
.hero {
    background: linear-gradient(90deg, #0B2E59, #163B73);
    padding: 40px;
    border-radius: 18px;
    color: white;
}

/* TITLE */
.title {
    font-size: 48px;
    font-weight: 900;
}

.subtitle {
    font-size: 16px;
    opacity: 0.9;
}

/* CARD */
.card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    border-left: 8px solid #0B2E59;
}

/* BOXES */
.box {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #E6EAF0;
}

/* STATUS */
.green { color: #1AAE6F; font-weight: bold; }
.blue { color: #2F6FED; font-weight: bold; }
.yellow { color: #B8860B; font-weight: bold; }
.red { color: #E30613; font-weight: bold; }

hr {
    border: none;
    height: 1px;
    background: #E6EAF0;
}
</style>
""", unsafe_allow_html=True)


# =========================
# HERO SECTION (HOMEPAGE)
# =========================
st.markdown("""
<div class="hero">
    <div class="title">🛂 Visa Assist</div>
    <div class="subtitle">
        Cestovní vízová asistence v reálném čase — jako Europ Assistance
    </div>
</div>
""", unsafe_allow_html=True)


st.write("")
st.write("")


# =========================
# INFO BLOCKS (HOMEPAGE)
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="box">
    🌍 <b>195+ zemí</b><br>
    Globální pokrytí vízových pravidel
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="box">
    ⚡ <b>Realtime data</b><br>
    Napojení na Travel Buddy API
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="box">
    🧠 <b>Inteligentní fallback</b><br>
    Funguje i bez API odpovědi
    </div>
    """, unsafe_allow_html=True)


st.write("")
st.write("")


# =========================
# CHECK VISA SECTION
# =========================
st.markdown("## 🧭 Zkontrolujte vízové podmínky")

col1, col2 = st.columns(2)

with col1:
    passport = st.selectbox("Občanství", ["CZ", "SK"])

with col2:
    country = st.selectbox(
        "Cílová země",
        list(COUNTRIES_100.keys()),
        format_func=lambda x: COUNTRIES_100[x]
    )


# =========================
# RESULT
# =========================
if st.button("🔍 Zkontrolovat vstupní podmínky"):

    result = get(passport, country)

    visa = result.get("visa_name", "Neznámé")
    duration = result.get("visa_duration", "N/A")
    source = result.get("source", "N/A")
    color = result.get("visa_color", "yellow")

    st.write("")
    st.markdown("## ✈️ Výsledek cestovní kontroly")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="box">
        🌍 <b>Cílová země:</b> {COUNTRIES_100[country]}<br>
        🛂 <b>Vízový režim:</b> {visa}<br>
        ⏱ <b>Délka pobytu:</b> {duration}
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # =========================
    # STATUS
    # =========================
    st.markdown("### 📊 Status vstupu")

    if color == "green":
        st.markdown('<div class="green">🟢 Bez vízové povinnosti</div>', unsafe_allow_html=True)
        st.markdown("Cestování je možné bez víza.")

    elif color == "blue":
        st.markdown('<div class="blue">🔵 Víza po příletu / eVisa</div>', unsafe_allow_html=True)
        st.markdown("Víza lze získat po příletu nebo online.")

    elif color == "yellow":
        st.markdown('<div class="yellow">🟡 Elektronická autorizace (ETA)</div>', unsafe_allow_html=True)
        st.markdown("Je nutná online registrace před cestou.")

    else:
        st.markdown('<div class="red">🔴 Vízová povinnost</div>', unsafe_allow_html=True)
        st.markdown("Je nutné vyřídit vízum před cestou.")

    st.write("")

    # =========================
    # SOURCE
    # =========================
    st.markdown("---")
    st.write("📡 Zdroj dat:", source)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# FOOTER
# =========================
st.write("")
st.markdown("""
<hr>
<div style="text-align:center;color:#6B7280;">
Visa Assist • Travel intelligence platform • Europ Assistance style prototype
</div>
""", unsafe_allow_html=True)
