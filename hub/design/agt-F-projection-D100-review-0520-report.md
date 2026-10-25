FAIL_SOURCE — F-D86 protected review.

Finding: `07f37c96fa1ce8b2f894d41c2d0347e5e27da626` permanently adds `repeated-third` via `occurrence.place-shared` (lines 296–340), reloads it, then removes only the first authoring shot (lines 348–402). The added occurrence remains in the canonical source graph, violating D100’s original-topology requirement. Existing goldens still require only `["shot-z", "shot-a"]` at lines 445 and 499.

The source-item admission itself is statically valid: registered Runtime route, ordered semantic birth + guarded `doc.patch`, exact `before: []`, declared reads, canonical reload, no fake history/foreign authority/SQL/manual CAS.

Checks:

- AST parse/in-memory compile: PASS; candidate and parent.
- Protected diff conservation: PASS; 61 additions, 0 deletions.
- Ruff candidate and parent: PASS.
- Mypy candidate: PASS.
- `git diff --check`: PASS.
- No pytest, collection, imports, helpers, or fixtures executed.

Dependency handback: candidate remains dependent on D100 `d3b5cfef76b4b3abef5db5f8288abc214a61354f`, which is not an ancestor of the review head; no behavioral proof was run against the old base.

No worktree files changed. `DONE` and commit message were created.