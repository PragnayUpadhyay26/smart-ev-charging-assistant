import math
import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Smart EV Charging Assistant AI Service")

# Enable CORS for Express backend and Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Trained Model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "wait_time_model.joblib")

try:
    model = joblib.load(MODEL_PATH)
    print(f"Loaded ML model from {MODEL_PATH}")
except Exception as e:
    model = None
    print(f"Warning: Could not load model ({e}). Train model first.")


# Input Schemas
class WaitTimeRequest(BaseModel):
    battery_percentage: float
    distance: float
    total_chargers: int
    occupied_chargers: int
    queue_length: int
    charging_speed: float


class StationInput(BaseModel):
    station_id: int
    name: str
    latitude: float
    longitude: float
    total_chargers: int
    occupied_chargers: int
    queue_length: int
    charging_speed: float


class RecommendationRequest(BaseModel):
    vehicle_id: Optional[int] = 1
    latitude: float
    longitude: float
    battery_percentage: float
    stations: List[StationInput]


def calculate_distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)


@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "Smart EV AI Engine",
        "model_loaded": model is not None,
    }


@app.post("/predict-wait-time")
def predict_wait_time(data: WaitTimeRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")

    features = pd.DataFrame(
        [[
            data.battery_percentage,
            data.distance,
            data.total_chargers,
            data.occupied_chargers,
            data.queue_length,
            data.charging_speed,
        ]],
        columns=[
            "battery_percentage",
            "distance",
            "total_chargers",
            "occupied_chargers",
            "queue_length",
            "charging_speed",
        ],
    )

    predicted_wait = model.predict(features)[0]
    return {"predicted_wait_time": max(0, round(float(predicted_wait), 2))}


@app.post("/recommend")
def recommend_stations(data: RecommendationRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")

    recommendations = []

    for station in data.stations:
        dist = calculate_distance(
            data.latitude,
            data.longitude,
            station.latitude,
            station.longitude,
        )

        features = pd.DataFrame(
            [[
                data.battery_percentage,
                dist,
                station.total_chargers,
                station.occupied_chargers,
                station.queue_length,
                station.charging_speed,
            ]],
            columns=[
                "battery_percentage",
                "distance",
                "total_chargers",
                "occupied_chargers",
                "queue_length",
                "charging_speed",
            ],
        )

        predicted_wait = float(model.predict(features)[0])
        predicted_wait = max(0, round(predicted_wait, 2))

        # Recommendation scoring function
        distance_score = dist * 100
        wait_score = predicted_wait
        availability_benefit = (
            station.total_chargers - station.occupied_chargers
        ) * 5
        battery_urgency_benefit = (100 - data.battery_percentage) * 0.5

        final_score = (
            distance_score
            + wait_score
            - availability_benefit
            - battery_urgency_benefit
        )

        recommendations.append({
            "station_id": station.station_id,
            "name": station.name,
            "latitude": station.latitude,
            "longitude": station.longitude,
            "distance": round(dist, 4),
            "predicted_wait_time": predicted_wait,
            "total_chargers": station.total_chargers,
            "occupied_chargers": station.occupied_chargers,
            "available_chargers": station.total_chargers - station.occupied_chargers,
            "queue_length": station.queue_length,
            "recommendation_score": round(final_score, 2),
        })

    # Sort stations ascending by recommendation score (lower score = better choice)
    recommendations.sort(key=lambda x: x["recommendation_score"])

    return {
        "vehicle_id": data.vehicle_id,
        "battery_percentage": data.battery_percentage,
        "recommended_station": recommendations[0] if recommendations else None,
        "all_recommendations": recommendations,
    }