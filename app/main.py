"""Główny moduł aplikacji webowej (Frontend)."""

import requests
import streamlit as st

st.title("🏠 Wycena Mieszkania - Frontend")
st.write("Aplikacja odpytuje niezależny kontener API w celu uzyskania wyceny.")

size = st.number_input("Metraż (m²)", min_value=10, max_value=200, value=50)
rooms = st.number_input("Liczba pokoi", min_value=1, max_value=10, value=2)
distance = st.number_input("Odległość (km)", min_value=0.1, max_value=50.0, value=3.5)
year = st.number_input("Rok budowy", min_value=1900, max_value=2026, value=2020)

if st.button("Oblicz wartość"):
    payload = {
        "size": size,
        "rooms": rooms,
        "distance": distance,
        "year": year
    }
    
    try:
        response = requests.post("http://api:8000/predict", json=payload, timeout=5)
        response.raise_for_status()
        
        price = response.json().get("predicted_price", 0)
        st.success(f"Szacowana cena to: **{price:,.2f} PLN**")
        
    except requests.exceptions.RequestException as e:
        st.error(f"Błąd połączenia z API: {e}")