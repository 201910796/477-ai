# 프론트 API 계약 1.0 — Figma 확인 + 명시적 보완

출처: https://www.figma.com/design/pK7WGcPjkNjP7zaAbK4c13/477?node-id=61-14&m=dev
확인: 2026-10-06. 링크 node 61:14는 API 주석 페이지 60:2의 사각형입니다.
페이지 공통 API 60:1758 및 주석 61:18, 61:115, 61:182, 62:18, 62:106, 62:200을 읽었습니다.
docs/sources/figma-api-extract.json에 관련 원문을 보관했습니다. Figma는 수정하지 않았습니다.

| API | 역할/응답 | 현재 구현 |
|---|---|---|
| GET /api/status | 상태, active_count, total_cameras, timestamp | 개발/데모 상태; 실제 477 연결 주장하지 않음 |
| GET /api/cameras | 카메라 배열 id/name/location/stream_url/status/bbox | 9개 초기 로드 |
| GET /stream/{cam_id} | 영상 bytes | 로컬 MP4, 없으면 503, unknown camera 404 |
| WS /ws/attention | 서버 순서 incidents, cameras, level_counts, active_count | 최초 snapshot + 변경 push + 15초 snapshot |
| GET /api/pipeline/stats | total/candidates/reasoned/incidents/suppressed/needs_review/stage_trace | snapshot 카운트; 실측 latency=null |
| GET /api/suppressed | id/cam_id/stage1_label/ai_verdict/reason/risk/resumed_walking | 보관 및 restored 필드 |
| GET /api/incidents/{id} | 전체 Incident | typed schema, server rank/next_id |
| GET /api/incidents/{id}/clip | clip_url/start/end/bbox_track | JSON metadata; 데모 0~10초, 실제 crop 후속 구현 |
| POST /api/incidents/{id}/ack | action/note/to_operator | 상태·audit·idempotency·WS 반영 |
| POST /api/demo/step | step 1..6 | demo에서만; 6은 5의 상세 화면용 상태 |
| POST /api/suppressed/{id}/restore | 제외 알림 복구 | 추가 보완 API, 사람 검토로 복원 |

## Figma와 다른 부분은 프론트 팀과 반드시 맞추기
- 내부 id는 CAM_08, 화면 name은 CAM 08. Figma 표시 이름을 API id로 쓰지 않습니다.
- Figma 예시 risk=94, axes=(.9,.95,.8,.85)는 식으로 계산하면 89입니다. axes를 바꾸지 않고 서버 89를 사용합니다.
- review는 UI 표시 상태이며 위험 등급과 별개입니다. level_counts는 review를 우선 집계하여 중복 카운트를 피합니다.
- 실패는 risk=null, level=UNKNOWN을 허용합니다. 프론트는 '위험도 미측정'으로 표시하고 review 카드로 유지합니다.
- 원본에 없던 revision, 전체 cameras snapshot, Idempotency-Key 및 restore API를 추가했습니다.
- MP4는 파일 응답이며 RTSP/HLS 라이브 스트리밍 서버는 아닙니다. 영상은 사용자에게 공급받아야 합니다.

## ACK 의미 (원본 Figma에는 정확한 상태 전이 미정 → 본 키트의 합의 초안)
verify → acked, active queue에서 제외. dismiss → dismissed, 종결.
needs_review → open/review. confirm_review → open, review 해제(실제 위험 확정 후 다시 verify 필요).
request_dispatch → dispatch_requested=true 기록, 외부 신고/호출 없음. handover → assigned_operator 지정.
종결 dismissed에서 dismiss 외 액션은 409. handover에 to_operator 누락은 409.
잘못된 action/step은 422. 같은 key+같은 요청은 동일 응답, 같은 key+다른 요청은 409.
모든 POST는 Idempotency-Key 헤더 필수입니다. 재시도에는 같은 key, 새 행동에는 새 key 사용.
이 의미를 frontend가 구현 전에 확인하고 MAIN이 계약/테스트를 함께 고칩니다.

## WS
{event_type:'snapshot', schema_version:'1.0', revision, active_count, total_cameras:477,
 configured_cameras:9, suppressed_count, level_counts, incidents:[...], cameras:[...]}
클라이언트는 전체 snapshot으로 덮어쓰고 revision이 낮은 메시지는 무시합니다.
새 연결/재연결 첫 snapshot은 완전한 현재 상태입니다. cameras를 다시 GET할 필요가 없습니다.
같은 revision의 heartbeat는 무시해도 됩니다. 큐는 1개만 보관하여 느린 client에게 최신 상태를 전달합니다.
현재 event별 delta가 아니라 전체 snapshot으로 안정성을 우선했습니다.

## 실행 제한
memory repository 단일 프로세스, --workers 1. restart 시 incidents/audit/idempotency 초기화됩니다.
영구 DB·outbox·인증·rate limit·실시간 CV ingestion이 없는 개발용 서버입니다.
production 모드는 지원하지 않습니다. 외부 공유/운영 전에 docs/extension-plan.md 과제를 수행하세요.
