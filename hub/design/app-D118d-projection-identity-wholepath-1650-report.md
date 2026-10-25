# D118d report

Found the first failure: Agent’s `_item_ids` guard rejects one candidate item against an authenticated baseline containing zero items (`identity_conflict: shot item correspondence changed`). Runtime registration is reached, but acceptance, persistence, canonical reread, and duplication are not.

Identity ownership:

- Candidate item: unallocated request identity.
- Accepted physical ID: none; Runtime never accepted it.
- Alias: selects the physical shot revision, not an item.
- `source_mapping`: custody pins with an empty `item_id_map`, not an allocation ledger.
- Owner: Agent provider identity guard; no Runtime defect established.

Checks:

- AST parsing: PASS.
- Private-cache `compileall`: PASS.
- JSON/XML parsing: PASS.
- `git diff --check`: PASS.
- Worktree: clean.
- Retained own9: exit 1, 9 setup errors, first failure at `tests/sdk/test_timeline_capture_projection.py:311` → `_command_state.py:369`.

Evidence written:

- [facts.json](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118d-projection-identity-wholepath-1650/evidence/facts.json>)
- [predicate-map.json](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118d-projection-identity-wholepath-1650/evidence/predicate-map.json>)
- [verdict.md](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118d-projection-identity-wholepath-1650/evidence/verdict.md>)

No fixes or pytest reruns performed. Next step requires an authorized physical-item allocation/setup decision; do not relax the correspondence guard or normalize identities.