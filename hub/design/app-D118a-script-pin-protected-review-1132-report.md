# PASS — D118a protected independent review

- Reviewed `706e83559`; diff is exactly 12 insertions in `tests/sdk/test_timeline_script.py`.
- Original/current source hashes: `c2cab…c2fc5` / `72163…8193`.
- Exact node passed independently: `1 passed in 2.41s`.
- Runtime was immutable and receipt-backed: commit `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`, clean checkout `/home/user/work/wt/rt-pin-42aad0e9`.
- Ruff, mypy, py_compile, and `git diff --check` passed.
- All 7 original assertions and 49 original call ASTs remain conserved; authored media inputs and old text/head/revision/config assertions remain exact.
- The added patch uses the genuine Runtime-returned binding row through the registered v2 caller; it fabricates no binding, head, history, or media. The live rebind and pinned old-revision read remain proven.
- Separate unapplied product seam remains: `native_text_binding.py` strips Runtime-derived `binding_id`/`head`, while `timeline_script.py` correctly requires them. Owners: those two Agent files. The setup workaround does not claim this fixed.

Evidence: `evidence/facts.json`, `evidence/facts.md`, `evidence/node.xml`, `evidence/node.log`. No blockers.