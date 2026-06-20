"""Weekly report aggregates."""
from fastapi import APIRouter

router = APIRouter(tags=["reports"])


@router.get("/reports")
def get_reports() -> dict:
    return {
        "summary": {
            "consults": 42, "delta_pct": 12, "completion_pct": 94,
            "no_shows": 2, "avg_consult_min": 14, "earnings_inr": 31500,
        },
        "consults_by_day": [
            {"day": d, "n": n}
            for d, n in [("Mon", 5), ("Tue", 7), ("Wed", 4), ("Thu", 8),
                         ("Fri", 6), ("Sat", 9), ("Sun", 3)]
        ],
        "triage_mix": [
            {"tier": "high", "n": 10, "pct": 24},
            {"tier": "moderate", "n": 16, "pct": 38},
            {"tier": "low", "n": 16, "pct": 38},
        ],
        "top_symptoms": [
            {"symptom": s, "n": n}
            for s, n in [("Fever", 14), ("Cough", 9), ("Stomach pain", 7),
                         ("Headache", 7), ("Body ache", 5)]
        ],
    }
