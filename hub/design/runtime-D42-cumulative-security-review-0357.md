## FAIL — D42 cumulative security review

Candidate:

- SHA/tree: `a6843aa9322d354a8db2576a43dd202244608d65` / `29918b0ebedbd3ef86dacd1c9a33eb6db933e8f1`
- Base `36760ee0ad4b064a849edb3fc6e5a60a43fe8f48` / tree `11389911c2eec5acc901ab3b70e234fad9e1bc5d`
- Delta: runtime store plus three new memo test files; no worker edits.

Finding: closure-cell state is absent from the replay dependency fingerprint at [timeline_commit_store.py:58](/home/user/work/wt/rt-R-D42-cumulative-security-review-0357/runtime_protocol/timeline_commit_store.py:58). A warm accepted-history read continued to succeed after mutating state captured by a replacement `auth.validate_claims` closure. The old parent reproduced the original bypass; the candidate passed the helper-replacement test but failed this new closure attack. This violates the requirement that mutable validator dependencies cold-miss/reverify safely.

Required tests:

- 145 HTTP/authentication selectors: **145 passed** in 66.10s.
- Replay/input/dependency selectors: **184 passed**, 2 expected deprecation warnings, in 65.35s.
- Parent `validate_claims` attack: expected RED reproduced.
- Candidate closure attack: **accepted forged warm result — finding**.

Static/custody:

- Ruff: 11 inherited findings unchanged; all three new tests clean.
- Pyright: candidate/parent each 1,449 diagnostics; normalized additions/removals: 0.
- Artifact manifest and `git diff --check`: passed.
- Protected 64-file manifest: unchanged; SHA `a0211ffaa76476c668385c739e0862279817c0e20cae32d9c847214a53ca0923`.
- Runtime imported from this worktree; Agent source was archived from exact `415181d983d6d1d56a912da16ad4c5690e663187`, tree `f49cae445194350ed6def2aed65abbf4d870f639`.

No full/browser/gesture/benchmark suites run. No source or Git changes made. Completion marker and commit message were recorded. Recommended next step: fingerprint closure contents recursively or refuse memo reuse for closure-backed validators.