import requests
import json
import os
import time
import streamlit as st

CACHE_FILE = "cache.json"
CACHE_TTL = 60 * 60 * 24 * 30


# =========================
# 💾 CACHE
# =========================
def load_cache():
    if os.path.exists(CACHE_FILE):
        return json.load(open(CACHE_FILE, "r", encoding="utf-8"))
    return {}


def save_cache(cache):
    json.dump(cache, open(CACHE_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


# =========================
# 🌐 1. TRAVEL BUDDY API (PRIMARY)
# =========================
def travel_buddy_api(passport, country):
    try:
        key = st.secrets["TRAVEL_BUDDY_API_KEY"]

        url = "https://visa-requirement.p.rapidapi.com/v2/visa/check"

        headers = {
            "Content-Type": "application/json",
            "x-rapidapi-host": "visa-requirement.p.rapidapi.com",
            "x-rapidapi-key": key
        }

        payload = {
            "passport": passport,
            "destination": country
        }

        r = requests.post(url, headers=headers, json=payload, timeout=8)

        if r.status_code == 200:
            data = r.json().get("data", {})
            rules = data.get("visa_rules", {})
            primary = rules.get("primary_rule", {})
            secondary = rules.get("secondary_rule", {})

            return {
                "visa_name": primary.get("name") or secondary.get("name"),
                "visa_duration": primary.get("duration") or secondary.get("duration"),
                "visa_color": primary.get("color", "yellow"),
                "source": "Travel Buddy API"
            }

    except:
        pass

    return None


# =========================
# 🌍 2. TRAVELBRIEFING API (FREE FALLBACK)
# =========================
def travelbriefing_api(country):
    try:
        # TravelBriefing uses country names with underscore
        url = f"https://travelbriefing.org/{country.replace(' ', '_')}?format=json"

        r = requests.get(url, timeout=8)

        if r.status_code == 200:
            data = r.json()

            visa = data.get("visa", {}).get("info", "Unknown visa rules")

            return {
                "visa_name": visa,
                "visa_duration": "See details",
                "visa_color": "blue",
                "source": "TravelBriefing (FREE fallback)"
            }

    except:
        pass

    return None


# =========================
# 🧠 3. LOCAL FALLBACK (NEVER FAILS)
# =========================
def local_fallback(passport, country):

    if passport in ["CZ", "SK"] and country in ["DE","FR","IT","ES","AT","NL","BE","PT","GR"]:
        return {
            "visa_name": "Visa-free (Schengen)",
            "visa_duration": "90 days",
            "visa_color": "green",
            "source": "Local rules engine"
        }

    return {
        "visa_name": "Visa required (estimated)",
        "visa_duration": "Varies",
        "visa_color": "yellow",
        "source": "Fallback rules"
    }


# =========================
# 🚀 MAIN ENGINE
# =========================
def get(passport, country):

    cache = load_cache()
    key = f"{passport}_{country}"
    now = time.time()

    if key in cache:
        if now - cache[key]["time"] < CACHE_TTL:
            return cache[key]["data"]

    # 1. PRIMARY API
    result = travel_buddy_api(passport, country)

    # 2. FREE FALLBACK API
    if not result:
        result = travelbriefing_api(country)

    # 3. LOCAL FALLBACK
    if not result:
        result = local_fallback(passport, country)

    cache[key] = {"data": result, "time": now}
    save_cache(cache)

    return result
