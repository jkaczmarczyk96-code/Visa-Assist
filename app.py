import streamlit as st
from engine import get
from countries import COUNTRIES, get_mzv_cz_url, get_mzv_sk_url


st.set_page_config(page_title="Visa Assist", page_icon="🌍")

st.title("🌍 Visa Assist")
st.caption("Rychlá kontrola vízových podmínek")

st.divider()


passport = st.selectbox("🛂 Pas", ["CZ", "SK"])
country = st.selectbox("🌍 Země", COUNTRIES)


if st.button("🔍 Zkontrolovat vízové podmínky"):

    result = get(passport, country)

    status_map = {
        "green": ("Bez víza", "#2ecc71"),
        "blue": ("Vízum při příjezdu / eVisa", "#3498db"),
        "yellow": ("Registrace / eVisa", "#f1c40f"),
        "red": ("Vízum nutné", "#e74c3c")
    }

    label, color = status_map.get(result["visa_color"], ("Neznámé", "#999"))

    with st.container(border=True):

        st.markdown(
            f'<div style="height:8px;background:{color};border-radius:10px;margin-bottom:10px;"></div>',
            unsafe_allow_html=True
        )

        st.subheader(country)
        st.markdown(f"**{label}**")

        st.divider()

        st.write("🛂 Typ víza:", result.get("visa_name"))
        st.write("⏳ Maximální pobyt:", result.get("visa_duration"))

        st.divider()

        st.caption(f"Zdroj: {result.get('source')}")
        st.caption(f"Aktualizováno: {result.get('generated_at')}")

        # ⚠️ warning
        if result.get("visa_color") == "yellow":
            st.warning("⚠️ Podmínky se mohou lišit. Ověř informace na MZV.")

        # 🌍 MZV
        if passport == "CZ":
            link = get_mzv_cz_url(country)
        else:
            link = get_mzv_sk_url(country)

        if link:
            st.markdown(f"🔗 Oficiální informace MZV: {link}")
