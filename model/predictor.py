"""Moduł do obsługi gotowych prognoz cenowych."""

import os
import joblib
import pandas as pd


class PricePredictor:
    """Klasa ładująca model i wykonująca prognozy cen mieszkań."""

    def __init__(self, model_name: str = "housing_model.joblib"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, "saved_models", model_name)

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Nie znaleziono pliku modelu w ścieżce: {model_path}. "
                f"Upewnij się, że skrypt trainer.py uruchomił się poprawnie."
            )

        self.model = joblib.load(model_path)

    def predict_price(
        self, size: float, rooms: int, distance: float, year: int
    ) -> float:
        """Przyjmuje parametry mieszkania i zwraca prognozowaną cenę."""
        input_data = pd.DataFrame(
            [[size, rooms, distance, year]],
            columns=["size", "rooms", "distance_to_center", "year_built"],
        )
        prediction = self.model.predict(input_data)
        return float(prediction[0])