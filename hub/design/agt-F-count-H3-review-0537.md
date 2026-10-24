## FAIL — evidence package

- Count arithmetic: **PASS — 179 closed / 88 open of 267**.
- Qualified delta: **PASS — +7 exact H3 originals** (`h3_current_0508`), with historical `h3_import_0137` retained separately.
- Mapping: **PASS — 37 exact rows** (prior 30 unchanged + 7 H3).
- Baseline preservation: **PASS — all prior IDs/phases/body mappings preserved; only 7 H3 nodes changed**.
- Installed proof: **PASS — 7 passed; current `9cd…` and installed Agent `ba8…` relevant bytes/AST match; origins and receipt unchanged**.
- Scope exclusions: **PASS — source-copy tests absent from the 267 census and receive zero credit; D40, track labels, ABA, IMAGE, renderer, and Farm remain open**.
- `git diff --check`: **PASS**. No product/test changes in the candidate commit; no full/browser/body reruns performed.

Packaging defects causing FAIL:

1. `H30-limits.md` claims artifact SHA `c240…`; actual candidate SHA is `0168…`.
2. `known_scopes_and_limits` still contains stale 172/95-era claims, including that the seven H3 nodes remain open.

Commit message written and `DONE` marker created.