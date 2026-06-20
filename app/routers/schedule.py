"""Day schedule and open slots."""
from fastapi import APIRouter, Depends, Query

from app.logging_conf import log
from app.schemas import ScheduleSlot
from app.store import Store, get_store

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.get("")
def get_schedule(store: Store = Depends(get_store)) -> dict:
    with store.lock:
        return {
            "slots": [s.model_dump() for s in store.schedule],
            "open_slots": list(store.open_slots),
        }


@router.post("/slot", status_code=201)
def add_open_slot(
    t: str = Query(default="5:30", min_length=1, max_length=10),
    store: Store = Depends(get_store),
) -> dict:
    with store.lock:
        store.schedule.append(ScheduleSlot(t=t, open=True))
        label = t if ("AM" in t or "PM" in t) else f"{t} PM"
        store.open_slots.append(label)
        log.info("Open slot added at %s", label)
        return {"ok": True, "t": t}
