"""Uvicorn entrypoint: `uvicorn main:app --reload --port 8000`."""
from app.main import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    from app.config import settings

    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
