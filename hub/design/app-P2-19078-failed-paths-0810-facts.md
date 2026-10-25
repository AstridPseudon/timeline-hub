# P2 actual19078 failed-path handoff

## Result

The one authorized D66 full P2 service on the exact App/Agent/Runtime/Composition tuple terminated `FAIL` after 716 seconds. Readiness is separate and passed 1/1. The original eight-case arithmetic is **4 PASS, 2 FAIL, 1 ERROR, 1 NOTRUN**; the private early terminal note saying FAIL 3 is erroneous and was not modified. This is not an independent GO or service-pass verdict. The four passing cases remain owned by the sole independent pass review.

## Finite failed-path attribution

| Original | First missing seam | Observed outcome | Safe source boundary |
| --- | --- | --- | --- |
| SWAP | `tests/e2e/local/three-products.p2-popup.spec.ts:495`, accepted response expected 200 | Retained popup trace has a real POST with HTTP 409 and `history_unavailable`; no accepted receipt or Undo request | The mounted popup requests `occurrence.swap-media`. Runtime phase namespace `launch-a1e...` has provider/lock/handler raised at ordinals 114/117/119 and HTTP 409 at 120–121, but namespace-to-gesture correlation is UNKNOWN. |
| element apply | `tests/e2e/local/three-products.p2-elements-assets.spec.ts:1037`, `applied` status missing after 5s | Retained element trace has POST activity including incomplete `-1` entries; no completed commit response, receipt, reload, or Undo outcome | The intended A2 operation is an element `doc.patch` (the next source assertion is at line 1039), but the completed request body operation is UNOBSERVED. The pending phase records at `launch-c9f...` ordinals 106/109/110/117 are not assigned to this gesture. |
| automatic placement | `tests/e2e/local/three-products.p2-elements-assets.spec.ts:1263`, commit response wait | The placement trace archives retain POST activity; the response wait timed out at 90s. Later page-close is teardown evidence only | The gesture intends `occurrence.add-media`. The source path is mounted drop → task admission → persisted placement continuation → Agent selection/capture → A2 outbox → Runtime commit → canonical reload → `timeline.inverse`; no accepted receipt, server outcome, reload result, or inverse result is observed. Phase correlation is UNKNOWN. |

No Runtime cost is inferred from the wait, no absence of POST is inferred from the element timeout, and the older no-POST geometry result is not applied to this new tuple.

## Placement whole path

The static App path is present and finite: `editorImagePlacement.ts:30-145` prepares an occurrence-owned, read-closed placement and reserves the task; `placementRequester.ts:197-280` authorizes/admits or resumes the task, validates the selected output, captures the placement into the persisted continuation, and dispatches it; `commitOutbox.ts:374-505` persists the continuation and enforces the canonical commit route; `commitSession.ts:238-408` transmits through the operation and consumes the authoritative accepted closure; `dataProvider.ts:751-803` sends the v2 commit and builds native `timeline.inverse`; the original test checks canonical/history/reload and guarded Undo at `three-products.p2-elements-assets.spec.ts:1255-1276`. The actual19078 failure is at the response wait before those downstream predicates are proven.

## Runtime retained diagnostics

I searched the exact six phase files and six stderr files listed in `terminal-safe-facts.json`. The retained set contains completed HTTP 200 records, one raised/HTTP 409 record, and one incomplete pending request. The final listed stderr contains only the bounded catchall `runtime_protocol.errors.ProtocolError` with redacted frames `_lookup:215 → evaluate:168 → __enter__:141 → _read_transaction:310 → _store_version:265`. It is not safely attributable to SWAP, element, or placement; all three gesture correlations remain UNKNOWN.

## Bounded comparisons and verification

The current ADD, parent-move, transition-single, and transition-bulk PASS cases are credited only on exact tuple `04beedcd / 070dfc5e / 1daca2a3 / 635f4de0`. Prior `asset27438` is only the separate `registerAsset` PASS on tuple `5337b439 / 6386c700 / 6634a17f / 635f4de0`; it is not causal evidence for 19078. The requested R4 control path was searched and absent; no substitute was used.

Retained manifest/XML/trace inventory and hashes are in `19078-failed-paths.json`. Manifest JSON, both XML files, and all four trace archives parsed/tested in place. Protected source hashes match the retained manifest; the App worktree is the exact requested base, `git diff --check` passed, and the worktree is clean. No tests, browser, TypeScript, lint, backend, full suite, Runtime repair, guard waiver, or product files were run/changed.
