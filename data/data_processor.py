"""Moduł odpowiedzialny za przetwarzanie i przygotowanie danych."""

import os
import pandas as pd
from sklearn.model_selection import train_test_split


class DataProcessor:
    """Klasa do ładowania i dzielenia danych o mieszkaniach."""

    def __init__(self, filename: str = "apartments.csv"):
        # Pobieramy ścieżkę do katalogu głównego projektu (wyżej niż folder 'data')
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(base_dir, "datasets", filename)

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Nie znaleziono pliku bazy danych w: {self.file_path}")

    def load_and_split_data(self, test_size: float = 0.2):
        """Wczytuje plik CSV i dzieli go na zbiór treningowy i testowy."""
        data = pd.read_csv(self.file_path)

        # Cechy (X) i wartość docelowa (y)
        features = data[["size", "rooms", "distance_to_center", "year_built"]]
        target = data["price"]

        return train_test_split(
            features, target, test_size=test_size, random_state=42
        )