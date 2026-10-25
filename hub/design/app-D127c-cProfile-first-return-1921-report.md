## D127c first-return report

Implemented all five 1909 findings in the two permitted files:

- Exact mounted `RuntimeHandler` element-only selection; rejects mixed commands and retries.
- Safe private raw-pstats parent/file handling.
- Cleanup and prior-profile restoration on partial enable failure.
- Added required negative controls and exact edge-count/bounds tests.
- Corrected `pstats.Stats.stats` typing.

Evidence written under the assigned worker directory, including source manifest, predicate map, findings, validation, attach recipe, and safe schema.

Validation:

- Ruff: PASS.
- Python 3.11 compile: PASS.
- Helper-only Pyright: PASS.
- Mypy touched files: PASS.
- `git diff --check`: PASS.
- Informational local tests: `29 passed, 2 deselected`.
- Central targeted suite: queued/not run because free disk was `4,984,758,272` bytes, below the required 5 GB floor.
- No mounted body, full suite, or production qualification performed.

The supported D66 `p2-element --submit` recipe and helper hashes are documented. Independent cumulative review remains pending.