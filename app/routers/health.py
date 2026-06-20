"""Health-check endpoint."""
from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    return {"ok": True, "ts": datetime.now(timezone.utc).isoformat()}
