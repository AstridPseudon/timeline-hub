# H30/D43/H3 incremental census limits

- Artifact: `agent-D32-current-node-reconciliation-H30-corrected.json`
- Artifact SHA-256: `c70b6627e6fe4cd7f6d900e0bcb99168dd8e56a4269ad8d88e12b07eec272268`
- Current qualified census: **267 total; 179 closed; 88 open**.
- Historical baseline preserved: **172 closed / 95 open** (136 baseline proof records, six current render-wire records, and 30 retained-caller records); all 267 original IDs, statuses, proofs, bodies, assertion mappings, and the exact 37-row delta mapping remain preserved.
- Prior artifact SHA-256: `990f231afced56377202ff9d7d3fa2705d075f30a09bdd96c58ce962c2fe047f` (172 closed / 95 open).
- Delta in this update: **+7 exact current H3 originals**, all in `test_character_swap_cpu_boundary.py`.
- Current H3 proof: 7 passed once on genuine child3b5c (Agent `ba8f0bc8`, Runtime `f3208b26`), independently PASS-reviewed 0517; relevant current HOME `9cd3dbe8` source bytes and target AST match the installed child, and the production caller reaches the installed guard.
- Historical `h3_import_0137` remains historical; it was not retroactively relabeled. The seven nodes retain that proof reference and add `h3_current_0508`.
- Source-copy 0502/0511: 2 exact selectors passed in 20.90s, but neither selector exists among the original 267 IDs. Scope note only; **zero census credit**, no alias or original matching.
- Three track-label rows, ABA-11466, IMAGE inverse, D40 installed-positive result, renderer timeout 0509, and Farm checkpoint remain open. No late D40 credit was available from an independent qualifying result review.
- No unrelated closed node was audited or relabeled. No full, browser, gate, body rerun, product/test edit, or v2 implementation was performed.

The delta mapping contains one row per credited exact original node: the prior 30 retained-caller rows plus the seven H3 rows. The source-copy selectors intentionally have no mapping rows.
