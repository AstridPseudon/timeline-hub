## D118a report — PASS (b)

The four retained nodes are stale test expectations, not a live product misclassification.

- Nodes: image-at, image-hold, video-at, video-hold.
- Observed reason: `value_conflict`.
- Unchanged expected reason: `dependency_changed`.
- All four refused before acceptance; no persistence occurred.
- Source and tests were not changed. Target SHA-256 remains `3138f2ac…`; worktree is clean.
- Target test is absent from frozen R4 upstream.

The production path captures genuine field reads for anchor `at`, `at_ms`, `track`, `hold`, `from`, `to`, and `speed`, then writes one ordinary `clip.add-media` row. C0 §3 says field/item overlap is `value_conflict` (lines 604–612); `dependency_changed` applies to scope dependencies (lines 637–648). `_commit_patch.py:973` implements that distinction. The approved `cb35bd4fb` / `824e03f6a` change already confirms the same path for `track-label`.

Unapplied proposal: [proposal.patch](proposal.patch), changing only the expected reason to `value_conflict`. `git apply --check` passes.

Checks:

- Ruff: pass
- Mypy `--follow-imports=skip`: pass
- `py_compile`: pass
- `git diff --check`: pass
- Original four nodes were not rerun per D120.

Evidence: [facts.md](evidence/facts.md), [facts.json](evidence/facts.json). `DONE` and D118a commit message are present.