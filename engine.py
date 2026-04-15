import requests
import json
import os
import time
import streamlit as st

CACHE_FILE = "cache.json"
CACHE_TTL = 60 * 60 * 24 * 30  # 30 dní


# ======================
# CACHE (disk)
# ======================
def load_cache():
    if os.path.exists(CACHE_FILE):
        return json.load(open(CACHE_FILE, "r", encoding="utf-8"))
    return {}


def save_cache(cache):
    json.dump(cache, open(CACHE_FILE, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)


# ======================
# API
# ======================
def api(passport, country):
    try:
        api_key = st.secrets.get("TRAVEL_BUDDY_API_KEY", None)

        r = requests.get(
            "https://api.travel-buddy.ai/v2/visa/check",
            headers={"Authorization": f"Bearer {api_key}"},
            params={
                "passport": passport,
                "destination": country
            },
            timeout=5
        )

        if r.status_code == 200:
            d = r.json()
            return {
                "visa": d.get("visa_required"),
                "days": d.get("stay_days"),
                "source": "API"
            }
    except:
        pass

    return None


# ======================
# WIKI FALLBACK (LIGHT)
# ======================
def wiki(passport, country):
    try:
        url = f"https://en.wikipedia.org/wiki/Visa_requirements_for_{passport}_citizens"
        r = requests.get(url, timeout=5)

        if country.lower() in r.text.lower():
            return {
                "visa": None,
                "days": 0,
                "source": "WIKIPEDIA"
            }
    except:
        pass

    return None


# ======================
# 🚀 HLAVNÍ FUNKCE (STREAMLIT CACHE)
# ======================
@st.cache_data(ttl=60*60*24*30)
def get(passport, country):

    cache = load_cache()
    key = f"{passport}_{country}"
    now = time.time()

    # CACHE HIT (disk)
    if key in cache:
        item = cache[key]
        if now - item["time"] < CACHE_TTL:
            return item["data"]

    # API
    result = api(passport, country)

    # WIKI fallback
    if not result:
        result = wiki(passport, country)

    # FINAL fallback
    if not result:
        result = {
            "visa": None,
            "days": 0,
            "source": "UNKNOWN"
        }

    cache[key] = {
        "data": result,
        "time": now
    }

    save_cache(cache)

    return result


# ======================
# 🚀 FAST BATCH (PRO MAPU)
# ======================
@st.cache_data(ttl=60*60*24*30)
def get_many(passport, countries):

    results = {}

    for c in countries:
        results[c] = get(passport, c)

    return results
