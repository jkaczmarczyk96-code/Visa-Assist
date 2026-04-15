import requests
import json
import os
import time
import streamlit as st
from bs4 import BeautifulSoup

CACHE_FILE = "cache.json"
CACHE_TTL = 60 * 60 * 24 * 30  # 30 dní


# ======================
# CACHE
# ======================
def load_cache():
    if os.path.exists(CACHE_FILE):
        return json.load(open(CACHE_FILE, "r", encoding="utf-8"))
    return {}


def save_cache(cache):
    json.dump(cache, open(CACHE_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


# ======================
# API (TRAVEL BUDDY)
# ======================
def api(passport, country):

    try:
        api_key = st.secrets["TRAVEL_BUDDY_API_KEY"]

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
# WIKIPEDIA FALLBACK
# ======================
def wiki(passport, country):
    try:
        url = f"https://en.wikipedia.org/wiki/Visa_requirements_for_{passport}_citizens"
        r = requests.get(url, timeout=10)

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
# HLAVNÍ LOGIKA
# ======================
def get(passport, country):

    cache = load_cache()
    key = f"{passport}_{country}"
    now = time.time()

    # CACHE (30 dní)
    if key in cache:
        item = cache[key]
        if now - item["time"] < CACHE_TTL:
            return item["data"]

    # API
    result = api(passport, country)

    # FALLBACK
    if not result:
        result = wiki(passport, country)

    # FINAL
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
