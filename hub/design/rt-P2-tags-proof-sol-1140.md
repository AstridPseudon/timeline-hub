Added 50 boundary tests covering all 44 tags and fixed only the two B010 helper assignments. Original tests and product guards remain unchanged.

Validation:

- New boundaries: **50 passed**.
- Required regressions: **135 + 68 + 4 passed**.
- Central socket test: **1 passed**.
- Normalized Ruff/Pyright: **zero new diagnostics**.
- Compile and `git diff --check`: passed.

**Acceptance remains blocked:** the reference-apply fault returns 503 on pre-tag `f0c4d6d2b`, while supplied base `4acfe0d20` already returns 409. Parent comparison found 48 diagnostic-visibility failures, this public-envelope mismatch, and one unchanged passing sink test.

[Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P2-tags-proof-sol-1140/evidence/validation-commands.txt)

Wrote `commit-msg` and `BLOCKED`; source is held for independent review. Recommend owner adjudication of the inherited apply catch. No merge/release. Original15203 remains **UNKNOWN**; fresh20990 `dependency_changed` remains distinct.