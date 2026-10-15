
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="TripGenie AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


class TripPlanRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    destination: str = Field(min_length=1, max_length=120)
    dates: str = ""
    travellers: str = "2 travellers"
    budget: str = "₹10,000"
    interests: list[str] = Field(default_factory=list)


@app.post("/api/plan-trip")
def plan_trip(request: TripPlanRequest):
    interests = request.interests or ["Explore"]
    focus = interests[0].lower()

    return {
        "destination": request.destination.strip(),
        "dates": request.dates.strip() or "Your selected dates",
        "travellers": request.travellers,
        "budget": request.budget,
        "interests": interests,
        "days": [
            {
                "label": "DAY 01",
                "title": "Arrive & explore",
                "activities": [
                    "Arrive and settle in",
                    f"Explore an attraction that matches your {focus} interests",
                    "Enjoy a relaxed local dinner",
                ],
            },
            {
                "label": "DAY 02",
                "title": "Your main adventure",
                "activities": [
                    "Start with a scenic viewpoint",
                    f"Choose a {focus}-focused activity",
                    "Leave time for a local experience",
                ],
            },
        ],
    }

@app.get("/")
def home():
    return {
        "message": "Welcome to TripGenie AI!"
    }

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "project": "TripGenie AI"
    }
