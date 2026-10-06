import argparse
import asyncio
import hashlib
import json
from pathlib import Path
from app.models.registry import get_adapter, ADAPTER_NAMES
from app.models.execution import execute
from app.schemas.model import ModelInput
from app.services.incidents import make_incident

async def run(adapter_name, path, timeout_sec=5, output=None):
    mi=ModelInput.model_validate_json(Path(path).read_text(encoding="utf-8"))
    adapter=get_adapter(adapter_name);r=await execute(adapter,mi,timeout_sec)
    canonical=json.dumps(mi.model_dump(mode="json"),sort_keys=True,separators=(",",":"))
    item={"sample_id":mi.sample_id,"adapter":adapter_name,"input_sha256":hashlib.sha256(canonical.encode()).hexdigest(),
        "prediction":r.model_dump(mode="json"),"error":r.metadata.error_code}
    if output:
        p=Path(output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(item,ensure_ascii=False)+"\n",encoding="utf-8")
    else: print(json.dumps(item,ensure_ascii=False))
    return item

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--adapter",choices=ADAPTER_NAMES,required=True);p.add_argument("--input",required=True)
    p.add_argument("--timeout-sec",type=float,default=5);p.add_argument("--output")
    a=p.parse_args();item=asyncio.run(run(a.adapter,a.input,a.timeout_sec,a.output))
    raise SystemExit(2 if item["error"] else 0)
