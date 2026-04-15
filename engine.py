import requests
import json
import os
import time
import streamlit as st

CACHE_FILE = "cache.json"
CACHE_TTL = 60 * 60 * 24 * 30


# =========================
# 💾 CACHE SYSTEM
# =========================
def load_cache():
    if os.path.exists(CACHE_FILE):
        return json.load(open(CACHE_FILE, "r", encoding="utf-8"))
    return {}


def save_cache(cache):
    json.dump(cache, open(CACHE_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


# =========================
# 🌍 ISO MAP (CRITICAL FIX)
# =========================
ISO_MAP = {
    "Czech Republic": "CZ",
    "Slovakia": "SK",
    "Germany": "DE",
    "France": "FR",
    "Italy": "IT",
    "Spain": "ES",
    "Portugal": "PT",
    "Egypt": "EG",
    "United Arab Emirates": "AE",
    "United States": "US",
    "Canada": "CA",
    "United Kingdom": "GB",
    "Japan": "JP",
    "China": "CN",
    "Thailand": "TH",
    "Vietnam": "VN",
    "Turkey": "TR"
}


# =========================
# 🧠 NORMALIZER
# =========================
def normalize_country(country):
    return ISO_MAP.get(country, country.replace(" ", "_"))


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
        url = f"https://travelbriefing.org/{normalize_country(country)}?format=json"

        r = requests.get(url, timeout=8)

        if r.status_code == 200:
            data = r.json()

            visa_data = data.get("visa")

            # FIX: string OR dict
            if isinstance(visa_data, dict):
                visa = visa_data.get("info", "Visa information available")
            else:
                visa = visa_data if visa_data else "Visa information available"

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
# 🧠 3. RULE ENGINE (EDGE CASE FIXES)
# =========================
def rule_engine(passport, country):

    rules = {

        ("CZ", "Germany"): ("Visa-free (Schengen)", "90 days", "green"),
        ("CZ", "France"): ("Visa-free (Schengen)", "90 days", "green"),
        ("CZ", "Italy"): ("Visa-free (Schengen)", "90 days", "green"),
        ("CZ", "Spain"): ("Visa-free (Schengen)", "90 days", "green"),

        ("CZ", "Egypt"): ("Visa on arrival / eVisa", "30 days", "blue"),
        ("SK", "Egypt"): ("Visa on arrival / eVisa", "30 days", "blue"),

        ("CZ", "United Arab Emirates"): ("Visa-free / visa on arrival", "30 days", "blue"),

        ("CZ", "Thailand"): ("Visa-free", "30 days", "green"),

        ("CZ", "United States"): ("ESTA required", "90 days", "yellow"),
        ("CZ", "Canada"): ("eTA required", "180 days", "yellow"),

        ("CZ", "United Kingdom"): ("ETA / visa rules apply", "180 days", "yellow"),

        ("CZ", "Japan"): ("Visa-free", "90 days", "green"),

        ("CZ", "China"): ("Visa required", "varies", "red"),
    }

    key = (passport, country)

    if key in rules:
        visa, duration, color = rules[key]

        return {
            "visa_name": visa,
            "visa_duration": duration,
            "visa_color": color,
            "source": "Rule Engine (offline fallback)"
        }

    return None


# =========================
# 🚀 MAIN ENGINE
# =========================
def get(passport, country):

    cache = load_cache()
    key = f"{passport}_{country}"
    now = time.time()

    # CACHE
    if key in cache:
        if now - cache[key]["time"] < CACHE_TTL:
            return cache[key]["data"]

    # NORMALIZE INPUT FOR API
    country_api = normalize_country(country)

    # 1. PRIMARY API
    result = travel_buddy_api(passport, country_api)

    # 2. FREE API
    if not result:
        result = travelbriefing_api(country)

    # 3. RULE ENGINE
    if not result:
        result = rule_engine(passport, country)

    # 4. FINAL SAFE FALLBACK
    if not result:
        result = {
            "visa_name": "Visa rules vary",
            "visa_duration": "Check embassy",
            "visa_color": "yellow",
            "source": "Global fallback system"
        }

    cache[key] = {"data": result, "time": now}
    save_cache(cache)

    return result
