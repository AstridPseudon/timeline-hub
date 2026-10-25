# D118a Protected Review — FAIL_SOURCE

Candidate commit `04eb2d2b947b421828ec744542d724c0aaed161e`; only the allowed test file changed.

Verdict:

- Provider registration before bootstrap is causally required and correct.
- Added v2 metadata is not required: stripping it reproduced identical inverse failures.
- It is non-neutral under C0: explicit per-command steps and `merge: fields` alter the original ABI-1 wrapper’s synthesized grouping/default behavior.

Minimum correction: retain provider registration relocation; remove the added metadata from `request(calls)`. No review self-fix applied.

Evidence:

- Pinned Runtime: `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`, clean.
- Exact retained nodes: 3 failed. Scalar/compound fail at Runtime `timeline_commit_auth.py:1607`; separate at `:1755`.
- Metadata-stripped diagnostic: same 3 failures and seams.
- Public caller: `1 passed in 2.69s`.
- Ruff, mypy, py_compile, `git diff --check`, and AST conservation: passed.
- Original RED was bootstrap-time `NotFoundError` at test line 171; provider relocation removes that RED.
- No functional GREEN claim: remaining inverse failures are outside this file in Runtime.