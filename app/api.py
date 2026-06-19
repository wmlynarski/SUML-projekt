"""Moduł API wystawiający endpoint do predykcji cen mieszkań."""

import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.predictor import PricePredictor

app = FastAPI(title="Housing Price API", description="API do wyceny nieruchomości.")
predictor = PricePredictor()


class HouseFeatures(BaseModel):
    """Schemat danych wejściowych wymaganych przez model."""
    size: float
    rooms: int
    distance: float
    year: int


@app.post("/predict")
def predict(features: HouseFeatures):
    """Zwraca prognozowaną cenę na podstawie przekazanych cech."""
    predicted_price = predictor.predict_price(
        features.size, features.rooms, features.distance, features.year
    )
    return {"predicted_price": predicted_price}