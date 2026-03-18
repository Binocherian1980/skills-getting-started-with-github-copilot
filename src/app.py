"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


# ── Conversion Calculator ──────────────────────────────────────────────────────

@app.get("/convert/temperature")
def convert_temperature(value: float, from_unit: str, to_unit: str):
    """Convert temperature between Celsius (C), Fahrenheit (F), and Kelvin (K)."""
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()
    supported = {"C", "F", "K"}
    if from_unit not in supported or to_unit not in supported:
        raise HTTPException(status_code=400, detail="Unsupported unit. Use C, F, or K.")

    # Convert to Celsius first
    if from_unit == "C":
        celsius = value
    elif from_unit == "F":
        celsius = (value - 32) * 5 / 9
    else:  # K
        celsius = value - 273.15

    # Convert from Celsius to target unit
    if to_unit == "C":
        result = celsius
    elif to_unit == "F":
        result = celsius * 9 / 5 + 32
    else:  # K
        result = celsius + 273.15

    return {
        "input_value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "result": round(result, 4),
    }


@app.get("/convert/distance")
def convert_distance(value: float, from_unit: str, to_unit: str):
    """Convert distance between miles (mi), kilometers (km), meters (m), and feet (ft)."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    # Conversion factors to meters
    to_meters = {"mi": 1609.344, "km": 1000.0, "m": 1.0, "ft": 0.3048}
    supported = set(to_meters.keys())
    if from_unit not in supported or to_unit not in supported:
        raise HTTPException(
            status_code=400, detail="Unsupported unit. Use mi, km, m, or ft."
        )

    meters = value * to_meters[from_unit]
    result = meters / to_meters[to_unit]

    return {
        "input_value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "result": round(result, 4),
    }


@app.get("/convert/weight")
def convert_weight(value: float, from_unit: str, to_unit: str):
    """Convert weight between kilograms (kg), pounds (lb), grams (g), and ounces (oz)."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    # Conversion factors to grams
    to_grams = {"kg": 1000.0, "lb": 453.592, "g": 1.0, "oz": 28.3495}
    supported = set(to_grams.keys())
    if from_unit not in supported or to_unit not in supported:
        raise HTTPException(
            status_code=400, detail="Unsupported unit. Use kg, lb, g, or oz."
        )

    grams = value * to_grams[from_unit]
    result = grams / to_grams[to_unit]

    return {
        "input_value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "result": round(result, 4),
    }

