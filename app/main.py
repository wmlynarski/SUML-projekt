"""Główny moduł aplikacji webowej (Frontend)."""

import requests
import streamlit as st

st.set_page_config(page_title="Wycena Nieruchomości", page_icon="🏠")

st.title("🏠 Algorytm Wyceny Nieruchomości")
st.write("Wprowadź parametry domu na podstawie danych rynkowych.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Podstawowe parametry")
    area = st.number_input("Powierzchnia (m²)", min_value=10.0, value=200.0)
    bedrooms = st.number_input("Liczba sypialni", min_value=1, value=1)
    bathrooms = st.number_input("Liczba łazienek", min_value=1, value=1)
    stories = st.number_input("Liczba pięter", min_value=1, value=2)
    parking = st.number_input("Liczba miejsc parkingowych", min_value=0, max_value=5, value=0)
    furnishing_options = {"Brak (Unfurnished)": 0,
    "Częściowe (Semi-furnished)": 1, "Pełne (Furnished)": 2}
    selected_furnishing = st.selectbox("Stan umeblowania", options=list(furnishing_options.keys()))
    furnishingstatus = furnishing_options[selected_furnishing]

with col2:
    st.subheader("Udogodnienia")
    mainroad = int(st.checkbox("Blisko głównej drogi ", value=True))
    guestroom = int(st.checkbox("Pokój gościnny "))
    basement = int(st.checkbox("Piwnica "))
    hotwaterheating = int(st.checkbox("Ogrzewanie wody"))
    airconditioning = int(st.checkbox("Klimatyzacja"))
    prefarea = int(st.checkbox("Lepsza okolica"))

if st.button("Szacuj wartość rynkową", use_container_width=True):
    payload = {
        "area": area,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "stories": stories,
        "mainroad": mainroad,
        "guestroom": guestroom,
        "basement": basement,
        "hotwaterheating": hotwaterheating,
        "airconditioning": airconditioning,
        "parking": parking,
        "prefarea": prefarea,
        "furnishingstatus": furnishingstatus
    }
    try:
        response = requests.post("http://api:8000/predict", json=payload, timeout=5)
        response.raise_for_status()
        price = response.json().get("predicted_price", 0)
        st.success(f"Szacowana cena to: **{price:,.2f} PLN**")
    except requests.exceptions.RequestException as e:
        st.error(f"Błąd połączenia z API: {e}")
