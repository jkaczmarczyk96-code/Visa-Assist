# =========================
# 🌍 COUNTRY DATABASE (TOP NON-SCHENGEN DESTINATIONS)
# =========================

COUNTRIES_DATA = {
    "Albania": {"iso2": "AL", "aliases": ["Albania"]},
    "Argentina": {"iso2": "AR", "aliases": ["Argentina"]},
    "Australia": {"iso2": "AU", "aliases": ["Australia"]},
    "Azerbaijan": {"iso2": "AZ", "aliases": ["Azerbaijan"]},
    "Bahrain": {"iso2": "BH", "aliases": ["Bahrain"]},
    "Bangladesh": {"iso2": "BD", "aliases": ["Bangladesh"]},
    "Belarus": {"iso2": "BY", "aliases": ["Belarus"]},
    "Bosnia and Herzegovina": {"iso2": "BA", "aliases": ["Bosnia", "BiH"]},
    "Brazil": {"iso2": "BR", "aliases": ["Brazil"]},
    "Cambodia": {"iso2": "KH", "aliases": ["Cambodia"]},
    "Canada": {"iso2": "CA", "aliases": ["Canada"]},
    "Chile": {"iso2": "CL", "aliases": ["Chile"]},
    "China": {"iso2": "CN", "aliases": ["China"]},
    "Colombia": {"iso2": "CO", "aliases": ["Colombia"]},
    "Costa Rica": {"iso2": "CR", "aliases": ["Costa Rica"]},
    "Cuba": {"iso2": "CU", "aliases": ["Cuba"]},
    "Dominican Republic": {"iso2": "DO", "aliases": ["Dominican Republic"]},
    "Egypt": {"iso2": "EG", "aliases": ["Egypt"]},
    "Ethiopia": {"iso2": "ET", "aliases": ["Ethiopia"]},
    "Georgia": {"iso2": "GE", "aliases": ["Georgia"]},
    "Ghana": {"iso2": "GH", "aliases": ["Ghana"]},
    "Hong Kong": {"iso2": "HK", "aliases": ["Hong Kong"]},
    "India": {"iso2": "IN", "aliases": ["India"]},
    "Indonesia": {"iso2": "ID", "aliases": ["Indonesia"]},
    "Israel": {"iso2": "IL", "aliases": ["Israel"]},
    "Jamaica": {"iso2": "JM", "aliases": ["Jamaica"]},
    "Japan": {"iso2": "JP", "aliases": ["Japan"]},
    "Jordan": {"iso2": "JO", "aliases": ["Jordan"]},
    "Kazakhstan": {"iso2": "KZ", "aliases": ["Kazakhstan"]},
    "Kenya": {"iso2": "KE", "aliases": ["Kenya"]},
    "Kuwait": {"iso2": "KW", "aliases": ["Kuwait"]},
    "Laos": {"iso2": "LA", "aliases": ["Laos"]},
    "Lebanon": {"iso2": "LB", "aliases": ["Lebanon"]},
    "Madagascar": {"iso2": "MG", "aliases": ["Madagascar"]},
    "Malaysia": {"iso2": "MY", "aliases": ["Malaysia"]},
    "Maldives": {"iso2": "MV", "aliases": ["Maldives"]},
    "Mauritius": {"iso2": "MU", "aliases": ["Mauritius"]},
    "Mexico": {"iso2": "MX", "aliases": ["Mexico"]},
    "Moldova": {"iso2": "MD", "aliases": ["Moldova"]},
    "Mongolia": {"iso2": "MN", "aliases": ["Mongolia"]},
    "Montenegro": {"iso2": "ME", "aliases": ["Montenegro"]},
    "Morocco": {"iso2": "MA", "aliases": ["Morocco"]},
    "Namibia": {"iso2": "NA", "aliases": ["Namibia"]},
    "Nepal": {"iso2": "NP", "aliases": ["Nepal"]},
    "New Zealand": {"iso2": "NZ", "aliases": ["New Zealand"]},
    "Nigeria": {"iso2": "NG", "aliases": ["Nigeria"]},
    "North Macedonia": {"iso2": "MK", "aliases": ["Macedonia"]},
    "Oman": {"iso2": "OM", "aliases": ["Oman"]},
    "Peru": {"iso2": "PE", "aliases": ["Peru"]},
    "Philippines": {"iso2": "PH", "aliases": ["Philippines"]},
    "Qatar": {"iso2": "QA", "aliases": ["Qatar"]},
    "Russia": {"iso2": "RU", "aliases": ["Russia"]},
    "Rwanda": {"iso2": "RW", "aliases": ["Rwanda"]},
    "Saudi Arabia": {"iso2": "SA", "aliases": ["Saudi Arabia"]},
    "Serbia": {"iso2": "RS", "aliases": ["Serbia"]},
    "Singapore": {"iso2": "SG", "aliases": ["Singapore"]},
    "South Africa": {"iso2": "ZA", "aliases": ["South Africa"]},
    "South Korea": {"iso2": "KR", "aliases": ["South Korea", "Korea"]},
    "Sri Lanka": {"iso2": "LK", "aliases": ["Sri Lanka"]},
    "Taiwan": {"iso2": "TW", "aliases": ["Taiwan"]},
    "Tanzania": {"iso2": "TZ", "aliases": ["Tanzania"]},
    "Thailand": {"iso2": "TH", "aliases": ["Thailand"]},
    "Tunisia": {"iso2": "TN", "aliases": ["Tunisia"]},
    "Turkey": {"iso2": "TR", "aliases": ["Turkey"]},
    "Uganda": {"iso2": "UG", "aliases": ["Uganda"]},
    "Ukraine": {"iso2": "UA", "aliases": ["Ukraine"]},
    "United Arab Emirates": {"iso2": "AE", "aliases": ["UAE", "Emirates"]},
    "United Kingdom": {"iso2": "GB", "aliases": ["UK", "Britain"]},
    "United States": {"iso2": "US", "aliases": ["USA", "US"]},
    "Uzbekistan": {"iso2": "UZ", "aliases": ["Uzbekistan"]},
    "Vietnam": {"iso2": "VN", "aliases": ["Vietnam"]},
    "Zambia": {"iso2": "ZM", "aliases": ["Zambia"]},
    "Zimbabwe": {"iso2": "ZW", "aliases": ["Zimbabwe"]}
}

COUNTRIES = sorted(COUNTRIES_DATA.keys())


# =========================
# NORMALIZATION
# =========================
def normalize_country(user_input):
    user_input = user_input.lower().strip()

    for name, data in COUNTRIES_DATA.items():
        if user_input == name.lower():
            return name
        for alias in data["aliases"]:
            if user_input == alias.lower():
                return name

    return user_input


# =========================
# API FORMAT
# =========================
def to_api_format(country):
    country = normalize_country(country)
    return COUNTRIES_DATA.get(country, {}).get("iso2", country)
