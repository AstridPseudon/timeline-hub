No blocking issues remain. C0c closes point 3 of the previous review at the contract level.

- **Unique addressing:** §2 requires exactly one reachable physical image at each evaluation boundary. Both `internal:<timeline_id>` and `shot:<shot_id>` reject multiple matches with `ambiguous_ref`. Explicit `internal-revision:<revision_id>` and `shot-revision:<revision_id>` forms are defined.
- **Bindings and overlap:** Authenticated records persist physical identity, revision, digest and evaluation boundary. Aliases normalize before overlap and dependency checks. Effects resolve against the verified before/after union, with separate bindings for revision turnover and intermediate inverse boundaries.
- **Replay and undo:** Successors require authenticated materialization and managed-edge provenance in the same ownership context. Unrelated replacements fail with `binding_changed`; surviving original images retain their identity. Undo uses persisted bindings rather than resolving historical aliases anew.
- **Fixture coverage:** The two-child scenario includes equal-payload children sharing `film-1`, a qualified edit that preserves the other child, ambiguous-alias rollback, partial-undo refusal, edit undo/redo and whole-batch undo/redo. Additional cases cover multiple shot revisions, newly ambiguous aliases and unrelated replacements with matching bytes.

This approves the addressing contract; the document explicitly leaves provider behavioral qualification to implementation work.

Review was read-only. No edits, builds, tests or network access.

VERDICT: APPROVE