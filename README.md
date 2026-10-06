# 477 AI Role 1 — Validated Agent Kit v2

한국어 실행 안내: [시작하기.md](시작하기.md)
구조·완성도 평가: [reports/assessment-ko.md](reports/assessment-ko.md)
순서별 복사 지시문: prompts/00_audit.txt부터 09_frozen_test.txt까지.

## What runs now
- Typed model contracts; safe execution/failure policy; explicit mocks.
- Fixture -> adapter -> assessment -> incident -> GET integration.
- Demo 1..6, stateful ACK/audit/idempotency, WS snapshot push/reconnect, suppression restore.
- Licensed local MP4 file serving (media files not included).
- Manifest validation, batch evaluator, contract hashing and partitioned agent ownership.

## Not implemented yet
Real CV/Clef/VLM providers, video feature extraction/cache, real-provider resolver injection,
live ingestion/model-to-repository orchestration, persistent DB/outbox, operator auth and 477-camera scaling.
This is a development harness. Real adapter names explicitly fail until implemented; no silent mocks.

## Run
```bash
python -m venv .venv
# Windows: use .venv\Scripts\python.exe; Unix: .venv/bin/python
python -m pip install -e ".[dev]"
python -m pytest -q
python scripts/check_contracts.py
python -m uvicorn app.main:app --reload --host 127.0.0.1
python -m app.eval.runner --adapter mock_local_cv --input fixtures/model_input.json
```
Use your venv Python. One ASGI worker only. Open http://127.0.0.1:8000/docs.
POST endpoints require Idempotency-Key. APP_MODE=development disables the demo switch.

## Agent roles
MAIN owns integration/shared files. explorer/reviewer read only. model_engineer owns adapters only;
evaluation_engineer owns eval only; backend_engineer owns API/services/memory only.
See docs/ownership.md. Default one writer, optional disjoint parallel work after contract freeze.
No hardcoded model IDs: agents inherit the current selected account model.

## Dependencies and provenance
pyproject.toml has package discovery/build config and bounded dependency majors.
requirements-tested.txt records tested versions on Linux/Python 3.12; it is not an all-platform lock.
Sources: supplied harness ZIP + attached files + original AI answer + Figma API annotation page read 2026-10-06.
Original AI answer is preserved as source material, not authoritative executable instructions.
