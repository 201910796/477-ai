import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.config import Settings
from app.repositories.memory import MemoryStore
from app.services.events import SnapshotHub

def create_app(settings: Settings | None = None):
    settings=settings or Settings.from_env()
    app=FastAPI(title="477 AI Role 1 Development Backend",version="0.2.0")
    app.state.settings=settings;app.state.store=MemoryStore();app.state.hub=SnapshotHub();app.state.lock=asyncio.Lock()
    app.add_middleware(CORSMiddleware,allow_origins=list(settings.origins),allow_credentials=False,
        allow_methods=["GET","POST"],allow_headers=["Content-Type","Idempotency-Key"])
    app.include_router(router)
    return app
app=create_app()
