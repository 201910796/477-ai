# 실제 상태 — 검증 완료 항목과 후속 과제

## 하네스 v2에서 완료
- [x] 공통 typed I/O, opaque media refs, bounds/extra 필드 검증
- [x] shared execution: timeout/schema/provider/evidence/input-mutation 실패 → review
- [x] mock 이름 분리와 real 미설정 명시
- [x] fixture → adapter → assessment → Incident → GET vertical slice
- [x] demo 1..6, ACK 상태/audit/idempotency, WS push/reconnect snapshot
- [x] suppressed restore API, UNKNOWN 위험 표현
- [x] source/scenario/hash 기반 manifest validation + batch evaluator 기본 metrics
- [x] MAIN + 5 role ownership, handoff, 계약 변경 hash 검사
- [x] 한국어 단계별 prompts/시작 안내/평가 보고서

## 순서대로 남은 작업
- [ ] P0 사용자 환경에서 설치/pytest/Codex 에이전트 로딩 확인
- [ ] P0 frontend 담당자에게 UNKNOWN/카메라ID/WS/ACK/Idempotency 의미 확인
- [ ] P0 실제 모델→repository 실행 wiring + 실제 evidence media URL
- [ ] P1 Clef provider/API 접근/입력 modality/SDK 공식 문서 확인 (진행 전 명확히)
- [ ] P1 data/asset-map ingestion + fixed frame sampling + neutral cache/provenance
- [ ] P1 local_cv 실제 구현 + decode/track/pose 워커 + 지원 이벤트 검증
- [ ] P1 clef_direct 실제 구현; 접근 불가면 BLOCKED 기록
- [ ] P1 general_vlm 실제 구현 + schema constrained output
- [ ] P2 동일 validation 샘플 세 모델 run + 오류/비용/전처리 coverage
- [ ] P2 dataset/run-config/코드·weight/cache 고정 후 test 1회
- [ ] P2 후보 누락을 포함하는 pipeline end-to-end 평가
- [ ] P3 실제 video clipping/bbox/frame evidence, SQLite/PostgreSQL transactions/outbox
- [ ] P3 operator auth, audit retention, multi-worker load/camera throughput
- [ ] Stretch router→VLM, multi-camera merge

실제 모델/실제 데이터 완료는 mock 테스트 통과로 체크하지 않습니다.
