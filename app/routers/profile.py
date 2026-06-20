"""Doctor profile and availability."""
from fastapi import APIRouter, Depends

from app.logging_conf import log
from app.schemas import AvailabilityRequest, Profile, ProfileUpdate
from app.store import Store, get_store

router = APIRouter(tags=["profile"])


@router.get("/profile", response_model=Profile)
def get_profile(store: Store = Depends(get_store)) -> Profile:
    with store.lock:
        return store.profile


@router.put("/profile", response_model=Profile)
def update_profile(
    body: ProfileUpdate, store: Store = Depends(get_store)
) -> Profile:
    with store.lock:
        data = store.profile.model_dump()
        data.update({k: v for k, v in body.model_dump().items() if v is not None})
        store.profile = Profile(**data)
        log.info("Profile updated: %s", store.profile.name)
        return store.profile


@router.post("/availability")
def set_availability(
    body: AvailabilityRequest, store: Store = Depends(get_store)
) -> dict:
    with store.lock:
        store.available = body.available
        log.info("Availability -> %s", body.available)
        return {"available": store.available}
