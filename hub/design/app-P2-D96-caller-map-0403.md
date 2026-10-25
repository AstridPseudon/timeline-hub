# D96 `seedThreeProducts` caller audit

Base: `043631dbabfed566cfe037709c7fe861d6435b52`  
Source: `tests/e2e/local/support/harness.ts:1192`  
Reviewed patch: `app-placement12145-setup-review-only.patch` (`6378b5b448b28584705cf82d7683f3c55110c86f747687276dbeea3dd89e4e4a`)

## Direct caller inventory

All 17 direct call sites found with `rg -n 'seedThreeProducts\\s*\\(' tests src scripts`:

| Path:line | Mode | Usage and relevant expectations | Old-12 extent dependency? |
|---|---|---|---|
| `scripts/testing/d66-plain-stack.mjs:749` | normal D66 service smoke | Seeds once, then uses only `headRevisionId` to locate the accepted seed receipt and checks Agent identity/history. No occurrence timing assertion. | No |
| `tests/e2e/local/auto-real-proxy.spec.ts:27` | normal default | Production managed image placement through Vite/proxy. Reads the seeded occurrence/shot/child and asserts one appended V2 image row `{at: 6, hold: 5}` plus exact unrelated-field preservation. This is an intended host-boundary consumer. | Yes, intended fix consumer |
| `tests/e2e/local/clip-delete-command.spec.ts:21` | `parent-delete` | Deletes the seeded parent app clip, then checks collection membership, exact closure, lost ACK/reload/retry, Agent disjoint edit, and inverse. Timing is not asserted; occurrence/child collections are checked relationally. | No |
| `tests/e2e/local/parent-split-command.spec.ts:17` | normal default | `seed3` is used only for a truthy transition id; the actual test creates an isolated `seedSplit` timeline with its own source/neighbor and independent `duration: 12` registry fixture at `:29`. | No; independent 12s source fixture |
| `tests/e2e/local/parent-trim-command.spec.ts:28` | normal default | Parent source-window trim of `f2-transition-clip`; asserts `{from: 0.5/0.75, to: 3}` and parent registry/opaque preservation. No occurrence extent use. | No |
| `tests/e2e/local/public-trim-mounted-fixture.spec.ts:15` | normal default | Mounted public parent trim of `f2-transition-clip`; asserts parent source window and zero legacy traffic. No occurrence extent use. | No |
| `tests/e2e/local/shot-name-command.spec.ts:45` | normal default + settings seed | Renames the seeded shot and saves raw settings; checks shot payload/provenance/opaque closure and retry/undo. No timing/end/plate assertion. | No |
| `tests/e2e/local/three-products.live-edit-smoke.spec.ts:21` | normal default | D79 live Agent label during a parent V1 drag, then guarded Undo. Reads only parent V1/clip and Agent label. No occurrence extent use. | No |
| `tests/e2e/local/three-products.mounted-readiness.spec.ts:97` | normal default | Seeds the mounted-readiness descriptor environment and persists setup diagnostics. No timing or snapshot value for the shared occurrence. | No |
| `tests/e2e/local/three-products.p2-elements-assets.spec.ts:46` | `native-none` | Production managed child image drop: pointer `4.5`, snap `9`, V2 siblings `[3,6)`/`[6,9)`, hold `5`; asserts accepted canonical delta, reload, and native guarded Undo. This is an intended host-boundary consumer. Independent params field uses user-entered `12` at `:880`/`:893`, unrelated to occurrence extent. | Yes, intended fix consumer |
| `tests/e2e/local/three-products.p2-popup.spec.ts:255` | `native-none` | Prepares popup by placing `f2-occurrence-copy` from the seeded source at `on: 12` (`:280`), then expects copied occurrence placement `{start_ms: 12000}` (`:605`) and same source shot/revision before ADD/SWAP/fork/Undo. The operation copies the source `duration_ms`; old geometry is source `[0,12)` followed by copy `[12,24)`. With the proposed seed it becomes source `[0,14)` and copy `[12,26)`, overlapping `[12,14)` on S1. | **Yes — blocking global setup change** |
| `tests/e2e/local/three-products.p2-tour.spec.ts:33` | `native-none` | Gesture tour edits parent V1 clips and transitions; its canonical-delta helper requires only intended parent clip fields and unchanged shot/internal closure. No occurrence extent use. | No |
| `tests/e2e/local/three-products.spec.ts:60` | normal default | Main P1/M1 cross-product suite. Includes the production child drop at `:1015`/`:1024` with pointer `4.5` → snap `9`, hold `5`, and exact closure/Undo; also duplicate-occurrence checks preserve `duration_ms` relationally (`:2585`), without asserting literal `12`. | Yes, intended fix consumer; duplicate is extent-independent |
| `tests/e2e/local/three-products.spec.ts:2844` | `native-none` | Separate transition-clear worker seed; only parent V1 transition commands and exact parent/closure preservation. No occurrence extent use. | No |
| `tests/e2e/local/track-label-command.spec.ts:53` | normal default | Parent V1 move then Unicode track rename with Agent disjoint edit, retry/reload/Undo; opaque child is checked only for preservation. No timing/end/plate assertion. | No |
| `tests/integration/runtimeRestore.test.ts:47` | normal default | Runtime restoreHistory integration; uses seeded timeline/shot identity and an intervening parent move, not occurrence duration. | No |
| `tests/integration/runtimeRestore.test.ts:122` | `referenceAt = 3` | Shot settings save/readback with an intervening parent move; `3` is the parent transition reference position, not the shared occurrence extent. No old-12 dependency. | No |

## Why the popup caller blocks

`native_occurrence_shared.py:312-325` deep-copies the source occurrence, including `duration_ms`, and only rewrites the new occurrence id and `placement.start_ms`; it does not normalize the copied duration or enforce non-overlap. Therefore `on: 12` is not merely a text fixture: it is an implicit old-end adjacency placement. The reviewed `12 -> 14` seed change changes the popup setup's same-lane geometry and can alter overlap/render/guard behavior. Per D96, this is a global-scope failure; do not apply the shared patch.

Requested follow-up: a placement-only host-window parameter with default `12` (or a dedicated popup fixture), authored and independently reviewed by the existing manager. This worker did not author a narrower patch.

## Independent 12-valued fixtures found during the audit

- Shared seed source media remains independently 12 seconds: `harness.ts:1227` passes `12` to the video import and the seed builder sets parent video registry duration `12` at the embedded Python source `:917`; the reviewed patch does not change either. The video is used only for the parent `[0,3)` clip.
- `tests/e2e/local/parent-split-command.spec.ts:29` uses a separate timeline registry duration `12`.
- `tests/e2e/local/three-products.p2-elements-assets.spec.ts:880,893` tests a clip parameter value `12`, not timing extent.
- Broader non-caller scan found independent fixtures in `tests/e2e/local/support/drop-file-geometry.test.ts:38` (plate end `12`) and `src/tools/travel-between-images/components/ShotTimelinePreview.integration.test.tsx:122,141` (plate hold `12`, occurrence `duration_ms: 12000`); neither calls `seedThreeProducts`.

## Static proof collected

- Current source SHA-256: `92f1261bc3213824f8323202e6a7f3d117892dda5ef6a847f0fd571a6cf81956`.
- Reviewed patch SHA-256: `6378b5b448b28584705cf82d7683f3c55110c86f747687276dbeea3dd89e4e4a`.
- `git apply --check --whitespace=error`: passed.
- `git apply --numstat`: `5 5 tests/e2e/local/support/harness.ts`.
- `git diff --check`: passed; worktree remained clean.
- Protected hashes matched the supplied verification artifact; no protected file was changed.
