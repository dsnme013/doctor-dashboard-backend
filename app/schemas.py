"""Pydantic models shared across routers."""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

Tier = Literal["low", "moderate", "high"]
PatientStatus = Literal["pending", "accepted", "rescheduled"]
Mode = Literal["Video", "Home visit"]


class Patient(BaseModel):
    id: int
    name: str
    age: int
    gender: Literal["M", "F", "O"]
    symptom: str
    onset: str
    score: int = Field(ge=0, le=100)
    tier: Tier
    flags: list[str] = []
    comorb: list[str] = []
    mode: Mode
    time: str
    color: str
    status: PatientStatus = "pending"


class ScheduleSlot(BaseModel):
    t: str
    pid: Optional[int] = None
    open: bool = False
    now: bool = False


class Message(BaseModel):
    who: Literal["me", "them"]
    t: str
    txt: str


class Thread(BaseModel):
    patient_id: int
    unread: bool = False
    msgs: list[Message] = []


class ThreadSummary(BaseModel):
    patient_id: int
    name: str
    color: str
    unread: bool
    last: Optional[Message] = None


class Profile(BaseModel):
    name: str
    speciality: str
    fee: int = Field(ge=0)
    languages: str
    bio: str
    accept_video: bool = True
    accept_home_visits: bool = True
    auto_accept_low: bool = False
    whatsapp_notifications: bool = True


class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=80)
    speciality: Optional[str] = None
    fee: Optional[int] = Field(default=None, ge=0)
    languages: Optional[str] = None
    bio: Optional[str] = Field(default=None, max_length=500)
    accept_video: Optional[bool] = None
    accept_home_visits: Optional[bool] = None
    auto_accept_low: Optional[bool] = None
    whatsapp_notifications: Optional[bool] = None


class RescheduleRequest(BaseModel):
    slot: str = Field(min_length=1, examples=["1:00 PM"])


class SendMessageRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class AvailabilityRequest(BaseModel):
    available: bool


class Stats(BaseModel):
    booked_today: int
    video: int
    home_visits: int
    high_triage_pending: int
    pending: int
    avg_response_min: int
    rating: float
    reviews: int
    available: bool
    unread_messages: int
