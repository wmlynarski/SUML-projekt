"""Moduł odpowiedzialny za przetwarzanie danych z bazy SQLite."""

import os
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split

class DataProcessor:
    """Klasa do pobierania z bazy i dzielenia danych o nieruchomościach."""

    def __init__(self, filename: str = "housing.db"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, "datasets", filename)

        if not os.path.exists(self.db_path):
            raise FileNotFoundError(
                f"Nie znaleziono bazy w: {self.db_path}. Uruchom notatnik data_preparation.ipynb"
            )

    def load_and_split_data(self, test_size: float = 0.2):
        """Pobiera dane zapytaniem SQL i dzieli je na zbiory."""
        with sqlite3.connect(self.db_path) as conn:
            data = pd.read_sql_query("SELECT * FROM apartments", conn)

        feature_cols = [
            "area", "bedrooms", "bathrooms", "stories",
            "mainroad", "guestroom", "basement", 
            "hotwaterheating", "airconditioning",
            "parking", "prefarea", "furnishingstatus" # <- Nowe kolumny
        ]
        features = data[feature_cols]
        target = data["price"]

        return train_test_split(features, target, test_size=test_size, random_state=42)
