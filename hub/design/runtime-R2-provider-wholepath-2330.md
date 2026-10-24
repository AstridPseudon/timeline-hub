# R2r/P4 Whole-Path Investigation — FAIL

No product changes made. Worktree clean; commit message and `DONE` created.

Finding: `RequestCommitPort._ancestor()` authenticates via `TimelineCommitStore.history_entry()` at `runtime_protocol/timeline_commit_port.py:233`, then performs `reachable_document_input_pins()` at lines 237–240 before returning at line 241. A callback mutating `timeline_commit_history.metadata_json` during that pin read escaped the store’s final freshness check.

The real path is:

`Timeline.undo()` → `TimelineSession.undo()` → Runtime commit coordinator → Agent provider `commit()` → `RequestCommitPort.history_entry()` → store graph/replay authentication → pin-link read → returned history authority.

The exact witness reproduced the second failure:

- record-check mutation: refused
- post-auth pin-read mutation: returned stale history (`1 passed, 1 failed`)

Evidence: [provider-refusal.log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2-provider-wholepath-2330/evidence/provider-refusal.log), [provider-refusal.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2-provider-wholepath-2330/evidence/provider-refusal.xml).

Targeted comparator results:

- Graph-node authentication comparator: passed.
- Metadata mutation between provider lookups: passed.
- Public authenticated history reply comparator: passed.
- Private witness compile and Ruff lint: passed.
- `git diff --check`: passed.

The author’s authentic RELEASED732-vs-candidate finite evidence remains valid: N2/N4/N8 replies were equal; N8 checks reduced from 128→8 records and 256→16 closure reads. Source identity matches candidate `7627c8318`; store SHA-256 is `f67e5d76…2abb`.

Repair seam for Sol 2330: make history authentication and reachable-pin collection one store-owned freshness boundary, including `timeline_document_input_links`, and return the entry only after the final input recheck. A simple second `history_entry()` call after the pin read catches this witness but is a narrower, more expensive alternative and does not fully cover mutable pin-link rows.