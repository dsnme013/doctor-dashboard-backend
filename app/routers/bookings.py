"""Accept / reschedule bookings."""
from fastapi import APIRouter, Depends

from app.logging_conf import log
from app.schemas import Patient, RescheduleRequest
from app.store import Store, get_store
from fastapi import HTTPException

router = APIRouter(prefix="/booking", tags=["bookings"])


@router.post("/{pid}/accept", response_model=Patient)
def accept_booking(pid: int, store: Store = Depends(get_store)) -> Patient:
    with store.lock:
        p = store.patient_or_404(pid)
        if p.status == "accepted":
            raise HTTPException(status_code=409, detail="already_accepted")
        p.status = "accepted"
        log.info("Booking accepted: patient=%s time=%s", p.name, p.time)
        return p


@router.patch("/{pid}/reschedule", response_model=Patient)
def reschedule_booking(
    pid: int, body: RescheduleRequest, store: Store = Depends(get_store)
) -> Patient:
    with store.lock:
        p = store.patient_or_404(pid)
        if body.slot not in store.open_slots:
            raise HTTPException(status_code=409, detail="slot_not_available")

        old_time = p.time
        p.time = body.slot
        p.status = "rescheduled"

        # Free the patient's old slot, occupy the new one.
        for s in store.schedule:
            if s.pid == pid:
                s.pid, s.open, s.now = None, True, False
        for s in store.schedule:
            if s.open and body.slot.startswith(s.t):
                s.open, s.pid = False, pid
                break

        store.open_slots.remove(body.slot)
        store.open_slots.append(old_time)
        log.info("Rescheduled %s: %s -> %s", p.name, old_time, body.slot)
        return p
