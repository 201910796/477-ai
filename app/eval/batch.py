import argparse
import asyncio
import hashlib
import json
from pathlib import Path
from app.eval.dataset import validate_manifest, load_input
from app.eval.metrics import summarize
from app.models.registry import get_adapter, ADAPTER_NAMES
from app.models.execution import execute

async def run_batch(manifest, adapter_name, split, output, lock=None, run_config=None, allow_test=False):
    if adapter_name.startswith("mock_"):raise ValueError("mock prohibited in dataset metrics")
    manifest=Path(manifest);rows=validate_manifest(manifest)
    digest=hashlib.sha256(manifest.read_bytes()).hexdigest()
    config_digest=None
    if split=="test":
        if not (allow_test and lock and run_config):raise ValueError("test requires --allow-test, --lock and --run-config")
        frozen=json.loads(Path(lock).read_text(encoding="utf-8"))
        config_digest=hashlib.sha256(Path(run_config).read_bytes()).hexdigest()
        if frozen["manifest_sha256"]!=digest or frozen["run_config_sha256"]!=config_digest:raise ValueError("frozen artifact changed")
        config=json.loads(Path(run_config).read_text(encoding="utf-8"))
        if adapter_name not in config["adapters"]:raise ValueError("adapter absent from frozen run config")
        timeout=config["timeout_sec"]
    else:timeout=5.0
    selected=[r for r in rows if r.split==split]
    if not selected:raise ValueError("no samples for requested split")
    output=Path(output)
    if output.exists():raise ValueError("output exists; choose a new run directory")
    output.mkdir(parents=True)
    records=[];adapter=get_adapter(adapter_name)
    with (output/'predictions.jsonl').open('w',encoding='utf-8') as f:
        for row in selected:
            mi=load_input(row,manifest.parent)
            assessment=await execute(adapter,mi,timeout)
            data={"sample_id":row.sample_id,"adapter":adapter_name,"split":split,
                "input_sha256":hashlib.sha256(mi.model_dump_json().encode()).hexdigest(),
                "manifest_sha256":digest,"run_config_sha256":config_digest,
                "prediction":assessment.model_dump(mode="json"),
                "ground_truth":{"event_type":row.event_type,"critical":row.critical,
                    "needs_human_review":row.needs_human_review,"risk_axes":row.risk_axes.model_dump() if row.risk_axes else None}}
            # Labels are added only after inference returns; never passed to adapter.
            records.append(data);f.write(json.dumps(data,ensure_ascii=False)+'\n');f.flush()
    metrics=summarize(records)
    (output/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    return metrics
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--adapter',choices=ADAPTER_NAMES,required=True)
    p.add_argument('--split',choices=['validation','test'],default='validation');p.add_argument('--output',required=True)
    p.add_argument('--lock');p.add_argument('--run-config');p.add_argument('--allow-test',action='store_true')
    a=p.parse_args();m=asyncio.run(run_batch(a.manifest,a.adapter,a.split,a.output,a.lock,a.run_config,a.allow_test))
    print(json.dumps(m,indent=2));raise SystemExit(2 if m['error_rate'] else 0)
