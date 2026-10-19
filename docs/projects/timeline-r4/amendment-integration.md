# Release-3 extension restoration integrated

Latest authority: the user's explicit instruction to integrate [r4-release3-extension-kinds-restored.md](amendments/r4-release3-extension-kinds-restored.md), received after the original portfolio conversion. The supplied file is retained byte-for-byte. It overrides narrowed Release-3 scope and affected dependencies, preserving Releases 1/2 and all unrelated product criteria.

The supplied amendment's closing statement says the original ZIP already contains this version. Direct inspection establishes that the preserved original ZIP instead contains 92 cards and the narrowed J scope. Retain both sources honestly: original ZIP = 92 cards / 131.25d / 37 normal / 55 xhard; current amended packet = 95 cards / 137.25d / 38 normal / 57 xhard. R1 = 69 cards / 97d and R2 = 15 / 21d unchanged; R3 = 11 / 19.25d. J = five cards / 10d rather than two / 4d. Original identity/history remains in [archive manifest](historical/archive-manifest.json).

| Card | Change | Milestone / dependencies |
|---|---|---|
| EXT-ONE | retain 2.5d/xhard, operation mechanism + fit_to_beats; scope note now delegates remaining kinds to real first-consumer cards | J#ext-one unchanged |
| EXT-VIEW | add 2d/xhard, story_overview in CLI/show/visualize/App, read-only | J#ext-view ← J#ext-one, G#views, I#story |
| EXT-COMPONENT | add 2.5d/xhard, modifier contract first, vignette Player/export parity and bounds | J#ext-component ← J#ext-one, G#render-parity, I#motion-contract |
| EXT-CHECK-GEN | add 1.5d/normal, existing DAMAGED-ART and chiptune.compose as declarations | J#proofs ← J#ext-one, J#curves, G#checks |
| EXT-CURVES | retain 1.5d/normal; widen to declared music actions and command macros | now J#curves, existing card dependencies unchanged |

FULL-AUDIO-EXT now waits for J#curves and J#ext-component (rather than old J#proofs) and includes component/transition parity. FINAL-R3 waits for J#curves, J#ext-view, J#ext-component and new J#proofs, plus all its previous non-J prerequisites. Root/project indexes, milestone graph, figures, architecture §3, release contract and affected deeper scope notes were reconciled. The current final reviewer scope contains all 95 cards.

Review roles/stages/caps and consumed/held history remain unchanged. The new EXT-COMPONENT prerequisite that the orchestrator review the modifier contract is a specific consequential design decision, routed J manager → orchestrator → configured oracle before build; it is not an added independent reviewer stage/correction allowance. New card difficulty remains supplied xhard/xhard/normal; FINAL-R3 campaign worker remains normal while the existing final independent reviewer keeps its configured binding/rationale.

Affected proof: EXT-ONE recipe/scope; new view/component/check/generator checks and fresh-agent examples; widened curve/music/macro declarations; component/transition parity in FULL-AUDIO-EXT and IP8; full-capability examiner. Future execution records new source/input identities and invalidates only changed criteria/dependents. No executable product proof existed in this packet, so no product PASS is claimed or reset. Advisory presence stays excluded everywhere; REVIEW remains review-before-accept only. No implementation, product tests/services/worktrees, model review or extra oracle invocation occurred to integrate this explicit amendment.
