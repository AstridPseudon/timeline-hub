# Viewing current-main census

This is the copy-ready update for the existing Viewing census document. It
records a reproducible source snapshot; it is not a final M4 freeze.

## Exact source pins

The census uses `origin/main` as baseline and the recorded `tl/integration`
heads as current source:

| repository | `origin/main` commit | `origin/main` tree | current source commit | current source tree |
| --- | --- | --- | --- | --- |
| Composition | `67b8aa3d0d6831d3e3504a340ff583c3da253707` | `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120` | `e7ef7a0729a2d7dad3c0ae60da9e6bb8f844d332` | `408633d6b73dde63f683eaf9d13a132bb34a3bd7` |
| Agent | `a411628f8fd6129f9c58c332019b56769d997384` | `e0ca791bb8adbf11e25e0e97843aaf246a04f965` | `01ee5b95857265065ec2cae795c7394bd490cdff` | `c9a44b4b6f17cbf689ee6e3fddb49485697b5d03` |
| App | `580508eed1bf6ed95caaf476c9d69a4672472a2f` | `ab3a5e296b01cc5458c88049c9eb5be402a05ccf` | `a12b19be56816112da9b16cd8db4c48f9c5c399b` | `62df1de0a14edf326c6a635fbd52ed8f367fe0e3` |

Runtime is omitted because it is outside the approved Viewing boundary.

## Exact canonical counts

Columns are files / bytes / physical lines / nonblank lines. Delta is current
minus `origin/main`.

| owned slice | `origin/main` | current source | delta |
| --- | ---: | ---: | ---: |
| Composition `typescript/src/**`, excluding generated registries/curves and timer declaration | 16 / 45,621 / 1,550 / 1,398 | 79 / 190,569 / 4,442 / 4,097 | +63 / +144,948 / +2,892 / +2,699 |
| Agent `timeline_visualize/**`, excluding schemas, stage/docs, fonts, inspector assets | 54 / 1,253,951 / 27,700 / 24,911 | 55 / 1,292,945 / 28,508 / 25,670 | +1 / +38,994 / +808 / +759 |
| Agent explicit render/evaluator adapters and `rendering/elements/**` text | 29 / 375,489 / 11,381 / 10,993 | 20 / 363,724 / 11,068 / 10,701 | −9 / −11,765 / −313 / −292 |
| Agent `onscreen.py`, `scene_answers.py` | 1 / 18,156 / 452 / 375 | 2 / 24,162 / 568 / 470 | +1 / +6,006 / +116 / +95 |
| Agent Remotion host, excluding adjacent paths and generated/declaration/test files | 11 / 24,264 / 631 / 573 | 10 / 28,084 / 690 / 630 | −1 / +3,820 / +59 / +57 |
| App non-test source in `PreviewPanel/**`, `compositions/**`, `render/**`, excluding fallback | 29 / 282,934 / 7,533 / 6,932 | 30 / 307,481 / 7,945 / 7,335 | +1 / +24,547 / +412 / +403 |
| **Viewing-owned canonical total** | **140 / 2,000,415 / 49,247 / 45,182** | **196 / 2,206,965 / 53,221 / 48,903** | **+56 / +206,550 / +3,974 / +3,721** |

The `49,247` physical / `45,182` nonblank baseline is the exact recorded
`origin/main` result. The `53,221` physical / `48,903` nonblank current result
is a snapshot only and must not be treated as final M4 until the final-cut
source is known.

## Boundary notes

- The approved census script and path boundary were reused unchanged.
- Composition `e7ef…` adds no test or generated data to the authored
  `typescript/src/**` count beyond the existing manifest.
- App `a12…` has no `DebugTrack.tsx`, `renderPipeline.ts`, or new-rate wrapper
  path in the counted source. No debug/duration credit is inferred; those are
  absent or outside the approved manifest unless a future integration lands an
  owned product path.
- Agent `onscreen.py` and `motion/model.py` private duration/mouth helpers
  remain where the current source uses them; they are not counted as cuts only
  because a public successor exists.
- Tests, generated registries/contract data, vendor copies, archives, stale
  `dist`, fallback paths, and untouched main infrastructure remain excluded.

## Pending cuts, separate from current counts

- Q1: `typescript/src/lib/fade.ts`, six nonblank lines, still present and
  conditional.
- D09 core: `onscreen.py` whole-file candidate (375 nonblank), retaining or
  moving the 69-nonblank role/coverage seam only after the named
  caller/source/parity gates.
- D09a/D09b: `motion/model.py` `mouth_state` plus helper (24 nonblank direct,
  33 with `hash_unit`) and `mouth_box` (7 nonblank direct), conditional on
  public motion/ROI caller qualification. Private crop/statistics and
  presentation consumers remain KEEP.
- D08 App host replacement (`VisualClip`/`TimelineRenderer`) remains zero
  census credit until a complete public-host parity proof exists. The small
  audio helper is already landed outside this canonical slice and is not
  re-credited.
- Agent D10 source-adapter copies are complete: all nine copies were
  physically deleted in the current source, and that deletion is already
  reflected in the measured current counts. No forecast is included in the
  current total.

## Exact reproduction

```sh
sed \
  -e 's/46bd700b2b46ae1cab1e8a1502ed6504e81aa8d8/e7ef7a0729a2d7dad3c0ae60da9e6bb8f844d332/g' \
  -e 's/931d7ec56dadffc2efdc893fec80b4c4aadf8a8e/01ee5b95857265065ec2cae795c7394bd490cdff/g' \
  -e 's/18becfbede00038830b97e63345445eeef54fa42/a12b19be56816112da9b16cd8db4c48f9c5c399b/g' \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-size-census-gate-review-script.mjs \
  | node
```

No tests, build, browser, renderer, full suite, install, or dependency/cache
operation was run for this census.
