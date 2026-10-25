## Report

Verdict: **PASS_SCOPE**

Verified retained 20990 evidence:

- XML: 1 passed, 0 failures, 37.091s; exit `0`.
- D112 SWAP/Undo: `200`/`200`.
- Fresh App-shaped fork+swap: fork generated; `409 dependency_changed`; no receipt; stderr empty.
- Original 15203 `history_unavailable` remains **UNKNOWN**, not reproduced or resolved.
- Runtime snapshot `b8b4001…`, tree `c45d9f…`; return delta contains only the two diagnostic files.
- One registry row exists; no product changes. Earlier 2867 tagging remains failed/unmerged.
- Fresh fixture uses Runtime API-generated state; no SQL/history patching, credential, or payload copying found.

Applicability limits: this is not the original App browser/outbox SWAP, not an original SWAP pass, not P2 GO, and not root resolution. Composition metadata has a commit/tree mismatch but was not exercised.

Tests/checks:

- Python AST syntax: PASS.
- Node syntax check: PASS.
- Evidence JSON validation: PASS.
- No additional full/targeted/native body run, per task scope.

Evidence: [20990-review.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P2-SWAP-native-result-review-1122/evidence/20990-review.json)

Next boundary: rerun the original App browser/outbox SWAP with retained realm/history/auth inputs and trace App → registered Agent → Runtime history/closure. Do not equate `dependency_changed` with the original `history_unavailable`.

Created `DONE` and `commit-msg`; the Runtime worktree remains clean.