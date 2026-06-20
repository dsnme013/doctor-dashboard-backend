"""Patient directory / search."""
from fastapi import APIRouter, Depends, Query

from app.schemas import Patient
from app.store import Store, get_store

router = APIRouter(tags=["patients"])


@router.get("/patients", response_model=list[Patient])
def list_patients(
    q: str = Query(default="", max_length=100),
    store: Store = Depends(get_store),
) -> list[Patient]:
    needle = q.strip().lower()
    with store.lock:
        items = list(store.patients.values())
    if not needle:
        return items
    return [
        p for p in items
        if needle in p.name.lower()
        or needle in p.symptom.lower()
        or needle in " ".join(p.comorb).lower()
    ]
