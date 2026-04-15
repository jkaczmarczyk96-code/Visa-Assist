import requests
import json
import os
import time
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from countries import to_api_format


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
# 🎨 COLOR DETECTION
# =========================
def detect_color(text):
    t = (text or "").lower()

    if "visa free" in t or "without visa" in t:
        return "green"
    if "visa on arrival" in t:
        return "blue"
    if "evisa" in t:
        return "yellow"
    if "visa required" in t:
        return "red"

    return "yellow"


# =========================
# ⏳ DURATION PARSER
# =========================
def extract_max_stay(text):
    if not text:
        return "Unknown"

    t = text.lower()

    if "90" in t:
        return "Up to 90 days"
    if "30" in t:
        return "Up to 30 days"
    if "180" in t:
        return "Up to 180 days"

    return text


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
            "passport": to_api_format(passport),
            "destination": to_api_format(country)
        }

        r = requests.post(url, headers=headers, json=payload, timeout=8)

        if r.status_code == 200:
            data = r.json().get("data", {})
            rules = data.get("visa_rules", {})
            primary = rules.get("primary_rule", {})

            return {
                "visa_name": primary.get("name"),
                "visa_duration": primary.get("duration"),
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
            visa = data.get("visa")

            text = visa.get("info") if isinstance(visa, dict) else visa

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
        ("CZ", "Egypt"): ("Visa on arrival", "30 days", "blue"),
        ("SK", "Egypt"): ("Visa on arrival", "30 days", "blue"),
        ("CZ", "Japan"): ("Visa free", "90 days", "green"),
        ("SK", "Japan"): ("Visa free", "90 days", "green"),
    }

    if (passport, country) in rules:
        v, d, c = rules[(passport, country)]
        return {
            "visa_name": v,
            "visa_duration": d,
            "visa_color": c,
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

    debug = []

    # =========================
    # CACHE
    # =========================
    if key in cache and now - cache[key]["time"] < CACHE_TTL:
        debug.append("⚡ Cache HIT")

        data = cache[key]["data"]
        data["debug"] = debug
        return data

    debug.append("🆕 Cache MISS")

    # =========================
    # API PIPELINE
    # =========================
    result = travel_buddy_api(passport, country)
    debug.append("✔ Travel Buddy API used" if result else "❌ Travel Buddy API failed")

    if not result:
        result = travelbriefing_api(country)
        debug.append("✔ TravelBriefing used" if result else "❌ TravelBriefing failed")

    if not result:
        result = rule_engine(passport, country)
        debug.append("✔ Rule engine used" if result else "❌ Rule engine not matched")

    if not result:
        debug.append("⚠ Using fallback")
        result = {
            "visa_name": "Visa rules vary",
            "visa_duration": "Check embassy",
            "visa_color": "yellow",
            "source": "Fallback"
        }

    # =========================
    # POST PROCESS
    # =========================
    combined = f"{result.get('visa_name')} {result.get('visa_duration')}"

    result["visa_color"] = detect_color(combined)
    result["visa_duration"] = extract_max_stay(result.get("visa_duration"))

    # =========================
    # TIME + DEBUG
    # =========================
    result["generated_at"] = get_cz_time().strftime("%Y-%m-%d %H:%M:%S")
    result["debug"] = debug

    # =========================
    # CACHE SAVE
    # =========================
    cache[key] = {
        "data": result,
        "time": now
    }

    save_cache(cache)

    return result
