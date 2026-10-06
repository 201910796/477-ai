import asyncio
import time
from pydantic import ValidationError
from app.models.base import ModelAdapter
from app.schemas.model import ModelInput, ModelAssessment, ModelMetadata

async def execute(adapter: ModelAdapter, model_input: ModelInput, timeout_sec: float = 5.0) -> ModelAssessment:
    if timeout_sec <= 0:
        raise ValueError("timeout_sec must be positive")
    started = time.perf_counter()
    isolated = model_input.model_copy(deep=True)
    before = isolated.model_dump(mode="json")
    code = None
    try:
        raw = await asyncio.wait_for(adapter.evaluate(isolated), timeout=timeout_sec)
        result = ModelAssessment.model_validate(raw)
        if isolated.model_dump(mode="json") != before:
            raise ValueError("input mutation")
        if result.metadata.adapter != adapter.name:
            raise ValueError("wrong adapter identifier")
        if set(result.evidence_refs) - {e.frame_id for e in model_input.evidence}:
            raise ValueError("unknown evidence reference")
        if result.risk_axes is not None and not result.evidence_refs:
            raise ValueError("event has no evidence")
    except TimeoutError:
        code = "timeout"
    except (ValidationError, ValueError, TypeError):
        code = "schema_or_contract"
    except Exception:
        code = "provider_error"
    latency = (time.perf_counter() - started) * 1000
    if code:
        # Sanitized reason: never expose exception payloads, prompts or credentials.
        return ModelAssessment(event_type="uncertain", event_confidence=0, risk_axes=None,
            needs_human_review=True, uncertainty_reason=code,
            evidence_refs=[e.frame_id for e in model_input.evidence],
            recommended_actions=["verify"],
            metadata=ModelMetadata(adapter=adapter.name, model="unavailable", error_code=code, latency_ms=latency))
    return result.model_copy(update={"metadata": result.metadata.model_copy(update={"latency_ms": latency})})
