"""Moduł do trenowania modelu Machine Learning"""

import os
import joblib
from sklearn.linear_model import LinearRegression  # <-- ZMIENIONY IMPORT
from data.data_processor import DataProcessor

def train_and_save_model():
    """Trenuje model Regresji Liniowej i zapisuje go do pliku."""
    output_dir = os.path.join(os.getcwd(), "saved_models")
    os.makedirs(output_dir, exist_ok=True)

    processor = DataProcessor()
    x_train, _, y_train, _ = processor.load_and_split_data()

    for col in x_train.select_dtypes(include=['object']).columns:
        x_train[col] = x_train[col].map({'yes': 1, 'no': 0}).fillna(0)

    model = LinearRegression()
    model.fit(x_train, y_train)

    model_path = os.path.join(output_dir, "housing_model.joblib")
    joblib.dump(model, model_path)
    print(f"Model pomyślnie wytrenowany i zapisany w: {model_path}")

if __name__ == "__main__":
    train_and_save_model()
