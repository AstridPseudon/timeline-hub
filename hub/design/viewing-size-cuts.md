# Viewing source-size audit (corrected)

The previous report was invalid: it counted `onscreen.py` in held Agent D2 even though that ref deletes it. This audit uses only exact Git trees (no fallback path or worker-ref adoption): Composition `2ac77f40d45d593e68ef281df50d2408d5a0f5a3`; Agent current `fc324e838fd668fc06cae906e8bcfccace86ad62` / held D2 `94e86ec1ffa7b8d600be434d42479adccf400aae`; App current `2bfde69eac32335eae0bc5fa2820940c0b3c694b` / held flat candidate `b231089267451ec1f64b77eabb66321dc7851ad3`.

Counts are reproducible nonblank physical lines from `git ls-tree` + `git cat-file --batch`; comments count, JSON/YAML count line-wise, and the product extensions are `.py`, `.ts`, `.tsx`, `.js`, `.mjs`, `.css`, `.json`, `.yaml`, `.yml`. Tests, fixtures, generated files, `dist`, locks, tarballs, vendor trees, Agent docs/fonts/inspector assets, and App test files are excluded. The visualize row additionally includes its package `schemas/action-index.json`; other schema metadata is excluded. Missing paths count zero.

| exact scope | current integration | held candidate |
|---|---:|---:|
| Composition `typescript/src` | **4,086** (80 files) | same source ref |
| Agent `astrid/packs/rendering` | **54,253** (151) | **54,579** (151) |
| Agent `timeline_visualize` | **25,350** (57) | **25,671** (57) |
| Agent `remotion/src` | **1,490** (14) | **1,514** (15) |
| Agent core evaluator | **375** (`onscreen.py`) | **116** (`scene_answers.py`) |
| App preview/player/render roots | **7,300** (32) | **7,503** (32) |

Exact correction evidence: `94e86ec1:astrid/core/timeline/onscreen.py` is absent and `scene_answers.py` is 116 lines; `fc324e83` has the inverse (375-line `onscreen.py`, no `scene_answers.py`). Both retain `tests/core/timeline/test_onscreen.py` and `_more.py`. Thus D09 is already present only on the held candidate; it is not another cut to count on current integration, and no test deletion is proposed. Keep `fast_lane`, `sweep`, and Agent `_timing_evaluators`; retain originals until their public equivalents are proven. The 0.0.8 package pins remain; pin adoption is not a size cut.

These rows are overlapping ownership inventories, not an additive consolidated total; the PLAN 20–26k target applies after canonical adoption and approved deletions. No feature cuts are inferred from the standalone area totals. Semantic/pixel/film/macOS qualification remains unrun.

