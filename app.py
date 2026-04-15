import streamlit as st
from engine import get
from countries import COUNTRIES_100


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Visa Assist",
    layout="wide",
    page_icon="🛂"
)


# =========================
# STYLE (CLEAN EUROP ASSISTANCE)
# =========================
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background-color: #F3F6FA;
    color: #1B1F2A;
    font-family: Arial;
}

/* HERO */
.hero {
    background: linear-gradient(90deg, #0B2E59, #163B73);
    padding: 28px;
    border-radius: 16px;
    color: white;
}

/* TITLE */
.title {
    font-size: 42px;
    font-weight: 900;
}

.subtitle {
    font-size: 14px;
    opacity: 0.9;
}

/* CARD */
.card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    border-left: 6px solid #0B2E59;
}

/* INFO */
.box {
    background: white;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #E6EAF0;
}

/* STATUS */
.green { color: #1AAE6F; font-weight: bold; }
.blue { color: #2F6FED; font-weight: bold; }
.yellow { color: #B8860B; font-weight: bold; }
.red { color: #E30613; font-weight: bold; }

/* BUTTON FIX (NE ČERNÉ!) */
.stButton > button {
    background-color: #0B2E59;
    color: white;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background-color: #163B73;
    color: white;
}

hr {
    border: none;
    height: 1px;
    background: #E6EAF0;
}

</style>
""", unsafe_allow_html=True)


# =========================
# HERO
# =========================
st.markdown("""
<div class="hero">
    <div class="title">🛂 Visa Assist</div>
    <div class="subtitle">Asistent pro vyhledání víz</div>
</div>
""", unsafe_allow_html=True)


st.write("")


# =========================
# INPUT SECTION (COMPACT)
# =========================
st.markdown("### 🧭 Kontrola vstupních podmínek")

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
# ACTION
# =========================
result = None

if st.button("🔍 Zkontrolovat vízové podmínky"):
    result = get(passport, country)


# =========================
# OUTPUT (ONLY IF DATA EXISTS)
# =========================
if result:

    visa = result.get("visa_name", "Neznámé")
    duration = result.get("visa_duration", "N/A")
    source = result.get("source", "")
    color = result.get("visa_color", "yellow")

    st.write("")
    st.markdown("## ✈️ Výsledek")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="box">
        🌍 <b>Země:</b> {COUNTRIES_100[country]}<br>
        🛂 <b>Vízový režim:</b> {visa}<br>
        ⏱ <b>Délka pobytu:</b> {duration}
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("### 📊 Status")

    if color == "green":
        st.markdown('<div class="green">🟢 Bez vízové povinnosti</div>', unsafe_allow_html=True)

    elif color == "blue":
        st.markdown('<div class="blue">🔵 Víza po příletu / eVisa</div>', unsafe_allow_html=True)

    elif color == "yellow":
        st.markdown('<div class="yellow">🟡 ETA / registrace před cestou</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="red">🔴 Vízová povinnost</div>', unsafe_allow_html=True)

    if source:
        st.markdown("---")
        st.write("📡 Zdroj:", source)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    # žádná prázdná tabulka / žádný output
    st.write("")
