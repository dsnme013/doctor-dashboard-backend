"""Application factory."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.logging_conf import configure_logging
from app.routers import (bookings, health, messages, patients, profile, queue,
                         reports, schedule)

API_PREFIX = "/api/v1"


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title=settings.app_name, version=settings.version, docs_url="/docs")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for r in (health, queue, bookings, schedule, patients, messages, reports, profile):
        app.include_router(r.router, prefix=API_PREFIX)

    return app
