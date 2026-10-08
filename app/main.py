import asyncio
from weakref import WeakValueDictionary
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.config import Settings
from app.repositories.memory import MemoryStore
from app.services.events import SnapshotHub
from app.services.incidents import apply_assessment, lookup_assessment
from app.models.base import ModelAdapter
from app.models.execution import execute
from app.models.registry import get_adapter
from app.models.media import MediaResolver
from app.models.adapters.ingestion import MediaIngestion
from app.schemas.model import ModelInput

def create_app(settings: Settings | None = None, *, adapter: ModelAdapter | None = None,
               media_resolver: MediaResolver | None = None):
    settings=settings or Settings.from_env()
    app=FastAPI(title="477 AI Role 1 Development Backend",version="0.2.0")
    app.state.settings=settings;app.state.store=MemoryStore();app.state.hub=SnapshotHub();app.state.lock=asyncio.Lock()
    if media_resolver is None and settings.asset_map_path is not None:
        media_resolver = MediaResolver.from_asset_map(settings.asset_map_path, settings.asset_root)
    app.state.model_adapter = adapter if adapter is not None else get_adapter(
        settings.model_adapter, resolver=media_resolver)
    app.state.media_resolver = media_resolver
    app.state.media_ingestion = MediaIngestion(media_resolver) if media_resolver is not None else None
    sample_locks: WeakValueDictionary[str, asyncio.Lock] = WeakValueDictionary()

    async def prepare_model_input(model_input: ModelInput):
        if app.state.media_ingestion is None:
            raise ValueError("media resolver is not configured")
        return await app.state.media_ingestion.prepare(model_input)

    app.state.prepare_model_input = prepare_model_input

    async def ingest_model_input(model_input: ModelInput):
        # Internal integration seam; live ingestion and real media remain separate work.
        model_input = ModelInput.model_validate(model_input)
        # Waiting callers keep a strong reference; unused locks are released automatically.
        sample_lock = sample_locks.setdefault(model_input.sample_id, asyncio.Lock())
        async with sample_lock:
            async with app.state.lock:
                cached = lookup_assessment(app.state.store, model_input)
                if cached is not None:
                    return cached
            assessment = await execute(app.state.model_adapter, model_input, settings.model_timeout_sec)
            async with app.state.lock:
                applied = apply_assessment(app.state.store, model_input, assessment)
                if applied.changed:
                    app.state.hub.publish(app.state.store.snapshot())
                return applied

    app.state.ingest_model_input = ingest_model_input
    app.add_middleware(CORSMiddleware,allow_origins=list(settings.origins),allow_credentials=False,
        allow_methods=["GET","POST"],allow_headers=["Content-Type","Idempotency-Key"])
    app.include_router(router)
    return app
app=create_app()
