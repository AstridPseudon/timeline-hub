## Report

- **Disposition:** D95 legacy-only for IDs 99 and 101; both originals remain unchanged.
- CURRENT `word_anchors` bind to an authenticated immutable transcript-document pin plus occurrence/clip and stable word IDs—not to `text_bindings` or MIME.
- The originals use legacy `elementRef.binding_id`. Native set/clear changes/removes the referenced row, so C0’s unchanged-source predicate rejects without writing.
- No faithful setup-only migration preserves the legacy reference, descriptor bytes/MIME, inverse assertions, and no-write purpose.

Checks passed:

- In-memory AST compile: 6 files.
- Scoped Ruff: passed.
- Scoped mypy: passed.
- `git diff --check`: passed.
- Worktree diff/status: clean.

No pytest, fixture/helper execution, services, probes, or full suites were run per source-only scope.

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D95-current-binding-return-0405/evidence/`

Recommended next step: ledger both originals as legacy-only, naming existing unbound inverse coverage and adding one targeted bound-invalidating refusal/no-write test if the gap is approved.