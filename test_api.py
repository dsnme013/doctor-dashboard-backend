"""Smoke tests for every endpoint. Run: python -m pytest test_api.py  (or python test_api.py)"""
from fastapi.testclient import TestClient

from main import app

c = TestClient(app)


def run() -> None:
    assert c.get("/api/v1/health").status_code == 200
    assert len(c.get("/api/v1/queue").json()) == 5
    assert len(c.get("/api/v1/queue?tier=high").json()) == 2

    r = c.post("/api/v1/booking/1/accept")
    assert r.status_code == 200 and r.json()["status"] == "accepted"
    assert c.post("/api/v1/booking/1/accept").status_code == 409
    assert c.post("/api/v1/booking/999/accept").status_code == 404

    r = c.patch("/api/v1/booking/3/reschedule", json={"slot": "1:00 PM"})
    assert r.json()["time"] == "1:00 PM"
    assert c.patch("/api/v1/booking/4/reschedule", json={"slot": "9:00 PM"}).status_code == 409

    sch = c.get("/api/v1/schedule").json()
    assert "12:00 PM" in sch["open_slots"]  # freed slot returned to pool
    assert c.post("/api/v1/schedule/slot?t=5:30").status_code == 201

    assert c.get("/api/v1/patients?q=fever").json()[0]["name"] == "Sneha Reddy"

    assert len(c.get("/api/v1/messages").json()) == 3
    assert c.get("/api/v1/messages/1").json()["unread"] is False
    r = c.post("/api/v1/messages/1", json={"text": "Take the tablet now and rest."})
    assert r.json()["msgs"][-1]["who"] == "me"
    assert c.get("/api/v1/messages/999").status_code == 404

    assert c.get("/api/v1/stats").json()["high_triage_pending"] == 1
    assert c.get("/api/v1/reports").json()["summary"]["consults"] == 42

    r = c.put("/api/v1/profile", json={"name": "Dr. A. Mehta", "fee": 700})
    assert r.json()["fee"] == 700
    assert c.post("/api/v1/availability", json={"available": True}).json()["available"] is True
    print("ALL 18 BACKEND CHECKS PASSED")


if __name__ == "__main__":
    run()
