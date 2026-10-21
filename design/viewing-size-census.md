# Viewing Timeline Core — current M4 size census

Captured 2026-10-21 at 02:18:11 UTC from committed Git blobs. This is one
source snapshot for the approved Viewing-owned boundary, not a final-all-repo
claim, deletion forecast, or size-limit gate. Physical lines use
`len(blob.splitlines())`; nonblank lines count lines whose `strip()` is
non-empty.

## Exact source tuple

The Main baselines are the current `origin/main` commits in each repository.
The current tuple is pinned to the commits below; local `tl/integration` and
`hub/tl/integration` matched at capture time. If a peer branch advances later,
these immutable commit pins remain the captured tuple and are not silently
relabelled as a newer all-repository state.

| repository | Main commit | Main tree | current commit | current tree |
| --- | --- | --- | --- | --- |
| Composition | `67b8aa3d0d6831d3e3504a340ff583c3da253707` | `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120` | `7bb54bbd64107e5090643ecca1e4d33164173e85` | `20467712e66dbadff4d562c0d5baae22b8c077a7` |
| Agent (Astrid/sdk) | `a411628f8fd6129f9c58c332019b56769d997384` | `e0ca791bb8adbf11e25e0e97843aaf246a04f965` | `4467c1c1a9ed81fa7cd1b2d7687b8ada54dc216a` | `5997f0162374dcfb56597b636caaad597c951b68` |
| App (Reigh) | `580508eed1bf6ed95caaf476c9d69a4672472a2f` | `ab3a5e296b01cc5458c88049c9eb5be402a05ccf` | `692765846fef511047445fecef3e55ec8bb6a5bf` | `e615c0a3aafca34504ba3544560de3887e4de38d` |

Runtime is outside this approved Viewing boundary and is not counted.

## Canonical authored source

Values are files / bytes / physical lines / nonblank lines. Delta is current
minus the exact Main baseline.

| approved owned slice | Main | current tuple | delta |
| --- | ---: | ---: | ---: |
| Composition `typescript/src/**`, excluding generated registries/curves and timer declaration | 16 / 45,621 / 1,550 / 1,398 | 79 / 195,770 / 4,525 / 4,174 | +63 / +150,149 / +2,975 / +2,776 |
| Agent `timeline_visualize/**`, excluding schemas, stage/docs, fonts, inspector assets | 54 / 1,253,951 / 27,700 / 24,911 | 56 / 1,304,901 / 28,775 / 25,924 | +2 / +50,950 / +1,075 / +1,013 |
| Agent explicit render/evaluator adapters and `rendering/elements/**` text | 29 / 375,489 / 11,381 / 10,993 | 20 / 363,724 / 11,068 / 10,701 | −9 / −11,765 / −313 / −292 |
| Agent `onscreen.py`, `scene_answers.py` | 1 / 18,156 / 452 / 375 | 2 / 25,278 / 598 / 503 | +1 / +7,122 / +146 / +128 |
| Agent Remotion host, excluding adjacent paths and generated/declaration/test files | 11 / 24,264 / 631 / 573 | 10 / 28,084 / 690 / 630 | −1 / +3,820 / +59 / +57 |
| App non-test source in `PreviewPanel/**`, `compositions/**`, `render/**`, excluding fallback | 29 / 282,934 / 7,533 / 6,932 | 30 / 307,481 / 7,945 / 7,335 | +1 / +24,547 / +412 / +403 |
| **Viewing-owned canonical total** | **140 / 2,000,415 / 49,247 / 45,182** | **197 / 2,225,238 / 53,601 / 49,267** | **+57 / +224,823 / +4,354 / +4,085** |

The arithmetic and complete per-snapshot path lists are in
[`viewing-size-census-manifest.json`](viewing-size-census-manifest.json). The
manifest records that each total is the sum of its six rows and that delta is
current minus Main.

## Historical prior census

The previous actual-current census is retained here as historical evidence; it
is not part of the current tuple above. It used Composition `4788e107…`, Agent
`57d6635…`, and App `813a851…` and measured **197 / 2,227,916 / 53,657 /
49,316** against the same Main baseline. The current update uses Composition
`7bb54bbd…`, Agent mirror `4467c1c…`, and App home mirror `6927658…`; no
speculative cut is credited for the difference.

## Boundary and reproduction

The approved read-only manifest/tooling was reused unchanged:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-size-census-gate-review-script.mjs`

It reads `git ls-tree` and `git show` only. The boundary includes authored
Composition `typescript/src/**`, Agent visualize plus the explicit
render/evaluator/elements/Remotion paths, and App non-test source under the
three named preview/composition/render roots. Generated data, tests/fixtures,
vendor copies, archives, fallback paths, stale `dist`, untouched
infrastructure, and Runtime remain excluded.

The captured current tuple can be replayed with:

```sh
sed \
  -e 's/46bd700b2b46ae1cab1e8a1502ed6504e81aa8d8/7bb54bbd64107e5090643ecca1e4d33164173e85/g' \
  -e 's/931d7ec56dadffc2efdc893fec80b4c4aadf8a8e/4467c1c1a9ed81fa7cd1b2d7687b8ada54dc216a/g' \
  -e 's/18becfbede00038830b97e63345445eeef54fa42/692765846fef511047445fecef3e55ec8bb6a5bf/g' \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-size-census-gate-review-script.mjs \
  | node
```

No tests, build, install, browser, renderer, graph copy, or unchanged-delivery
proof was run for this documentation-only census.
