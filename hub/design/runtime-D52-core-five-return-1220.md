## Result: FAIL — diagnosis limits corrected

Read PLAN, the 1207 brief/report/evidence, review1214, contract, and D54/D56. No product or test files changed; worktree remains clean.

Original result retained: 3 PASS, 2 FAIL.

- PASS: captured config native-order
- PASS: nested config native-order
- PASS: retained fork source baseline
- FAIL: independent parent edit + preview redo
- FAIL: retained-sibling redo

Both failures reach Agent `_commit_patch._materialization_sites` and return `history_unavailable: inverse stage image differs from authenticated effects`.

### Corrected source diagnosis

The provider does not broadly “incorrectly require an after pin.” Earlier accepted custody exists:

- `_commit_patch.py:651-669` records `commit.materialization` at the authenticated input boundary.
- Publication-1 records custody from `shot-rev-1` / `internal-1` to the authoring shot/internal roots, with owners `f2-occurrence/shot` and `shared-sibling/shot`.
- Publication-2 is an independent parent `meta` patch.
- Publication-3 is an accepted inverse stage restoring the parent edge and old fork roots, but its stage records do not carry the earlier source custody across the inverse-stage boundary. The retained mismatch log records `new=shot-revision:shot-rev-1`, `side=after`, `pins=[]`.

The precise Agent seam is:

- `_commit_patch.py:950-1005`: inverse-stage validation requires exact before/after `commit.effect` pins, physical refs, revisions, digests, owners, effect ranges, step, and boundary.
- `_commit_patch.py:1044-1058`: `inverse_address_resolver` invokes that validation.
- `_commit_patch.py:1096-1110`: continuation follows only authenticated transitions.

The provider must continue authenticating publication/step/command source, current owner, revision, digest, exact effect/materialization ranges and order, sibling ownership, accepted history ancestry, ABA, and corruption guards. No validation or pin requirement should be removed.

The smallest Agent-owned seam is `_commit_patch._materialization_sites` / `inverse_address_resolver`; no Runtime attribution or competing source owner is supported.

### Limits and unknowns

The passing source-copy test only reconstructs and compares an in-memory closure (`test_occurrence_fork_source_baseline.py:99-104`). It does not qualify durable accepted-history redo with a retained sibling.

UNKNOWN: whether the eventual repair should propagate prior `commit.materialization` custody into the inverse stage or record an equivalent authenticated stage-side effect. No complete post-fix accepted redo record exists.

### Checks

Original qualification command produced `assigned.xml`: 5 tests, 3 passed, 2 failed, 0 errors/skips. No original body was rerun.

`git diff --check`: PASS.  
Ruff/mypy: N/A; no files changed.  
No full suite, gate, HTTP, browser, install, schema, or source-admission run.

Commit message was written to the requested path; `DONE` marker created.