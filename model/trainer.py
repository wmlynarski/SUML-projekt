"""Moduł do trenowania modelu Machine Learning."""

import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from data.data_processor import DataProcessor


def train_and_save_model():
    """Trenuje model Random Forest i zapisuje go do pliku."""
    # Pobieramy ścieżkę do katalogu głównego projektu
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "saved_models")
    
    # Automatyczne tworzenie folderu na model, jeśli nie istnieje
    os.makedirs(output_dir, exist_ok=True)

    # Inicjalizacja procesora (sam znajdzie apartments.csv)
    processor = DataProcessor()
    x_train, _, y_train, _ = processor.load_and_split_data()

    # Prosty i skuteczny model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)

    # Zapisujemy model w dedykowanym folderze
    model_path = os.path.join(output_dir, "housing_model.joblib")
    joblib.dump(model, model_path)
    print(f"Model został pomyślnie zapisany w: {model_path}")


if __name__ == "__main__":
    train_and_save_model()