from statistics import mean
from app.services.policy import decide
from app.schemas.model import ModelAssessment
CLASSES=("normal","collapse","conflict","intrusion","loitering","uncertain")
def ratio(n,d):return n/d if d else None

def summarize(records):
    if not records:raise ValueError("empty evaluation")
    pairs=[(r["ground_truth"],ModelAssessment.model_validate(r["prediction"])) for r in records]
    # Present ground-truth classes only; explicitly reported, failures still in denominators.
    classes=[c for c in CLASSES if any(g["event_type"]==c for g,_ in pairs)]
    f1=[]
    for c in classes:
        tp=sum(g["event_type"]==c and a.event_type==c for g,a in pairs)
        fp=sum(g["event_type"]!=c and a.event_type==c for g,a in pairs)
        fn=sum(g["event_type"]==c and a.event_type!=c for g,a in pairs)
        f1.append(2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0)
    critical=[(g,a) for g,a in pairs if g["critical"]]
    normal=[(g,a) for g,a in pairs if g["event_type"]=="normal"]
    review=[(g,a) for g,a in pairs if g["needs_human_review"]]
    costs=[a.metadata.estimated_cost_usd for _,a in pairs if a.metadata.estimated_cost_usd is not None]
    lat=[a.metadata.latency_ms for _,a in pairs if a.metadata.latency_ms is not None]
    errors=[sum(bool(a.metadata.error_code) for _,a in pairs),len(pairs)]
    axis_errors=[]
    for g,a in pairs:
        if g.get("risk_axes") and a.risk_axes:
            axis_errors.extend(abs(g["risk_axes"][k]-v) for k,v in a.risk_axes.model_dump().items())
    return {"n":len(pairs),"macro_f1":mean(f1),"macro_f1_classes":classes,
        "critical_event_recall":ratio(sum(g["event_type"]==a.event_type for g,a in critical),len(critical)),
        "critical_escalation_recall":ratio(sum(decide(a).disposition!="suppressed" for _,a in critical),len(critical)),
        "false_alert_rate_on_normal":ratio(sum(decide(a).disposition!="suppressed" for _,a in normal),len(normal)),
        "human_review_recall":ratio(sum(decide(a).disposition=="review" for _,a in review),len(review)),
        "error_rate":ratio(*errors),"latency_ms_mean":mean(lat) if lat else None,
        "cost_usd_mean_measured":mean(costs) if costs else None,"cost_coverage":len(costs)/len(pairs),
        "risk_axis_mae_measured":mean(axis_errors) if axis_errors else None,
        "risk_axis_pair_count":len(axis_errors)//4,
        "mock_count":sum(a.metadata.is_mock for _,a in pairs)}
