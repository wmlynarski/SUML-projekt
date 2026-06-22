"""Moduł API wystawiający endpoint do predykcji cen mieszkań."""
import os
import sys
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from model.predictor import PricePredictor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="Housing Price API", description="API do wyceny nieruchomości.")
predictor = PricePredictor()


class HouseFeatures(BaseModel):
    """Schemat danych wejściowych z walidacją."""
    area: float
    bedrooms: int
    bathrooms: int
    stories: int
    mainroad: int
    guestroom: int
    basement: int
    hotwaterheating: int
    airconditioning: int
    parking: int
    prefarea: int
    furnishingstatus: int


@app.post("/predict")
def predict(features: HouseFeatures):
    """Zwraca prognozowaną cenę na podstawie przekazanych cech."""
    input_data = pd.DataFrame([features.dict()])
    predicted_price = float(predictor.model.predict(input_data)[0])
    return {"predicted_price": predicted_price}
