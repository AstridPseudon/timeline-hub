# F-D86 / V2/R3/G3 report

No source or test files changed. Worktree remains clean.

- **ID3 — source gap.** The authored exact choice is available through `native_word_anchor.binding`, but the validation seam currently falls through to `legacy_binding`, causing the ambiguous-anchor error after source move/reorder. Minimal correction: preserve `word_anchors[field]` through candidate/replay validation and invoke the authenticated exact binding. Leave untouched flat legacy declarations unchanged per D12/D12a; preserve all original rebase, timing, restart, and no-write assertions.

- **ID6 — stale test interface assertion.** `clip.anchor` is a registered production operation in `commands.operations()` and is used by the production execute path. The fresh-process test’s `assert "clip.anchor" not in operations()` is incorrect. Minimal correction is to assert registration/presence while retaining the pure canonical compile, no-history, JSON-only, result-identity, and exact timing guarantees. Do not remove the live operation.

- **ID8 — stale C0 status expectation.** At the claimed current base, `invalid_anchor` is C0 `invalid`, not `refused`. The faithful envelope is HTTP 422, outer `code: "validation_error"`, and `details` containing `status: "invalid"`, `reason/code: "invalid_anchor"`, validator path, hint, suggested command, exact base/current revisions, and `conflicts: []`; no receipt. Update only the old status assertion, preserving the half-open predicate, rational-FPS predicate, exact error/reason, unchanged head, atomicity, and undo assertions. No D83 change is justified.

- **ID9 — source gap.** Stale replay loses the authenticated exact choice and reaches `legacy_binding`, producing “legacy word anchor is missing” before the intended half-open-window check. Minimal correction: preserve the exact `word_anchors` binding through stale replay/validation, then retain the original outside-window refusal and all inputs, predicates, no-write, and retry behavior. D12/D12a prohibit treating an untouched legacy declaration as a new missing-binding failure. The handoff settles refusal semantics; the generic later-head error fallback must be aligned with that settled result.

D14 and D23 were checked; their deferred equal-text undo and child-word cases do not apply to these four IDs.

Checks performed without collection or function execution:

- AST parsing of affected source/test files: passed.
- Scoped Ruff: passed.
- Scoped mypy: passed.
- `git diff --check`: passed.
- Pytest, collection, services, browsers, and full suites: intentionally not run per brief.

Required commit message and empty `DONE` marker were created.