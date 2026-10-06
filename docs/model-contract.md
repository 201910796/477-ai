# 모델 계약 1.0

현재 스키마 소스: app/schemas/model.py. 초안은 계약 해시로 고정되어 있습니다.
MAIN이 변경 영향과 프론트 대응을 확인한 뒤 버전·문서·테스트를 함께 수정할 수 있습니다.

ModelInput: schema_version, 중립 sample_id, camera, window, clip_ref(선택), temporal_state, evidence[].
EvidenceFrame: frame_id, timestamp_ms, media_ref. 로컬 path 필드를 제거했습니다.
clip_ref/media_ref는 중립 token이며 app/models/media.py의 신뢰된 resolver가 실제 bytes로 변환합니다.
원본 경로, manifest, label, split, 파일명, 정답 타임스탬프를 provider request에 보내지 않습니다.
실제 adapter는 resolver를 생성자로 받도록 구현하고 MAIN이 registry에서 연결합니다.
현재 실제 adapter는 미구현이므로 resolver 자동 주입도 후속 과제입니다.

ModelAssessment: event_type, event_confidence, risk_axes(0..1 또는 null), needs_human_review,
uncertainty_reason, evidence_refs, metadata. extra 필드는 거절하고 NaN/Inf는 거절합니다.
operator evidence는 입력 frame_id와 timestamp_ms를 연결합니다. bbox/temporal observations는 추론으로 얻은 자료여야 합니다.
범용 dict 안의 텍스트까지 의미적으로 누수를 막을 수는 없으므로 extractor provenance와 표본 검토가 필수입니다.

모든 호출은 await execute(adapter, model_input, timeout_sec)를 사용합니다.
타임아웃, SDK 오류, 잘못된 스키마, input mutation, 잘못된 frame reference는 uncertain/review로 변환합니다.
실패 risk_axes=null, risk=null, level=UNKNOWN입니다. 이전 4등급에 UNKNOWN을 더한 명시적 프론트 계약 변경입니다.
실패는 실제 위험 0 또는 중간 위험 50이라는 뜻이 아닙니다.
asyncio.wait_for는 이벤트 루프를 차단하는 동기 GPU 연산을 끊지 못합니다. 실제 CV는 bounded process/GPU worker가 필요합니다.
취소 후 provider 요청이 남을 수 있어 retry·비용·worker 회수를 별도로 검증하세요.

mock_local_cv/mock_clef/mock_vlm은 오직 연결 점검용입니다. local_cv/clef_direct/general_vlm은 미설정 상태에서
명확한 provider_error를 반환하고 CLI exit 2가 됩니다. provider를 추정해 만들어 넣지 않습니다.

## 모델 독립성 및 공정성
A: Local CV가 원본 clip/frames로 추론. B: Clef 단독. C: VLM 단독.
공통 ModelInput은 bytes 접근 권한이 같은 고정 샘플이며 모델이 사용할 modality는 실제 capability와 함께 기록합니다.
B/C에 CV features를 함께 주면 결과 이름을 CV→Clef/CV→VLM로 적으세요. 이를 '완전 단독'이라고 표시하지 않습니다.
B/C 공통 feature cache는 label 없이 동일 extractor/version/window로 생성합니다.
연산 시간/비용은 extractor + bytes/frame prep + provider + routing 전체와 provider-only를 구분합니다.
CV가 네 위험축을 측정할 수 없다면 null/review와 지원 범위를 기록하고, 임의로 위험축을 만들어 성능을 비교하지 않습니다.
D: router→VLM은 A/B/C 평가와 candidate missed-event recall 확인 후 추가합니다.
