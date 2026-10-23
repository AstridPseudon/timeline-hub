# A2 P3 settled-owner boundary diagnosis

Verdict: **actual 15659 cause UNKNOWN / INSUFFICIENT EVIDENCE**. The requested read-only diagnosis is complete as a precise missing-boundary-fields return. As of 2026-10-23T19:34:58Z, the shared design area contains the Farm result and requests for a safe export, but no published safe 15659 trace projection. No raw archive or Farm snapshot was accessed, copied, fetched, or assumed locally available. Trace retention itself is owner-reported, not independently verified here.

## Provenance and actual failure

Read PLAN §3 A2/P3 and design/commit-v2.md §§1–5; consumed peer-app2-to-app-20261023T1922-P1-reviewed-P3-owner-boundary-need.md, handoff-ap2-P3-15659-owner-boundary-review-1918.md, Farm farm-p3-run4.md and peer-farm-to-app2-20261023T1915-p3-result-RED.md, and the 19:22/19:34 safe-export requests.

- Selected source: App 2107e1870e51c650d59315f4cc1ab6af338f198c / tree a3ff3584e9b559bbb3c3a82b77be7516ed8e761c; Agent 079580ca; Runtime 2a9e347ff. This worker directly verified the App identity only; Agent/Runtime selections are Farm-reported. No current-Agent GO claim.
- Farm preflight app-ap2-P3-gate5-h6-0348-preflight-1023190416-17114: reported PASS, exit 0, 97s; body not run. No new preflight.
- Original app-ap2-P3-gate5-h6-0348-1023190626-15659: reported FAIL, exit 1, 224s; ready:false for 90s at three-products.spec.ts:1275, entering original case :1533, call :1537, before the first gesture :1539.
- Only reported raw trace location: Farm snapshot's test-results/three-products/three-products-M2-real-gat-710b3-rt-and-undo-preserve-intent/trace.zip. Farm publication time 19:15Z, independent review 19:18Z; actual trace event times, member offsets, mounted project/timeline, basis pair, identity presence, owner state and error are UNKNOWN here.
- Source chain: Farm result -> Proof 1918/1922 review -> normal safe-export requests -> this source audit. No actual trace events have crossed that chain into this report. Absence of a published projection does not establish that the trace was lost.

The gate correctly requires a new durable empty owner relative to the pre-open owner set. commandOutboxes reads actual IndexedDB owners, filters timeline, and does not claim an owner (support/app.ts:199–217). The assertion observes persistence, not private hook readiness: a raw settled record alone cannot prove localOwner.handoff exists. Conversely ready:false does not distinguish absent DB, no matching/new owner, pending/intents, scope mismatch, or initialization error/cancellation. Keep this valid boundary unchanged.

## Source stages and exact requested safe fields

Return these fields ONLY if captured in the existing 15659 artifacts; otherwise mark each UNKNOWN/not captured. No new hook probe, collector, browser or run is requested. For each observation retain exact case, relative/absolute time when available, source artifact/member and event/line boundary, and whether it is a wire, DOM, storage or actual mounted observation. Do not turn wire success into a mounted-state observation.

| Stage, App source | Required safe projection from the existing artifact |
| --- | --- |
| Entry, useTimelineSave.ts:78–83,117–155 | Mounted provider/project/timeline correlation; capability booleans for loadTimelineCommandBasis, commitTimeline, getRecoverableIdentity; original.head presence and paired revision/publication; original editProjection kind; editSeq versus savedSeq equality; localOwner started/closed/generation/session presence. Preserve UNKNOWN for uncaptured hook fields. |
| Verified original, useTimelineSave.ts:156–179; timelineLocalSaveHandoff.ts:99–112 | Basis read start/end/failure; sanitized route class, method/status and safe error code; history page/cursor head-pair consistency; parent/shot/internal closure reads and validation outcome; displayed-original versus verified project/timeline/head pair equality; authoringBundleFromDocument and checkSource success/failure. HTTP 200 alone does not establish these local checks passed. |
| Authenticated recoverable identity, useTimelineSave.ts:181–184; runtime/client.ts:460–466 | Await start/end/error; actor/realm PRESENT booleans and realm-consistency boolean only; cached-session versus fresh-handshake distinction only if captured. No actor/principal/realm values, token, auth/header/cookie or credentials. Correlate resulting scope equality without disclosing identity values. |
| Lifecycle boundaries, useTimelineSave.ts:117–128,174–184,214,227,241–242 | Effect cleanup/unmount/provider-or-timeline replacement; generation before/after and current equality; cancelled/closed/editSeq changed at each await; previousDisposal pending/resolved/error. Absent lifecycle events must remain UNKNOWN, not false. |
| Session entry, localSaveSession.ts:65–100,242–245 | Session creation entered/completed/failed; initial canonical project/timeline/parent revision versus requested scope/head checks; storage.list start/end and recoverable owner count. Presence of a fresh owner cannot be inferred from an event/head feed. |
| Durable owner, commitOutbox.ts:116–121,151–154,205–248,252–276,285–300,544–549; localSaveSession.ts:208–239 | IndexedDB availability/open/upgrade/blocked/error; readonly list completion; Web Locks availability/acquisition/refusal; create versus recover branch; owner-record put transaction completion/abort/error; generation and same-scope equality; claimed.read completion; intent/pending counts and owner new-versus-previous equality. Use stable nonsecret owner aliases if needed. No raw outbox payload/request/key. |
| Recovery and final publication, useTimelineSave.ts:214–239 | Recoverable count 0/1/multiple, recover enter/complete/error, current generation, session status/owner presence, optional flush/latest-history outcome, handoff assigned or not, final changed callback applied/ignored, localSaveState status and sanitized error code/class/stage. DOM recovery notice/pageerror/console event if actually captured; do not invent a UI error from caught hook state. |
| Readiness observation, three-products.spec.ts:1263–1275 | Previous-owner alias set, observed matching timeline owner aliases/counts, pending/intents counts, notice projection and times throughout the 90s interval, tied to this case. Identify whether DB absent, matching records absent, only previous owners, or unsettled records; otherwise UNKNOWN. |

The initial path first lists storage, then creates/claims an owner when no recoverable work exists. commitOutbox persists the generation/record transaction before invoking the hold callback; localSaveSession reads that record before publishing saved and resolving mounted. Recovery takes a distinct branch. Identity may reuse ensureSession, so lack of a new handshake request does not prove getRecoverableIdentity was skipped or failed.

## Independent source counterexample, not the actual diagnosis

There is a bounded initialization-lifecycle failure schedule in the inspected source; it requires no failing server or storage operation:

1. With a clean original head H, start the originalRead promise and set localOwner.started=true/headKey=H (useTimelineSave.ts:155–177). Keep that read pending.
2. Replace assetResolver while keeping provider, timelineId and head H unchanged. resolveAssetUrl changes (:43–49), so the initialization effect dependency changes (:242), while localOwner memo identity remains unchanged (:78–82). Its cleanup sets cancelled=true (:241); the owner-lifetime cleanup (:117–128) does not run for this dependency-only change.
3. The replacement effect sees started=true and headKey===originalHeadKey and returns (:133–135), without a replacement read or resetting started.
4. When the original read succeeds, the original ready task throws at :178–179 because cancelled is true, before the identity await and before createLocalSaveSession. isCurrent still holds for this owner/generation, so :236–238 publishes error. With the same owner/head there is no initialization retry through that effect.

This is a source-level counterexample conditional on that dependency transition, not an executed test or proof that 15659 experienced it. The actual assetResolver/dependency identity changes and cancellation state are missing. No speculative fix is authored or prescribed; the manager should correlate existing trace evidence before assigning repair. A static schedule cannot replace the required actual causal evidence.

## Preservation and verification

Worktree source unchanged. Exact commands and observed results:

- git rev-parse HEAD -> 2107e1870e51c650d59315f4cc1ab6af338f198c.
- git rev-parse HEAD^{tree} -> a3ff3584e9b559bbb3c3a82b77be7516ed8e761c.
- git status --porcelain=v1 -> empty.
- git diff --exit-code HEAD -> exit 0, empty.
- git diff --check -> exit 0, empty.
- git rev-parse HEAD:tests/e2e/local/three-products.spec.ts and git hash-object tests/e2e/local/three-products.spec.ts -> both 37caf28577d42fbe98afd2320dffa3c72e6e74b1 (entire original Gate5-containing file).
- Python standard-library hashlib SHA-256 audit: read three-products.p1-chain.spec.ts as bytes; find first and second occurrences of the literal test('P1 split -> trim new clip:; hash first-title-to-next-title and second-title-to-EOF. First 11,614B -> 4b04ad7ef74b8106244d87c23d12c7a18da251dd8f5a746f42d3221a72ea8b7f; second 7,612B -> 2f7501184477c8aec38d3cd289dd13c0d011fa8f69ecd43378f24f6c3100a2f7.
- Read-only rg/nl/sed source and design searches -> inspected the stages above; no published safe 15659 projection located at the stated cutoff.
- Targeted tests, typecheck and lint: N/A, unchanged code/read-only task. No fresh PASS claimed. No test-service request or full suite.

Audited source blobs: useTimelineSave.ts 0f888f7c843ce7f8179c70b34b373a030c00d22a; timelineLocalSaveHandoff.ts 1c6176d2abc3d06f5b27b7c391a2c22c292ea4d1; localSaveSession.ts 83d2166d57c05980d3bd8ebc9bbd79a37c3c5e44; commitOutbox.ts 8f6c157b910b12b900b61d45354442e3474c2975; runtime/client.ts 6e9a894d09959ed9fa8f1c0c6f01b9423441c59b; runtime/dataProvider.ts fea25c9f28fa617eb3cf252a0a86818ef1218be2.

Existing NumberInput1635 and mounted replay1736/1744 controls were reused only for their documented limits: simulated execution/lifecycle evidence cannot prove this initial-owner failure or current real Gate5 success. No controls were repeated. This is distinct from P1 recovery/no-second-POST triage.

All contract/request/reply/undo/canonical reload/zero-old-route obligations remain preserved by the empty product/test diff. No product, test, collector, schema, generated, config, pin, lock, environment, dependency, bench, kit or Git changes. No archive transfer, credentials, HTTP, browser, service, seed, preflight, experiment, control loop, daemon/dispatcher call or deletion. No denied 1536 publication reused.

## Decisions, blocker and next step

Preserved the settled plan, readiness assertion and 90s bound. Returned UNKNOWN because the original failure lacks a published safe causal projection; did not assign Runtime/Agent fault or propose a speculative repair. No plan decision was shown wrong.

Evidence blocker: normal Farm safe export not published at cutoff. Manager/Farm should return the already-requested safe existing-trace projection with the fields above, or explicitly report LOST/not captured. The manager can then assign the smallest repair justified by actual stage evidence. This report authorizes no new execution or probe.

