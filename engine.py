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
# 🕒 TIME
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
# 🌍 ISO NORMALIZER
# =========================
ISO_API = {
    "United States": "US",
    "Czech Republic": "CZ",
    "Slovakia": "SK",
    "United Kingdom": "GB",
    "South Korea": "KR",
    "United Arab Emirates": "AE",
    "Egypt": "EG",
    "Thailand": "TH",
    "Japan": "JP",
    "Canada": "CA"
}


def normalize_country(value):
    return ISO_API.get(value, value)


# =========================
# 🧠 VISA COLOR DETECTOR (IMPROVED)
# =========================
def detect_color(text: str):

    text = (text or "").lower()

    if "visa free" in text or "without visa" in text:
        return "green"

    if "visa on arrival" in text:
        return "blue"

    if "evisa" in text or "electronic visa" in text:
        return "yellow"

    if "visa required" in text:
        return "red"

    return "yellow"


# =========================
# ⏳ MAX STAY PARSER
# =========================
def extract_max_stay(text: str):

    if not text:
        return "Unknown"

    t = text.lower()

    # basic patterns (robust enough for API responses)
    if "90" in t:
        return "Up to 90 days"

    if "30" in t:
        return "Up to 30 days"

    if "180" in t:
        return "Up to 180 days"

    if "365" in t:
        return "Up to 1 year"

    return text


# =========================
# 🌐 TRAVEL BUDDY API
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
            "passport": normalize_country(passport),
            "destination": normalize_country(country)
        }

        r = requests.post(url, headers=headers, json=payload, timeout=8)

        if r.status_code == 200:
            data = r.json().get("data", {})
            rules = data.get("visa_rules", {})
            primary = rules.get("primary_rule", {})
            secondary = rules.get("secondary_rule", {})

            name = primary.get("name") or secondary.get("name")
            duration = primary.get("duration") or secondary.get("duration")
            color = primary.get("color") or "yellow"

            return {
                "visa_name": name,
                "visa_duration": duration,
                "visa_color": color,
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

            text = visa_data.get("info") if isinstance(visa_data, dict) else visa_data

            return {
                "visa_name": text,
                "visa_duration": "Check details",
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
        ("CZ", "Japan"): ("Visa free", "90 days", "green"),
        ("SK", "Japan"): ("Visa free", "90 days", "green"),
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
# 🚀 MAIN ENGINE
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
            return cache[key]["data"]

    # =========================
    # API PIPELINE
    # =========================
    result = travel_buddy_api(passport, country)

    if not result:
        result = travelbriefing_api(country)

    if not result:
        result = rule_engine(passport, country)

    if not result:
        result = {
            "visa_name": "Visa rules vary",
            "visa_duration": "Check embassy",
            "visa_color": "yellow",
            "source": "Fallback system"
        }

    # =========================
    # 🧠 IMPROVEMENT LAYER (FIX DATA QUALITY)
    # =========================

    combined_text = f"{result.get('visa_name','')} {result.get('visa_duration','')}"

    result["visa_color"] = detect_color(combined_text)
    result["visa_duration"] = extract_max_stay(result.get("visa_duration"))

    # timestamp
    cz_time = get_cz_time()
    result["generated_at"] = cz_time.strftime("%Y-%m-%d %H:%M:%S")

    # =========================
    # 💾 CACHE WRITE
    # =========================
    cache[key] = {
        "data": result,
        "time": now
    }

    save_cache(cache)

    return result
