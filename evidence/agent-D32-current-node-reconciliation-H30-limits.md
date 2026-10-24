# H30/D43 incremental census limits

- Artifact: `agent-D32-current-node-reconciliation-H30-corrected.json`
- Artifact SHA-256: `990f231afced56377202ff9d7d3fa2705d075f30a09bdd96c58ce962c2fe047f`
- Census: **267 total; 172 closed; 95 open**.
- Delta: **+30 exact original closures**, all from the retained-caller mapping: 24 Sheet, 4 CLI, 2 Scene.
- Current proof head: Agent HOME `9cd3dbe865a941c052bda04ae0d61306d18f8f26` (tree `57f0231da0d7904ecd8778169973d6384e0ae141`), Runtime pin `8ea0766f5e9fb23cea26c7398770a8aaac06b258`.
- The 0500 result totals were 71 + 5 + 53; only the exact 30 mapped original IDs receive census credit.
- Three CLI track-label rows stay separate and open.
- ABA 11466 remains open after ambiguous-item undo failure. IMAGE 0441 remains open after the inverse failure.
- D40 candidate PASS is not integrated/custody-qualified. H3 current 0508 and support-timeout 0509 are pending.
- D44’s one-predicate PASS is outside the 267-node D32 census; it adds no census credit. Historical 0424 and Runtime16 remain separate and add no Agent-family credit.
- Scoped mypy/core-control passes are source/control evidence only and add no global node credit.
- Farm checkpoint remains pending; no full/P1–P5/browser/body run was performed for this reconciliation.

The mapping CSV provides one row per credited original node, with exact current node ID, phase, function name, source hash, function-body AST hash, and scenario mapping.
