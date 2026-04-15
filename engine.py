import requests
import json
import os
import time
import streamlit as st

CACHE_FILE = "cache.json"
CACHE_TTL = 60 * 60 * 24 * 30  # 30 dní


# =========================
# 💾 CACHE
# =========================
def load_cache():
    if os.path.exists(CACHE_FILE):
        return json.load(open(CACHE_FILE, "r", encoding="utf-8"))
    return {}


def save_cache(cache):
    json.dump(cache, open(CACHE_FILE, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)


# =========================
# 🌍 RULE BASE (GARANTOVANÝ FALLBACK)
# =========================
VISA_RULES = {
    "CZ": {
        "DE": {"visa": False, "days": 90},
        "FR": {"visa": False, "days": 90},
        "IT": {"visa": False, "days": 90},
        "ES": {"visa": False, "days": 90},
        "US": {"visa": True, "days": 90},
        "JP": {"visa": False, "days": 90},
        "TH": {"visa": False, "days": 30},
        "AE": {"visa": False, "days": 90},
    },
    "SK": {
        "DE": {"visa": False, "days": 90},
        "FR": {"visa": False, "days": 90},
        "IT": {"visa": False, "days": 90},
        "ES": {"visa": False, "days": 90},
        "US": {"visa": True, "days": 90},
        "JP": {"visa": False, "days": 90},
        "TH": {"visa": False, "days": 30},
        "AE": {"visa": False, "days": 90},
    }
}


# =========================
# 🌐 API (TRAVEL BUDDY)
# =========================
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


# =========================
# 🧠 MAIN ENGINE (NO UNKNOWN)
# =========================
def get(passport, country):

    cache = load_cache()
    key = f"{passport}_{country}"
    now = time.time()

    # CACHE HIT
    if key in cache:
        item = cache[key]
        if now - item["time"] < CACHE_TTL:
            return item["data"]

    # 1) API
    result = api(passport, country)

    # 2) RULE BASE
    if not result:
        result = VISA_RULES.get(passport, {}).get(country)

    # 3) GLOBAL SAFE FALLBACK
    if not result:
        result = {
            "visa": False,
            "days": 90,
            "source": "DEFAULT RULE (SAFE FALLBACK)"
        }

    # SAVE CACHE
    cache[key] = {
        "data": result,
        "time": now
    }

    save_cache(cache)

    return result
