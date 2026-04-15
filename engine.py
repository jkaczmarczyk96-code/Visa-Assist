import requests
import json
import os
import time
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

CACHE_FILE = "cache.json"
CACHE_TTL = 60 * 60 * 24 * 30


# =========================
# 🕒 CZ TIME
# =========================
def get_cz_time():
    return datetime.now(ZoneInfo("Europe/Prague"))


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
# 🌍 ISO MAP
# =========================
ISO_API = {
    "Egypt": "EG",
    "United Arab Emirates": "AE",
    "United States": "US",
    "Czech Republic": "CZ",
    "Slovakia": "SK",
    "Germany": "DE",
    "France": "FR",
    "Italy": "IT",
    "Spain": "ES",
    "Thailand": "TH",
    "Japan": "JP",
    "China": "CN",
    "Turkey": "TR",
    "Canada": "CA"
}


def normalize_for_api(value):
    return ISO_API.get(value, value)


# =========================
# 🌐 API
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
            "passport": normalize_for_api(passport),
            "destination": normalize_for_api(country)
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

    except Exception as e:
        print("API ERROR:", e)

    return None


# =========================
# 🌍 FALLBACK API
# =========================
def travelbriefing_api(country):
    try:
        url = f"https://travelbriefing.org/{country.replace(' ', '_')}?format=json"

        r = requests.get(url, timeout=8)

        if r.status_code == 200:
            data = r.json()
            visa_data = data.get("visa")

            if isinstance(visa_data, dict):
                visa = visa_data.get("info", "Visa info available")
            else:
                visa = visa_data or "Visa info available"

            return {
                "visa_name": visa,
                "visa_duration": "See details",
                "visa_color": "blue",
                "source": "TravelBriefing"
            }

    except Exception as e:
        print("TravelBriefing ERROR:", e)

    return None


# =========================
# 🧠 RULE ENGINE
# =========================
def rule_engine(passport, country):

    rules = {
        ("CZ", "Egypt"): ("Visa on arrival / eVisa", "30 days", "blue"),
        ("SK", "Egypt"): ("Visa on arrival / eVisa", "30 days", "blue"),
    }

    key = (passport, country)

    if key in rules:
        visa, duration, color = rules[key]

        return {
            "visa_name": visa,
            "visa_duration": duration,
            "visa_color": color,
            "source": "Rule Engine"
        }

    return None


# =========================
# 🚀 MAIN
# =========================
def get(passport, country):

    cache = load_cache()
    key = f"{passport}_{country}"
    now = time.time()

    # =========================
    # CACHE HIT
    # =========================
    if key in cache:
        if now - cache[key]["time"] < CACHE_TTL:
            cached_data = cache[key]["data"]

            # ✔ použij čas zápisu
            cached_data["generated_at"] = cache[key].get("created_at_cz")

            return cached_data

    # =========================
    # API
    # =========================
    result = travel_buddy_api(passport, country)

    # =========================
    # FALLBACK API
    # =========================
    if not result:
        result = travelbriefing_api(country)

    # =========================
    # RULE ENGINE
    # =========================
    if not result:
        result = rule_engine(passport, country)

    # =========================
    # FINAL FALLBACK
    # =========================
    if not result:
        result = {
            "visa_name": "Visa rules vary",
            "visa_duration": "Check embassy",
            "visa_color": "yellow",
            "source": "Global fallback"
        }

    # =========================
    # 🕒 TIME
    # =========================
    cz_time = get_cz_time()
    cz_str = cz_time.strftime("%Y-%m-%d %H:%M:%S")

    result["generated_at"] = cz_str

    # =========================
    # 💾 CACHE WRITE
    # =========================
    cache[key] = {
        "data": result,
        "time": now,
        "created_at_cz": cz_str,
        "created_at_iso": cz_time.isoformat()
    }

    save_cache(cache)

    return result
