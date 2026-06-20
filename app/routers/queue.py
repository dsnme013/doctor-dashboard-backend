"""Triage queue and dashboard stats."""
from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.schemas import Patient, Stats, Tier
from app.store import Store, get_store

router = APIRouter(tags=["queue"])


@router.get("/queue", response_model=list[Patient])
def get_queue(
    tier: Optional[Tier] = Query(default=None),
    store: Store = Depends(get_store),
) -> list[Patient]:
    """Today's incoming triage queue, optionally filtered by tier."""
    with store.lock:
        items = list(store.patients.values())
    if tier:
        items = [p for p in items if p.tier == tier]
    return items


@router.get("/stats", response_model=Stats)
def get_stats(store: Store = Depends(get_store)) -> Stats:
    with store.lock:
        patients = list(store.patients.values())
        pending = [p for p in patients if p.status == "pending"]
        return Stats(
            booked_today=8,
            video=5,
            home_visits=3,
            high_triage_pending=sum(1 for p in pending if p.tier == "high"),
            pending=len(pending),
            avg_response_min=11,
            rating=4.8,
            reviews=214,
            available=store.available,
            unread_messages=sum(1 for t in store.threads.values() if t.unread),
        )
