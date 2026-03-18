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
import httpx

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


# Fallback exchange rates relative to USD (used when the external API is unavailable)
FALLBACK_RATES_USD = {
    "USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 149.50, "CAD": 1.36,
    "AUD": 1.53, "CHF": 0.89, "CNY": 7.24, "INR": 83.12, "MXN": 17.15,
    "BRL": 4.97, "KRW": 1325.0, "SGD": 1.34, "HKD": 7.82, "NOK": 10.55,
    "SEK": 10.42, "DKK": 6.89, "NZD": 1.63, "ZAR": 18.63, "RUB": 91.50,
}

EXCHANGE_RATE_API = "https://open.er-api.com/v6/latest/{base}"


@app.get("/currency/convert")
async def convert_currency(amount: float, from_currency: str, to_currency: str):
    """Convert an amount from one currency to another."""
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(EXCHANGE_RATE_API.format(base=from_currency))
            response.raise_for_status()
            data = response.json()

        if data.get("result") != "success":
            raise ValueError("API returned non-success result")

        rates = data["rates"]
        if to_currency not in rates:
            raise HTTPException(status_code=400, detail=f"Unsupported target currency: {to_currency}")

        converted = amount * rates[to_currency]
        return {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "original_amount": amount,
            "converted_amount": round(converted, 4),
            "exchange_rate": round(rates[to_currency], 6),
            "source": "live",
        }

    except HTTPException:
        raise
    except Exception:
        # Fall back to static rates
        if from_currency not in FALLBACK_RATES_USD:
            raise HTTPException(status_code=400, detail=f"Unsupported source currency: {from_currency}")
        if to_currency not in FALLBACK_RATES_USD:
            raise HTTPException(status_code=400, detail=f"Unsupported target currency: {to_currency}")

        rate = FALLBACK_RATES_USD[to_currency] / FALLBACK_RATES_USD[from_currency]
        converted = amount * rate
        return {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "original_amount": amount,
            "converted_amount": round(converted, 4),
            "exchange_rate": round(rate, 6),
            "source": "fallback",
        }


@app.get("/currency/supported")
def get_supported_currencies():
    """Return the list of supported currencies."""
    return {"currencies": sorted(FALLBACK_RATES_USD.keys())}
