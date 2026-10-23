# farm: F-zip-dry hit permission denials in 3 of 4 workers (not worked around)
Steps 1 and 2 (integration identity, squashed patch) passed for agent, runtime and composition. Denied: (a) `git checkout --detach <base>` inside the worker's fresh clone (agent, runtime); (b) `npm ci` in the fresh composition clone; (c) ruff / venv calls (runtime). Composition did not need (a) and applied cleanly. Stopped per D19/D22; no workaround. Reports: design/farm-zip-dry-{agent,runtime,composition}.md.

Results so far:
- agent: integration 8c355a48e (tree c4d72b065d6e); base 431681a6d is an ancestor; upstream tip 74f3f7edb is also an ancestor (U2b landed). Patch 8,548,648 B, 820 files (514 test-like, 306 product-like).
- runtime: integration cfa0af0d4 (tree 3675f446c); patch 4,632,068 B, 245 files (173 tests, 72 product). UPSTREAM DRIFT is bigger than the brief says: the live tip is f23d1e43f, not 6162e0e33; b70c323 is tests-only, f23d1e4 changes product code (runtime_protocol/visual_seam.py). Five files overlap: visual_seam.py, tests/lanes.py, tests/test_skip_guard.py, tests/test_visual_seam_admission.py, tests/test_canonical_render_admission.py. Likely conflicts, not confirmed.
- composition: 635f4de06fda (tree 5ab5191a2969); patch 493,374 B, 118 paths; fresh apply clean, the tree equals the integration tree; upstream main is still 67b8aa3d0 (no drift).
- app: still running.

Decisions owed: (1) permit `git checkout --detach` in a worker scratch clone and `npm ci` for Composition, or run the apply steps on the host; or accept the rehearsal as partial; (2) are runtime upstream f23d1e4 and b70c323 in scope for the freeze (the orchestrator's header lists only 6162e0e33)?
