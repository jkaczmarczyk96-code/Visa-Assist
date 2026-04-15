import requests
import json
import os
import time
import streamlit as st

CACHE_FILE = "cache.json"
CACHE_TTL = 60 * 60 * 24 * 30


# =========================
# 🌍 NORMALIZE
# =========================
def normalize_country(c):
    return c.strip().upper()


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
# 🌐 RAPIDAPI v2 FULL
# =========================
def api(passport, country):
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

        r = requests.post(url, headers=headers, json=payload, timeout=10)

        if r.status_code == 200:
            data = r.json().get("data", {})

            rules = data.get("visa_rules", {})
            primary = rules.get("primary_rule", {})
            secondary = rules.get("secondary_rule", {})
            registration = data.get("mandatory_registration", {})
            exceptions = data.get("exception_rules", [])
            dest = data.get("destination", {})

            return {
                # VISA
                "visa_name": primary.get("name"),
                "visa_duration": primary.get("duration"),
                "visa_color": primary.get("color"),

                # SECONDARY
                "secondary_name": secondary.get("name"),
                "secondary_duration": secondary.get("duration"),

                # REGISTRATION
                "registration": registration.get("name"),
                "registration_link": registration.get("link"),

                # EXCEPTIONS
                "exceptions": exceptions,

                # DESTINATION DATA
                "country": dest.get("name"),
                "capital": dest.get("capital"),
                "currency": dest.get("currency"),
                "population": dest.get("population"),
                "timezone": dest.get("timezone"),

                # SOURCE
                "source": "RAPIDAPI v2 FULL"
            }

    except Exception as e:
        print("API ERROR:", e)

    return None


# =========================
# 🧠 FALLBACK (NO UNKNOWN)
# =========================
def fallback(passport, country):

    if passport in ["CZ", "SK"] and country in ["DE","FR","IT","ES","AT","NL","BE","PT","GR"]:
        return {
            "visa_name": "Visa-free (Schengen)",
            "visa_duration": "90 days",
            "visa_color": "green",
            "source": "RULE ENGINE"
        }

    return {
        "visa_name": "Estimated visa required",
        "visa_duration": "90 days",
        "visa_color": "yellow",
        "source": "GLOBAL RULES"
    }


# =========================
# 🧠 MAIN ENGINE
# =========================
def get(passport, country):

    country = normalize_country(country)

    cache = load_cache()
    key = f"{passport}_{country}"
    now = time.time()

    if key in cache:
        if now - cache[key]["time"] < CACHE_TTL:
            return cache[key]["data"]

    result = api(passport, country)

    if not result:
        result = fallback(passport, country)

    cache[key] = {"data": result, "time": now}
    save_cache(cache)

    return result
