"""Thread-safe in-memory data store.

This is the single integration point for persistence: replace this class
with a PostgreSQL / SQLAlchemy repository without touching the routers.
Triage tiers mirror the CareConnect engine: low <35, moderate 35-69, high 70+.
"""
from __future__ import annotations

from threading import Lock
from typing import Optional

from fastapi import HTTPException

from app.schemas import Message, Patient, Profile, ScheduleSlot, Thread


class Store:
    def __init__(self) -> None:
        self.lock = Lock()
        self.available = False
        self.profile = Profile(
            name="Dr. Arjun Mehta",
            speciality="General Physician",
            fee=600,
            languages="English, Hindi, Telugu",
            bio=(
                "15+ years in family medicine. Calm, thorough, and focused on "
                "practical home-care advice."
            ),
        )
        self.patients: dict[int, Patient] = {
            p.id: p
            for p in [
                Patient(id=1, name="Ramesh Kumar", age=67, gender="M",
                        symptom="Chest discomfort", onset="Today", score=86,
                        tier="high", flags=["Chest pain"],
                        comorb=["BP", "Diabetes"], mode="Video",
                        time="10:30 AM", color="#0f766e"),
                Patient(id=2, name="Lakshmi Devi", age=71, gender="F",
                        symptom="Breathing trouble", onset="Yesterday", score=79,
                        tier="high", flags=["Breathing trouble"], comorb=["BP"],
                        mode="Home visit", time="11:15 AM", color="#b45309"),
                Patient(id=3, name="Sneha Reddy", age=29, gender="F",
                        symptom="Fever", onset="2–3 days", score=52,
                        tier="moderate", mode="Video", time="12:00 PM",
                        color="#7c3aed"),
                Patient(id=4, name="Aditya Verma", age=35, gender="M",
                        symptom="Stomach pain", onset="Yesterday", score=41,
                        tier="moderate", flags=["Dehydration"], mode="Video",
                        time="2:00 PM", color="#0369a1"),
                Patient(id=5, name="Kavya Sharma", age=24, gender="F",
                        symptom="Headache", onset="Today", score=22, tier="low",
                        mode="Video", time="3:30 PM", color="#be185d"),
            ]
        }
        self.schedule: list[ScheduleSlot] = [
            ScheduleSlot(t="10:30", pid=1, now=True),
            ScheduleSlot(t="11:15", pid=2),
            ScheduleSlot(t="12:00", pid=3),
            ScheduleSlot(t="1:00", open=True),
            ScheduleSlot(t="2:00", pid=4),
            ScheduleSlot(t="3:30", pid=5),
            ScheduleSlot(t="4:30", open=True),
        ]
        self.open_slots: list[str] = ["1:00 PM", "4:30 PM"]
        self.threads: dict[int, Thread] = {
            1: Thread(patient_id=1, unread=True, msgs=[
                Message(who="them", t="9:42 AM",
                        txt=("Doctor, the chest tightness comes when I climb "
                             "stairs. Should I take my BP tablet now?")),
                Message(who="them", t="9:43 AM", txt="My BP reading is 152/96."),
            ]),
            3: Thread(patient_id=3, unread=True, msgs=[
                Message(who="them", t="8:15 AM",
                        txt="Fever touched 101.4 last night even after paracetamol."),
            ]),
            4: Thread(patient_id=4, msgs=[
                Message(who="them", t="Yesterday",
                        txt="Thank you doctor, the ORS helped a lot 🙏"),
                Message(who="me", t="Yesterday",
                        txt=("Glad to hear it. Keep sipping fluids and avoid "
                             "outside food for 2 days.")),
            ]),
        }

    # ------------------------------------------------------------------ utils
    def patient_or_404(self, pid: int) -> Patient:
        p: Optional[Patient] = self.patients.get(pid)
        if p is None:
            raise HTTPException(status_code=404, detail="patient_not_found")
        return p


store = Store()


def get_store() -> Store:
    """FastAPI dependency."""
    return store
