# Viewing Timeline Core census — reviewed 2026-10-20

This is the ORCH review of `tl/vw-m4-core-size-census` against the 08:00Z
boundary: authored product code implementing timeline Read/See/Edit. It is a
size census, not a target-achievement claim. Counts are committed Git blob
bytes and nonblank physical UTF-8 lines; delta is current snapshot minus the
`origin/main` baseline.

## Verdict

The candidate arithmetic is reproducible, but its `tl/integration` labels are
wrong for Agent and App. The pinned candidate SHAs are Agent `f7584fad` (08:05)
and App `1be0efdd` (06:59), while the observed live integration heads are Agent
`0e951d689`, App `75df44e99`, and Composition `024f69501`. Composition
`5e06f401` is also a historical integration snapshot. This report therefore
names the exact pinned snapshots and does not call them current.

The candidate’s broad total is exact for its broad path manifest:

| snapshot | files | bytes | nonblank lines |
| --- | ---: | ---: | ---: |
| `origin/main` | 143 | 2,036,935 | 46,000 |
| pinned candidate snapshots | 208 | 2,208,967 | 49,161 |
| delta | +65 | +172,032 | +3,161 |

Three unchanged Remotion files are not confirmed Timeline Core under the
08:00 definition: the frame worker is execution infrastructure, and the two
`LiveScene`/Three.js files are the adjacent live-scene path. They are listed,
not hidden, as an unresolved/adjacent bucket:

| excluded adjacent path | baseline/current bytes | baseline/current lines | reason |
| --- | ---: | ---: | --- |
| `remotion/src/astrid-frame-worker.mjs` | 18,569 / 18,569 | 365 / 365 | renderer execution worker |
| `remotion/src/LiveSceneClip.tsx` | 1,114 / 1,114 | 16 / 16 | live-scene adapter |
| `remotion/src/ThreeTimelineComposition.tsx` | 16,837 / 16,837 | 437 / 437 | live-scene/Three.js composition |
| **adjacent subtotal** | **36,520 / 36,520** | **818 / 818** | **not in confirmed core** |

Thus the corrected confirmed-core reading is:

| snapshot | files | bytes | nonblank lines |
| --- | ---: | ---: | ---: |
| `origin/main` | 140 | 2,000,415 | 45,182 |
| pinned candidate snapshots | 205 | 2,172,447 | 48,343 |
| delta | +65 | +172,032 | +3,161 |

If the orchestrator later decides that the Three.js/live-scene path belongs
to this core, add the adjacent subtotal back explicitly; do not silently mix
the two readings. No target achievement is claimed.

## Confirmed canonical boundary and counts

The flat reproducer is
[`handoff-vw-m4-size-census-gate-review-script.mjs`](./handoff-vw-m4-size-census-gate-review-script.mjs).
It is independent of the candidate repository helper and reads only the pinned
committed blobs from the three absolute repo paths. Run:

```sh
node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-size-census-gate-review-script.mjs > /tmp/viewing-size-census-reviewed.json
```

The canonical rows below are per repository/path boundary. The JSON output
contains the exact flat path manifest for every row.

| repo/path boundary | baseline files / bytes / lines | pinned current files / bytes / lines | delta files / bytes / lines |
| --- | ---: | ---: | ---: |
| Composition `typescript/src/**`, excluding generated registries/curves and `remotion-timer-compat.d.ts` | 16 / 45,621 / 1,398 | 79 / 190,523 / 4,097 | +63 / +144,902 / +2,699 |
| Agent `astrid/packs/rendering/actions/timeline_visualize/**`, excluding schemas, stage/docs, fonts, inspector assets | 54 / 1,253,951 / 24,911 | 55 / 1,270,190 / 25,256 | +1 / +16,239 / +345 |
| Agent explicit rendering/evaluator adapters and `rendering/elements/**` text source | 29 / 375,489 / 10,993 | 29 / 366,756 / 10,744 | 0 / −8,733 / −249 |
| Agent `astrid/core/timeline/onscreen.py`, `scene_answers.py` | 1 / 18,156 / 375 | 2 / 24,116 / 469 | +1 / +5,960 / +94 |
| Agent Remotion host source, excluding the three adjacent paths above and generated/declaration/test files | 11 / 42,215 / 573 | 10 / 27,058 / 613 | −1 / −15,157 / +40 |
| App non-test source in `src/tools/video-editor/components/PreviewPanel/**`, `compositions/**`, `render/**`, excluding fallback | 29 / 282,934 / 6,932 | 30 / 293,804 / 7,164 | +1 / +10,870 / +232 |
| **confirmed canonical total** | **140 / 2,000,415 / 45,182** | **205 / 2,172,447 / 48,343** | **+65 / +172,032 / +3,161** |

The baseline/current rows are all exact blob measurements. In particular, the
Composition source includes authored built-in components/defaults/metadata, and
the Agent element rows include authored `component` and `element.yaml` files;
those are not generated contracts.

## Exclusions and duplicate accounting

Generated, tests, documentation, archives, and generic infrastructure are not
in the canonical total:

| excluded category | baseline → current files / bytes / lines |
| --- | ---: |
| Composition generated registries/curves/timer declaration | 4 → 7 / 5,228 → 12,628 / 88 → 405 |
| Agent visualize schemas | 10 → 10 / 70,613 → 70,613 / 1,925 → 1,925 |
| Agent Remotion generated/declaration/test source | 5 → 4 / 14,636 → 14,228 / 419 → 408 |
| App fallback registries/theme shims | 4 → 0 / 4,785 → 0 / 229 → 0 |
| Agent old Composition reference `docs/reference/timeline-composition-v0.0.6/**` | 21 → 21 / 57,156 → 57,156 / 1,612 → 1,612 |

App vendored sources are not folded into App active source or Composition:

| vendored source (excluded) | baseline → current files / bytes / lines | duplicate finding at pinned current |
| --- | ---: | --- |
| App `vendor/timeline-composition/typescript/src/**` text | 21 → 21 / 51,742 → 51,742 / 1,504 → 1,504 | old Composition copy; not canonical |
| App vendored Agent/browser text under those roots’ Agent `astrid/**` and `remotion/src/**` trees | 169 → 169 / 1,319,619 → 1,319,619 / 35,024 → 35,024 | 123 files / 882,979 bytes / 21,122 lines have exact Agent-snapshot blob matches |
| of that vendored Agent source matching selected canonical Agent paths | — | 15 files / 24,931 bytes / 933 lines; excluded, so no App/Agent double count |

The Agent old Composition reference is also excluded. At the baseline it has
12 exact blob matches to Composition source (30,421 bytes); it is documentation
reference material, not a second canonical evaluator. Current Composition
changed, so it has no exact current-blob matches. Package archives are excluded:
Agent `remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz` is 58,008
bytes and App `vendor/artifacts/banodoco-timeline-composition-0.0.8.tgz` is
50,664 bytes at the pinned current snapshots.

The candidate’s App Composition duplicate row was therefore correct but
incomplete: App’s vendored Agent/browser trees also need explicit accounting.
Neither vendor tree was added to the canonical total, so the confirmed total
does not double count them.

## Boundary decisions and unresolved items

- Included: Composition evaluator/defaults, authored Agent visualize/read views,
  evaluator/render adapters and element seam, the Agent Remotion host pieces
  needed by the normal timeline viewer, and App preview/player/render source.
- Excluded exactly: generated registries/curves/schemas/declarations, tests,
  docs/reference material, package archives, App fallback generated shims,
  Agent’s execution worker, and the two live-scene/Three.js files above.
- Unresolved: whether the orchestrator wants the Three.js/live-scene path in
  the final Viewing slice. Its exact 818-line subtotal is isolated so either
  policy is auditable. No other path was discounted speculatively.
- Runtime is intentionally absent: its commit/inspection and visual seam code
  belong to the Runtime-owned census, per the area ownership split.
- The shared dependency graph was not inspected or modified; no environment
  qualification, browser, socket, renderer, install, or full-suite run was
  performed.

## M4-scoped deletion opportunities

These are only existing, already-tracked M4 rows; they are not new cleanup:

- D08: retire App duplicate visual math only after the existing frame/audio
  parity behavior tests pass; do not subtract it from this census beforehand.
- D09: retire Agent private evaluator/visibility math only after the existing
  positive/pixel coverage and caller migration evidence; do not subtract it
  from this census beforehand.
- D10: remove App/Agent vendored Composition copies only after coordinated
  package adoption and its existing behavior tests; no vendor bytes are
  counted as canonical today.

No target-achievement claim is made.
