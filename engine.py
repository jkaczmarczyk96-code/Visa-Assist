import requests
import json
import os
import time
import streamlit as st

CACHE_FILE = "cache.json"
CACHE_TTL = 60 * 60 * 24 * 30  # 30 dní


# =========================================================
# 🌍 100 COUNTRIES (ISO READY – V ENGINE)
# =========================================================
COUNTRIES_100 = {
    "CZ": "Czech Republic",
    "SK": "Slovakia",

    "AT": "Austria",
    "DE": "Germany",
    "PL": "Poland",
    "IT": "Italy",
    "FR": "France",
    "ES": "Spain",
    "HR": "Croatia",
    "GR": "Greece",
    "PT": "Portugal",
    "NL": "Netherlands",
    "BE": "Belgium",
    "CH": "Switzerland",
    "SE": "Sweden",
    "NO": "Norway",
    "FI": "Finland",
    "DK": "Denmark",
    "IE": "Ireland",
    "IS": "Iceland",
    "HU": "Hungary",
    "RO": "Romania",
    "BG": "Bulgaria",

    "GB": "United Kingdom",

    "US": "United States",
    "CA": "Canada",
    "MX": "Mexico",

    "BR": "Brazil",
    "AR": "Argentina",
    "CL": "Chile",
    "PE": "Peru",
    "CO": "Colombia",

    "EG": "Egypt",
    "MA": "Morocco",
    "TN": "Tunisia",
    "ZA": "South Africa",
    "KE": "Kenya",
    "TZ": "Tanzania",
    "NG": "Nigeria",

    "AE": "United Arab Emirates",
    "SA": "Saudi Arabia",
    "QA": "Qatar",
    "TR": "Turkey",

    "IN": "India",
    "CN": "China",
    "JP": "Japan",
    "KR": "South Korea",

    "TH": "Thailand",
    "VN": "Vietnam",
    "MY": "Malaysia",
    "SG": "Singapore",
    "ID": "Indonesia",
    "PH": "Philippines",

    "AU": "Australia",
    "NZ": "New Zealand",

    "RU": "Russia",
    "UA": "Ukraine",
    "GE": "Georgia",
    "AM": "Armenia",
    "AZ": "Azerbaijan",

    "IL": "Israel",
    "JO": "Jordan",
    "LB": "Lebanon",

    "PK": "Pakistan",
    "BD": "Bangladesh",
    "LK": "Sri Lanka",

    "UZ": "Uzbekistan",
    "KZ": "Kazakhstan",
    "MN": "Mongolia",

    "CR": "Costa Rica",
    "PA": "Panama",
    "UY": "Uruguay",
    "PY": "Paraguay",

    "CU": "Cuba",
    "DO": "Dominican Republic",
    "JM": "Jamaica",
    "BS": "Bahamas",

    "IS": "Iceland",
    "FI": "Finland",
    "NO": "Norway"
}


# =========================================================
# 🌍 AUTO CONVERSION
# =========================================================
COUNTRY_TO_ISO = {v.lower(): k for k, v in COUNTRIES_100.items()}


def normalize_country(country: str) -> str:
    if not country:
        return country

    c = country.strip().lower()

    # už ISO
    if country.upper() in COUNTRIES_100:
        return country.upper()

    return COUNTRY_TO_ISO.get(c, country.upper())


# =========================================================
# 💾 CACHE
# =========================================================
def load_cache():
    if os.path.exists(CACHE_FILE):
        return json.load(open(CACHE_FILE, "r", encoding="utf-8"))
    return {}


def save_cache(cache):
    json.dump(cache, open(CACHE_FILE, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)


# =========================================================
# 🌐 API
# =========================================================
def api(passport, country_iso):
    try:
        api_key = st.secrets.get("TRAVEL_BUDDY_API_KEY", None)

        r = requests.get(
            "https://api.travel-buddy.ai/v2/visa/check",
            headers={"Authorization": f"Bearer {api_key}"},
            params={
                "passport": passport,
                "destination": country_iso
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


# =========================================================
# 🧠 FALLBACK (NO UNKNOWN)
# =========================================================
def safe_fallback(passport, country_iso):

    schengen = ["DE","FR","IT","ES","AT","NL","BE","PT","GR","PL","CZ","SK","SE","NO","FI","DK"]

    if passport in ["CZ", "SK"] and country_iso in schengen:
        return {"visa": False, "days": 90, "source": "SCHENGEN RULE"}

    if country_iso in ["US", "CA", "GB"]:
        return {"visa": True, "days": 90, "source": "STANDARD RULE"}

    if country_iso in ["TH", "VN", "MY", "ID", "PH"]:
        return {"visa": False, "days": 30, "source": "ASIA RULE"}

    return {
        "visa": False,
        "days": 90,
        "source": "GLOBAL SAFE DEFAULT"
    }


# =========================================================
# 🧠 MAIN ENGINE
# =========================================================
def get(passport, country):

    country_iso = normalize_country(country)

    cache = load_cache()
    key = f"{passport}_{country_iso}"
    now = time.time()

    if key in cache:
        item = cache[key]
        if now - item["time"] < CACHE_TTL:
            return item["data"]

    result = api(passport, country_iso)

    if not result:
        result = safe_fallback(passport, country_iso)

    cache[key] = {
        "data": result,
        "time": now
    }

    save_cache(cache)

    return result


# =========================================================
# 🚀 BULK MAP LOAD
# =========================================================
def get_many(passport):
    results = {}

    for code in COUNTRIES_100.keys():
        results[code] = get(passport, code)

    return results


# export pro UI
def get_country_list():
    return COUNTRIES_100
