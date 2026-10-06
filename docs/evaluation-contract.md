# 평가 계약

현재 구현: 단일 입력 runner, manifest 검사, JSONL batch runner, 기본 metrics.
실제 adapter·raw-video feature extraction·asset map 자동 주입은 후속 작업입니다.
동일 입력 JSON을 모든 adapter에 deep copy하고 input_sha256를 기록합니다.

| 지표 | 현재 정의 |
|---|---|
| macro F1 | 해당 split의 정답에 존재하는 클래스 평균; 클래스 목록 출력 |
| critical_event_recall | critical 정답 중 event_type 일치 비율; 실패는 miss |
| critical_escalation_recall | critical 정답 중 incident/review로 올린 비율 |
| false_alert_rate_on_normal | normal 정답 중 incident/review 비율 |
| human_review_recall | review 정답 중 review로 보낸 비율 |
| error_rate | timeout/schema/provider_error / 전체 샘플 |
| latency_ms_mean | 실행 래퍼의 벽시계; 전처리 미포함이면 provider 평가로 표시 |
| cost_usd_mean_measured | 측정 가능한 샘플만 평균, coverage 필수 |
| risk_axis_mae_measured | 정답과 예측 둘 다 있는 축 MAE, pair_count 함께 표시 |

분모 0인 지표는 null. 실패 샘플을 전체 결과에서 삭제하지 않습니다.
모든 실패를 review로 보내면 escalation recall은 높지만 event recall은 낮아질 수 있습니다. 둘을 함께 봅니다.
mock은 실제 batch 평가에서 금지합니다. real adapter 미구현은 모든 실패로 기록하고 exit2가 됩니다.
이런 결과를 모델 성능으로 발표하지 않습니다.

추가 과제: p50/p95/p99 latency, 클래스별 recall/support, risk coverage, grouped rank agreement,
후보 생성부터의 end-to-end critical recall, false alarms per camera-hour, 반복 run/CI/seed,
provider retry/cancellation 비용, CV feature/preprocess 시간·장비·sample budgets 기록.
특히 event clip 단위 정상 FPR와 장시간 카메라당 오경보 수는 다른 지표입니다.

B가 features-only면 B/C 모두 같은 관측 feature로 비교한 실험과 raw-frame 비교 실험을 따로 씁니다.
프레임 수/해상도/기간/feature version, provider model/prompt version, token/usage/cost, 코드 commit을 저장하세요.
누락된 risk 정답·비용·rank 시나리오는 N/A로 표시합니다.

validation: python -m app.eval.batch --manifest data/manifest.jsonl --adapter local_cv --split validation --output outputs/A-validation-001
test: 같은 명령에 --split test --allow-test --lock data/dataset.lock.json --run-config data/run_config.json
동일 output 경로를 재사용하지 않습니다. frozen run config는 실제 모델 버전/전처리/prompt/코드 기록으로 바꿉니다.
현재 hash guard는 manifest와 config bytes 변경을 막습니다. 코드/weight/cache 전체를 강제 검증하지 않으므로
MAIN이 commit·weight/cache checksum을 별도 보관하고 재현성을 확인해야 합니다.
