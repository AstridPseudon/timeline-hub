# A2 placement native Undo: retained actual19078 cause

**Finding: the protected original leaves its embedded modal open, so its parent Undo role locator never resolves. No product repair is justified by this failure.** Product source and protected originals remain byte-exact at App `04beedcd18b8abb49502f65cd3facaafbe93db4e` (tree `300d186a45d3d0b96ef2ae39582f1e9b4a760e7d`). Read PLAN first and reviewed producer0753, independent fourpass0807, failedpath0810, and wire0815 reports. The earlier attribution to the initial placement response is superseded.

The retained service is `app-pin-04beedcd-d73-p2-04beedcd-submit-1025075440-19078`. The exact tuple is App `04beedcd`, Agent `070dfc5e`, Runtime `1daca2a3`, Composition `635f4de0`; full hashes are in the companion JSON. Overall service remains FAIL: four PASS, two FAIL, one ERROR, one NOTRUN. This finding grants no additional gate credit.

| Retained observation | Original | Retry1 |
| --- | --- | --- |
| Initial intended commit | One `occurrence.add-media`, HTTP 200 | One `occurrence.add-media`, HTTP 200 |
| Initial commit duration | 11381.015 ms | 11224.977 ms |
| Undo click call | `call@85` | `call@85` |
| Click start/end, monotonic ms | 101063.480 / 191082.958 | 244747.415 / 334770.930 |
| Click duration | 90019.478 ms | 90023.515 ms |
| Click log classification | Single role-locator wait; teardown closes target | Single role-locator wait; teardown closes target |
| Target-resolved / pointer-interception log | None / none | None / none |
| Undo input events / additional commit POSTs | Zero / zero | Zero / zero |

Both event streams reconstruct to the same DOM facts at `after@call@81`, `before@call@85`, and the response wait's `after@call@83`: one open dialog, one dialog Close button, and exactly one Undo button. That Undo is **enabled**, outside the dialog, and beneath a DIV with `aria-hidden="true"`. No Undo exists inside the dialog. The default role query excludes the hidden parent toolbar. The click remains unresolved until teardown closes its target. It never dispatches an event or reaches a disabled control, pointer interception, an interaction guard, capture, history targeting, or transport. Absence of the inverse is explained at this earlier boundary; no Runtime cause is inferred.

Snapshots contain incremental references. They were resolved in memory using Playwright's postorder indexing of literal element/text nodes, excluding reference nodes, with the referenced snapshot offset applied recursively. Each archive has one frame. ZIP CRCs and retained ZIP/event/network hashes match; event, network, and test JSONL parse through EOF. No raw snapshots, logs, messages, stacks, bodies, URLs, credentials, or private entity identifiers were exported.

The original's exact setup is `three-products.p2-elements-assets.spec.ts:1258–1263`: reload assertions call `openEmbeddedCanonicalShot`, check the occurrence-qualified placement row and absence of the raw row, then return while the modal remains open. Both retained test streams record the assertions at 1260 and 1261 completing without errors, followed by the Undo action at 1263 failing. `commitFromGesture:503–505` arms its response wait and awaits that click. The response wait (`call@83`) times out first; the still-pending click subsequently ends with `TargetClosedError` during teardown, 21.800 ms later in the original and 19.035 ms later in retry1. That page close is teardown evidence. The timeout does not imply failure of the already accepted initial placement.

`support/app.ts:261–268` opens the dialog and returns it without closing it. Production `AstridTimelineEditor.tsx:616–660` renders the embedded shot inside the normal Dialog; its open state clears on dismissal. The overlay wrapper uses Base UI's Dialog root and modal bridge; the installed root defaults to modal. The reconstructed `aria-hidden` ancestor is direct evidence of the actual modal state. `ShotTimelinePreview` renders no Undo control inside that modal.

The production route that would run after a valid parent Undo click remains intact: `TimelineEditorShellToolbar.tsx:45–70` calls `chrome.undo`; `useTimelineHistory.ts:325–335` checks settled remote history, pending uploads, interaction state, and editability; `useTimelineSave.ts:166–174` forwards to the current local handoff; `timelineLocalSaveHandoff.ts:179–202,645–685` derives targets from complete authenticated same-head ancestry and appends `timeline.inverse` with `select: null` and `args.publications`, no extra caller reads. `localSaveSession.ts:160–201` preserves that intent through the persisted outbox, builds full v2 label/steps/base/merge metadata, and transmits via the production provider wired at `useTimelineSave.ts:319–322`. `RuntimeDataProvider.commitTimeline:751–773` consumes the durable authoritative reply and rejects preview credit. This path is source inspection, not a claim that the blocked click executed it. The separate `undoTimeline` helper is not substituted for the toolbar's actual handoff route.

Same-tuple ADD19078 supplies the decisive setup comparison: `three-products.p2-popup.spec.ts:896` closes the embedded dialog before parent Undo at 898, with native inverse completion independently reviewed by fourpass0807. Parent19078 reloads the parent at `three-products.p2-tour.spec.ts:711`, clicks Undo at 716, and opens no embedded dialog in between. Prior asset27438 independently passed the parent registerAsset Undo on its separate `5337b439/6386c700/6634a17f/635f4de0` tuple; it supplies no placement or exact19078 product qualification. No passing trace was replayed or borrowed.

`review-only.patch` proposes exactly one line: close `reloadedDialog` after both existing placement-row assertions and before the parent Undo click. It mirrors ADD's normal dismissal and changes no existing assertion, locator, wait, fixture, body, authority guard, or production behavior. **Not applied.** Protected-original owner scope and review are required before applying it. Making the dialog nonmodal, forcing the hidden click, or adding a new child Undo is not supported by this evidence.

Verification performed:

- `git apply --check <worker>/notes/review-only.patch`: PASS, applicability only.
- `git diff --check`: PASS.
- `git diff --exit-code 04beedcd18b8abb49502f65cd3facaafbe93db4e -- tests/e2e/local src`: PASS, no differences.
- `git status --porcelain`: clean.
- Python in-memory ZIP/JSONL/XML/reference parsing and SHA-256 inspection: both placement traces verified, all four protected manifest hashes match before/after, ten inspected product files match HEAD. Exact hashes and finite findings are in `placement-Undo-cause.json`.
- C0 §§1–7 reviewed read-only against pinned contract SHA-256 `4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7`. Request/reply fields, guards, canonical authority, history and meta rules unchanged.
- Tests, mounted oldRED/newGREEN, tsc, ESLint, browser, service, backend, HTTP and full suite: **NOT RUN**, as required for a read-only finding. No independent Luna core-change review is needed because no core source changed.

Next step: obtain protected-original owner scope, review the one-line setup proposal, then run the authorized original placement case on the required pinned tuple. Outcome after dismissal, held-transport mounted evidence, authoritative inverse acceptance, restoration and history are unverified here. No product fix or newGREEN is claimed.
