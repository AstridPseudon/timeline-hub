# D118a protected review facts

- Verdict: **FAIL_SOURCE**.
- Candidate commit/tree: `04eb2d2b947b421828ec744542d724c0aaed161e` / `533d4c22fb95c3537f5ecae002987e960f42d99b`.
- Agent base/tree: `0ad49261ed36f043b059c07de989bd39cd3a5889` / `aa413f6e1712626c0506284c8727057d753f692d`.
- Only candidate-changed file: `tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py`.
- Original/current file SHA-256: `52c63fa1a59d4ac08ca9077b97e6facfe7947cc36fde2795d1538df31a14cfed` / `e8f28d05d9a458958d1e7bbd537a662ddecba6161e147c22f4b4dac6ede834db`.
- Runtime receipt: `/home/user/work/wt/rt-pin-42aad0e9`, commit `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`, clean.

## Causal review

- Provider registration-before-bootstrap is causal and minimum: the original retained run failed at `service.py:2347` in `_seed_current_app_document` with `NotFoundError: parent composition revision not found`; the provider was registered only after bootstrap.
- The added `label`/per-command `steps`/`merge`/`reads`/`source`/`rationale`/`group_id` are not causal to the retained failures. A one-off diagnostic stripped them only from post-seed scalar calls and reproduced all three current failures at the same Runtime inverse-auth seams.
- Under C0 backward compatibility, omitted metadata is valid and `_commit_patch.normalize_steps` synthesizes one step. The candidate’s explicit per-command steps and `merge: 'fields'` are therefore non-neutral: they change grouping and merge selection from the original omitted wrapper’s synthesized grouping/default behavior. Public v2 caller success does not prove this ABI-1 wrapper must be converted.
- Minimum correction: retain only the provider registration move; remove the added metadata from the original `request(calls)` helper. The review did not self-fix it.

## Evidence

- Candidate exact-3 run: `3 failed in 66.73s`; scalar/compound fail at Runtime `timeline_commit_auth.py:1607` (`inverse stage source materialization is outside its physical turnover`), separate fails at `:1755` (`inverse stage native writes do not cover its authenticated effect image`).
- Metadata-stripped exact-3 diagnostic: `3 failed in 34.25s`, same two Runtime seams.
- Public v2 caller: `1 passed in 2.69s`.
- Ruff, mypy (`--follow-imports=skip`), py_compile, git diff --check: passed.
- AST conservation: seed helper exact; all original request fields/values exact; all 14 assertions exact.
- No functional GREEN claim: the retained nodes remain blocked by the Runtime inverse authorization defect outside this file.
