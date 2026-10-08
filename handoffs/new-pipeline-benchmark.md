# new_477_piprline handoff

User requested a single full YOLO→Clef→VLM benchmark, 64 total frames/item,
source-resolved truth/output and one CSV row/item, delivered as a standalone folder.
Original folders and baseline results remain read-only. MAIN implementation in progress.

Sequential real agents:
1. `/root/new_pipeline_inventory` explorer, `.codex/agents/explorer.toml`, read-only,
   6video ffprobe/SHA matches; no supplied GT/box/routing labels. No edits/test/API.
2. `/root/new_pipeline_metrics` evaluation_engineer config, only
   app/eval/new_pipeline_metrics.py and tests/eval/test_new_pipeline_metrics.py.
   Focused38PASS0.43s; missing labels null, reviewed denoms preserve skipped errors.
3. `/root/new_pipeline_contract_review` reviewer config, read-only review pending.

MAIN: new folder contracts/runner/neutral input preparation/README, common execution
boundary addition `execute_pipeline_stage` exported to portable package. Full425PASS
52.22s (existing deprecation warning1). Contracts initially flagged authorized execution
change; MAIN updated lock after tests, rerun Frozen contracts match. Portable44PASS0.47s.

Inputs: P001~P0066solos, P007 SRC01+02, P008 SRC05+06,
P009 SRC01+03+05, P0101..4, P0111..5, P0121..6; total12items768slots.
Same event only05/06 documented; independent clip bundles otherwise, no simultaneity/
precise sync implied. PNG frames/hash manifest and neutral MP4s included. No originals edits.

`prepare.py` actual exit0, items12/frame_slots768/original_unchangedtrue/paid_calls0.
`inspect_media.py` actual exit0; MAIN inspected first/mid/last6sources contact sheet.
SRC05/06finalsample black; recorded quality issue, never change favorable sample allocation.

Scored-model evaluation remains blocked pending reviewed bbox/routing/eventtruth;
candidateREADMEreference notconverted into affirmedlabels. APIs no newcalls due
remaining0.00841472 reservation budget under prior cumulative5USD authorization.
No new ledger allowance, paid GPU or training. Final CV run/CSV/reviewer pending.

Reviewer initial BLOCK repaired sequentially: MAIN CV output gate before Clef, strict
bool route outputs and metric/safety propagation; evaluation agent follow-up45PASS
for blocked/timeout/skipped source classification. MAIN full432PASS57.98s/contracts
match/portable56PASS. Reviewer rereview PASS actual46+56focused,791locked entries
mismatch0 and identical87-request ledger. New CV writer `/root/new_pipeline_cv`
owns app/models/adapters/new_pipeline_cv.py + tests/models/test_new_pipeline_cv.py only.

Preflight actual exit0:12items,paid0, reservationforecast1.08251136 vsremaining.00841472.
Blackfinalframes measured SRC05#918@30.6 and SRC06#954@31.8 meanpixel0; inspection
quality artifact covers only18(first/mid/last) images, not fullsemanticGT.

User steering: explicit 2026-10-08 authorization to run both DeepSeek/Clef without
previous cost cap. MAIN paid_authorization.json scopes this new12-item run and keeps
legacy87requests/reservations. Standalone budget can honor explicit uncapped approval
but stillrequires --allow-paid and noautomaticretries. Original oldledger remains intact.
CVagent was interrupted beforewriting ownedfiles; MAIN verified nonexistentpaths
and resumed same agent sequentially. Portable worker copy (notoriginal) adaptsneutral
SRC01..06 and alternative explicitlocal .pt COCOdetectors.

CV writer finished actual focused15PASS1.93s, filesonlyowned; MAIN exported portable
CV/worker/test copies, full447PASS59.21s/contracts match/standalone72PASS2.61s.
`/root/new_pipeline_clef` sequential model_engineer now owns only
app/models/adapters/new_pipeline_clef.py and tests/models/test_new_pipeline_clef.py.
No actual models/API run yet; adapter tests are explicitly offline payload/worker fixtures.
MAIN adds evaluator-lock hashes before API, truth JSON schema/reviewer checks,
stage actual-vs-planned input counts, and suite preflight/wall timing. Current source GT
allpending. Defaultstop fallback preserved until explicit fullrun profile chosen.

Clef task completed only2ownedfiles focused38PASS0.74s; MAIN source review/export,
full485PASS59.23s/contracts match/portable111PASS3.66s. ActualAPI0untilfinalgate.
`/root/new_pipeline_vlm` nextsequential writer onlynew VLM adapter/tests, source-resolved
64JPEG DeepSeek interface. MAIN selected explicit config/full_pipeline.json profile
fallbackinvoke on every non-ok Clef result, including model/conversion errors and
Clef skipped after upstream YOLO failure (not on valid no_action); baseprofile remainsstop.
Truth schema initiallyinvalidJSON caughtinpreflight (benchmarkerror), MAIN fixedbefore
API; regression9PASS andactualpreflight12PASS costcapremoved remainingnull asauthorized.
No initialfailedpreflight judgeda model error. Evaluationlockwillfreezebeforepaidcall.

VLM writer completed exactly2ownedfiles focused43PASS28.54s (1existingwarning).
MAIN exportedall3+tests, actualfull528PASS92.88s/contractsFrozenmatch/portable154PASS45.06s.
Readiness reviewer resumedsequentially tocheck alladapters/budgetadditionalapproval/
CSVsemantics/source scopes beforeactualcalls. Requestcapacity preflight usingprevious
CV03 (ONLYserializerfit, notnewresultreuse)119762bytes2typedquestions api0.
Realexecutionpending; ENV date switched2026-10-09 Asia/Seoul, originalapproval datedOct08.

Final reviewer BLOCK: malformed worker raw response was overwritten by outer error
handler. CV owner resumed sequentially, wrote transport error to a separate file,
and proved sentinel raw text preserved with statuserror/outputNone/executedNone.
Focused16PASS2.61s; MAIN reexport/full529PASS92.27s/contracts match/portable155PASS32.33s.
Reviewer rechecking actual execution readiness. No model/API calls before PASS.

Reviewer readiness PASS with independentCV16PASS2.38s/contracts match; no edits/API.
MAIN froze evaluation.lock.json; final actual preflight12PASS, paidcalls0, forecast
reservation1.08251136USD with remainingnull explicit scoped uncapped authorization.
Actual sequential12run started under results/full_pipeline_v1; CPUyolo26s/ByteTrack,
existingClef and DeepSeek-flash. One repeat; no previous result reuse.

Actual full_pipeline_v1 P001: YOLOok, Clef input_contract_invalid beforeAPI
(benchmarkerror/executedfalse), DeepSeek fallbackok. MAIN stopped runner and confirmed
no remaining python processes, preserved partialCSV1row/P002partial artifacts.
P001 VLM usageestimate0.0200322USD, invoiceunknown. No Clef paidcall onthisitem.
Sequential Clefowner resumed onits2files todiagnose actual CV->Clef mapping offline;
must fix and rerun gates/review before new full_pipeline_v2 output, never overwritev1.

Exact actual failure cause: observations=1 track max_observation_gap_sec=null is
legitimate unknown, Clef numeric serializer incorrectly rejected it. Owner fixed
only2files preservingthatnull onlyforoneobservation; no0invented, nonfinite/bounds
and othernumericchecks retained. OfflineactualP001 serializationPASS27980bytes,
uncertaintrue. Focused43PASS0.60s; MAINreexport/full534PASS92.34s/contracts match/
portable160PASS32.50s. Sequential reviewer rechecking before v2actualrun.

Reviewer PASS with independentactualserializer27980bytes/43testsPASS0.82s, API0.
MAIN checked official Cloudflare Clef $0.24/M input and DeepSeek currentflash
off-peak rates0.15miss/0.003hit/0.60output USDperM; UTC2026-10-08 15:32 outside
peak windows. Selectedprofile records theseusageestimate rates (notinvoice).
Actual fresh12run started under results/full_pipeline_v2; v1 untouched.
