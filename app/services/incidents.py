import hashlib
from datetime import datetime, timezone
from app.schemas.model import ModelInput, ModelAssessment
from app.schemas.incident import Incident, Evidence
from app.services.policy import decide
from app.services.risk import risk_level

def make_incident(mi: ModelInput, a: ModelAssessment) -> Incident:
    d = decide(a)
    if d.disposition == "suppressed":
        raise ValueError("suppressed assessment is not an active incident")
    incident_id = "INC-" + hashlib.sha256(mi.sample_id.encode()).hexdigest()[:16]
    refs = set(a.evidence_refs)
    return Incident(id=incident_id, sample_id=mi.sample_id, type=a.event_type,
        title=a.ai_opinion or ("판단 불가 · 사람 검토" if d.disposition == "review" else a.event_type),
        primary_cam=mi.camera.id, location=mi.camera.location,
        risk=d.risk, risk_axes=a.risk_axes, level=risk_level(d.risk), confidence=a.event_confidence,
        needs_human_review=d.disposition == "review", uncertainty_reason=a.uncertainty_reason,
        evidence=[Evidence(frame_id=e.frame_id, timestamp_ms=e.timestamp_ms,
            t=f"{e.timestamp_ms//60000:02d}:{e.timestamp_ms//1000%60:02d}", text="Referenced observation")
            for e in mi.evidence if e.frame_id in refs],
        ai_opinion=a.ai_opinion, recommended_actions=a.recommended_actions,
        created_at=datetime.now(timezone.utc))
