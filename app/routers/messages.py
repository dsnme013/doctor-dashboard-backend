"""Patient chat threads."""
from fastapi import APIRouter, Depends, HTTPException

from app.logging_conf import log
from app.schemas import Message, SendMessageRequest, Thread, ThreadSummary
from app.store import Store, get_store

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("", response_model=list[ThreadSummary])
def list_threads(store: Store = Depends(get_store)) -> list[ThreadSummary]:
    with store.lock:
        out: list[ThreadSummary] = []
        for pid, th in store.threads.items():
            p = store.patients[pid]
            out.append(ThreadSummary(
                patient_id=pid,
                name=p.name,
                color=p.color,
                unread=th.unread,
                last=th.msgs[-1] if th.msgs else None,
            ))
        return out


@router.get("/{pid}", response_model=Thread)
def get_thread(pid: int, store: Store = Depends(get_store)) -> Thread:
    with store.lock:
        th = store.threads.get(pid)
        if th is None:
            raise HTTPException(status_code=404, detail="thread_not_found")
        th.unread = False
        return th


@router.post("/{pid}", response_model=Thread)
def send_message(
    pid: int, body: SendMessageRequest, store: Store = Depends(get_store)
) -> Thread:
    with store.lock:
        th = store.threads.get(pid)
        if th is None:
            store.patient_or_404(pid)  # 404 if patient unknown
            th = Thread(patient_id=pid)
            store.threads[pid] = th
        th.msgs.append(Message(who="me", t="Just now", txt=body.text.strip()))
        log.info("Message sent to patient_id=%s", pid)
        return th
