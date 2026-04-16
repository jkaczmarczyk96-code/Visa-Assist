import streamlit as st
from engine import process_query
from datetime import datetime
from zoneinfo import ZoneInfo
from openai import OpenAI, RateLimitError
import os
import time


# =========================
# 🔑 API KEYS
# =========================
def get_api_key(name):
    if name in st.secrets:
        return st.secrets[name]
    return os.getenv(name)


OPENAI_API_KEY = get_api_key("OPENAI_API_KEY")
RAPID_API_KEY = get_api_key("TRAVEL_BUDDY_API_KEY")

if not RAPID_API_KEY:
    st.error("❌ Chybí TRAVEL_BUDDY_API_KEY")
    st.stop()

openai_client = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)


# =========================
# 🕒 TIME
# =========================
def get_cz_time():
    return datetime.now(ZoneInfo("Europe/Prague"))


# =========================
# 🌍 MZV LINK
# =========================
def get_mzv_link(country, passport):
    if not country:
        return None

    slug = country.lower().replace(" ", "-")

    if passport == "CZ":
        return f"https://www.mzv.cz/jnp/cz/encyklopedie_statu/{slug}.html"

    if passport == "SK":
        return f"https://www.mzv.sk/web/sk/cestovanie-a-konzularne-info/{slug}"

    return None


# =========================
# ⚙️ PAGE
# =========================
st.set_page_config(page_title="Visa AI Chatbot", page_icon="🌍")

st.title("🌍 Visa AI asistent")
st.caption("Zeptej se na vízové podmínky")

st.divider()


# =========================
# SETTINGS
# =========================
use_ai = st.checkbox("🤖 Použít AI odpověď", value=True)
debug_mode = st.checkbox("🐞 Debug režim")


# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_input" not in st.session_state:
    st.session_state.last_input = ""

if "last_call" not in st.session_state:
    st.session_state.last_call = 0


# =========================
# CHAT HISTORY
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# =========================
# AI RESPONSE
# =========================
def generate_ai_response(user_input, data):

    if not openai_client:
        return None

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            timeout=10,
            temperature=0.4,
            messages=[
                {"role": "system", "content": "Jsi asistent pro vízové informace. Odpovídej česky stručně."},
                {"role": "user", "content": user_input},
                {
                    "role": "system",
                    "content": f"""
                    Země: {data.get("country")}
                    Pas: {data.get("passport")}
                    Typ víza: {data.get("visa_type")}
                    Pobyt: {data.get("duration")}
                    """
                }
            ]
        )

        return response.choices[0].message.content

    except RateLimitError:
        return None

    except Exception:
        return None


# =========================
# FALLBACK
# =========================
def fallback_answer(data):
    return f"""
🌍 **{data.get('country')}**

🛂 Typ víza: {data.get('visa_type')}
⏳ Maximální pobyt: {data.get('duration')}

📌 Zdroj: {data.get('source')}

ℹ️ Doporučujeme ověřit aktuální podmínky na stránkách MZV.
"""


# =========================
# INPUT
# =========================
user_input = st.chat_input("Napiš dotaz...")


if user_input and user_input.strip() != "":

    # DUPLICATE FIX
    if user_input == st.session_state.last_input:
        st.stop()
    st.session_state.last_input = user_input

    # RATE LIMIT
    if time.time() - st.session_state.last_call < 2:
        st.warning("⏳ Počkej chvíli...")
        st.stop()
    st.session_state.last_call = time.time()

    # USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # LOADING
    status = st.empty()
    status.info("⏳ Zpracovávám...")

    # ENGINE
    result = process_query(user_input, RAPID_API_KEY)

    # RESPONSE
    if result.get("error"):
        answer = result["error"]
        status.error(answer)

    else:
        if use_ai:
            ai_answer = generate_ai_response(user_input, result)

            if ai_answer:
                answer = ai_answer
            else:
                answer = fallback_answer(result)
                status.warning("AI nedostupná – použita základní odpověď")
        else:
            answer = fallback_answer(result)

        status.empty()

        with st.chat_message("assistant"):
            st.write(answer)

            # =========================
            # ⚠️ VAROVÁNÍ
            # =========================
            if result.get("status") in ["evisa", "unknown"]:
                st.warning("⚠️ Podmínky se mohou lišit. Ověř informace na MZV.")

            # =========================
            # 🌍 MZV LINK
            # =========================
            mzv_link = get_mzv_link(
                result.get("country"),
                result.get("passport")
            )

            if mzv_link:
                st.markdown(f"🔗 Oficiální informace MZV: {mzv_link}")

    # SAVE
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # DEBUG
    if debug_mode:
        with st.expander("🐞 Debug"):
            for line in result.get("debug", []):
                st.write(line)
            st.json(result)


# =========================
# API STATUS
# =========================
with st.expander("🔑 API status"):
    st.write("OpenAI:", bool(OPENAI_API_KEY))
    st.write("RapidAPI:", bool(RAPID_API_KEY))
