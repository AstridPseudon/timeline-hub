# Viewing M4 size/cut plan

Status: design-only handoff; no product or test changes.  This uses the frozen
08:00 Core boundary and the corrected 09:05 census, not a quota-driven
redefinition of the boundary.

## Accounting boundary

The authoritative confirmed Viewing slice is **140 -> 205 files,
45,182 -> 48,343 nonblank UTF-8 lines**.  It is reproduced by
`handoff-vw-m4-size-census-gate-review-script.mjs` from committed blobs at the
three frozen current SHAs in `handoff-vw-m4-current-core-census-freeze.json`.
The rows are disjoint:

| current row | files / nonblank lines | treatment |
| --- | ---: | --- |
| Composition authored `typescript/src/**` | 79 / 4,097 | one public evaluator/source; generated registries, curves and timer declaration excluded |
| Agent `timeline_visualize/**` authored subset | 55 / 25,256 | keep Read/See, pixel lane, statistics and timing behavior |
| Agent explicit render/evaluator adapters + elements | 29 / 10,744 | keep render/export, loaders, capabilities and diagnostics; D09 is a source-qualified replacement, not a blind file cut |
| Agent `onscreen.py` + `scene_answers.py` | 2 / 469 | private evaluator plus inactive/public transport; D09 held |
| Agent Remotion host (adjacent execution files removed) | 10 / 613 | keep host/runtime seam; adjacent live-scene/execution bucket is separate |
| App PreviewPanel/compositions/render active source | 30 / 7,164 | keep playback, themes, unknown placeholders and audio behavior; D08 remains partial |
| **confirmed total** | **205 / 48,343** | baseline is 140 / 45,182 |

Explicitly outside this number: Runtime generic worker/custody/auth/CAS/
platform/lifecycle infrastructure and generated clients/contracts/DTOs;
Agent visualize schemas, stage/docs/fonts/inspector assets and generated
Remotion/declaration/test files; App tests, generated/fallback modules, vendor
trees and package archives; Composition generated source; and Agent's three
unchanged `remotion/src` adjacent files (818 nonblank lines).  The App census
also has unresolved omitted domain files (for example `runtime/composition/
graphProjector.ts`, `patchPreview.ts`, `materialRuntime.ts` and
`data-kinds/`); they are not silently excluded from a global total.  Generic
classification is source-based: Runtime's `runtime_protocol/local_*`,
`remote_worker_*`, `verified_host_launch.py`, `astrid_runtime/` and generic
auth/backup/CAS/platform code are outside Read/See/Edit; App's seven reviewed
layout/recovery shell files are an adjacent bucket, not deletions.

Observed live `tl/integration` heads before estimating: Composition
`e80c46b`, Agent `efb9603`, App `18becfb`, Runtime `642eef7`.  Composition's
tree is the frozen census tree; App matches the frozen census tree; Agent has
only later committed source changes (+186 nonblank lines in the selected Agent
row, chiefly `composed_frame.py`, `filmstrip_cards.py` and
`filmstrip_execution.py`).  The frozen 48,343 number remains the accounting
base. Frozen R4 references were read as parts-bin evidence only: Composition
public `scene-evaluation.ts`, Agent's warm-owner `scene_answers.py`, App's
vendored evaluator/package tree, and Runtime's `visual_seam.py`; none is a
permission to transplant an old branch.

## Vendored copies: raw versus deduplicated

Independent blob comparison on current App `18becfb` against Agent `efb9603`
found that all vendor roots are disjoint from the confirmed active manifest.
Thus active authored copies were already excluded; deleting them cannot be
subtracted from 48,343 a second time.

| remaining vendor bucket | raw instances | deduplicated / exact evidence | future canonical reduction |
| --- | ---: | ---: | ---: |
| App `vendor/astrid-browser` + `vendor/astrid-build-inputs/primary/astrid` text | **169 / 35,024 NB / 1,319,619 B** | 153 unique blob contents / 31,346 NB; 123 exact Agent-snapshot files / 21,122 NB / 882,979 B; 15 exact selected canonical Agent files / 933 NB / 24,931 B | **0** (already outside census); delete only after owner proves which 123 are replaced. The 46 non-exact/unmatched files (13,902 NB) are unresolved, not imagined duplicates. |
| App vendored Composition `vendor/timeline-composition/typescript/src/**` | **21 / 1,504 NB / 51,742 B** | source copy is outside the active manifest; package metadata/tests/generated files are separate | **0** to confirmed core; package adoption may remove the vendor tree |
| Agent old Composition reference `docs/reference/timeline-composition-v0.0.6/**` | **21 / 1,612 NB / 57,156 B** | archived reference, not active source | **0** to confirmed core; delete only as an archive cleanup |
| App static/theme copies (`vendor/banodoco-animations`, `-effects`, `-transitions`, `timeline-theme-2rp`) | **64 / 1,091 NB / 42,575 B** | package inputs, not active manifest rows; package/alias ownership is unresolved | **0** until the immutable package/official pin gate proves replacement |

The committed App package still points at Composition **0.0.8** and local
theme/ops/schema packages; Agent carries the newer immutable **0.0.12**
artifact.  The replacement is the exact 0.0.12 package
(`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 77
members), with matching App/Agent/Runtime pins and no private vendor import.
The App 0.0.8 archive (50,664 B) and Agent 0.0.12 archive (58,444 B) are
binary/package debt, not authored lines.  Untracked local links for
`timeline-ops`, `timeline-schema` and `timeline-theme-2rp` are not committed
source and are not counted.

## Cuts and expected arithmetic

All figures below are nonblank lines unless marked otherwise.  “Net” includes
replacement source; a deletion-only ceiling is not a parity result.

| unit | current evidence and replacement | qualified reduction / expected net | blockers and proof required |
| --- | --- | ---: | --- |
| Composition `typescript/src/lib/fade.ts` | 7 physical / **6 NB**; inline the identical `fadeMultiplier` call already used by `VisualClip` | **-6 NB**, giving **48,337** confirmed Viewing lines if landed | Q1 replacement is exact. Preserve `VisualClip`; run `typescript/tests/transition-policy.test.ts` and `typescript/tests/registries.test.ts` after `npm run build:test`. |
| D08 App duplicate evaluator math | Historical `playerEvaluation.ts` is already absent from current App; do not count it. Remaining `TimelineRenderer`/`VisualClip` are mixed live consumers. `audioFade.ts` is 66 physical / **60 NB** outside this Viewing manifest. Replacement is Composition public evaluation and `audio-envelope.ts`/`applyAudioEnvelope` for audio. | **0 now**; conditional `-60 NB` is not a forecast until both preview/export PCM consumers pass | Actual frame+audio parity, public12 package/root/vendor adoption, source-selected revision/initial-read proof, and zero legacy visual/audio evaluator traffic. Keep playback fades, transitions, audio gains, diagnostics and unknown internals. |
| D09 private Agent evaluator | Current `onscreen.py` is **452 physical / 375 NB**; `scene_answers.py` is already 114 physical / 94 NB and is not a free deletion. Replacement is public Composition scene rows through the existing prepared Root/source boundary. | Deletion-only ceiling **-375 NB**; replacement net is **unmeasured**, so expected net is **0 until qualified** (the held old proposal deleted 452 physical lines on a different tree and is not current evidence) | Trusted post-resolve/historical source, exact materialized assets/theme/occurrence identity, real custom-loader/capability positives, advisory UNKNOWN/findings, renderer-free save behavior, and paired pixel/audio parity. Named neighbors: `test_scene_answers.py`, `test_scene_host.py`, `test_scene_caller_preservation.py`, `test_coverage_empty_cut.py`, label/fast-lane tests. |
| VW-D09a/b presenter mouth helpers | Current `motion/model.py`: `mouth_state` **24 NB**, `mouth_box` **7 NB**. Replacement is registered presenter `motionAt`/scene diagnostics from the same drawing geometry. | Deletion-only ceiling **-31 NB**; **0 net until caller/aggregate proof** | Exact selected-cut counts, ordinary registered render positive and planted mismatch, default/partial/raw-invalid known behavior, same source/theme/assets. Preserve private statistics/crop inputs while parity is open. |
| VW-D09c pixel crop/verification | Private crop selection remains coupled to `fast_lane.py`; pixel verification, statistics, strict 2% denominator and selected-key behavior are required evidence, not duplicate evaluator math. | **0** | Public source-qualified mouth ROI plus exact selected-cut aggregate; no threshold/denominator rewrite. |
| D10 vendored Composition/Agent/static copies | Counts are in the vendor table and already excluded from 48,343. Replacement is immutable public package plus official pins and alias isolation. | **0 canonical NB** (repository deletion may remove raw vendor lines later) | App/Agent matched package adoption, all public exports/registry/theme behavior, no private vendor imports, then actual frame/audio parity. |
| D12 stale `dist`/masked build | Current Composition has no tracked `dist`; ledger says stale dist/build masking is already deleted. | **0** | Standard build/package smoke remains the proof; do not recount. |

Honest current forecast: the only presently qualified authored-line reduction is
Q1, so the confirmed Viewing slice is **48,337 NB**, not 20–26k.  This is
**22,337 above the upper 26k target (28,337 above 20k)** before any Runtime or
Agent editing/App core outside this Viewing slice is included.  Runtime is a
separate census (23,501 physical lines at its frozen ref; 22,178 NB in the
live-head read), so it must not be arithmetically mixed into this nonblank
Viewing total.  The true four-repo core is higher because those Runtime,
App-editing and Agent-editing paths are not in this Viewing manifest.  Closing
that gap requires owner decisions about held evaluator/source joins and broader
product paths; it does not authorize cutting kept behavior or pretending
vendor/archive deletions are core savings.

## Non-negotiable preservation gates

Keep `fast_lane`/`sweep` pixel verification and statistics, `_timing_evaluators`,
custom loaders, registered capabilities, loud unknown-element diagnostics,
advisory UNKNOWN/findings, playback features (music beds, fades and
transitions), and owner-film/legacy intended-DIP coverage.  A replacement is
trusted only when it uses the same prepared source, registry, theme, occurrence
and revision identity; metadata that merely looks like a revision is not
authority.  No save-path renderer dependency, second projector, new manifest
framework, feature deletion, or test weakening is part of this plan.
