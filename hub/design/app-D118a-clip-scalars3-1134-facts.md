# D118a evidence facts

- Agent base: `0ad49261ed36f043b059c07de989bd39cd3a5889`.
- Runtime receipt: `/home/user/work/wt/rt-pin-42aad0e9`, commit `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`, clean.
- Only changed file: `tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py`.
- The assigned test now registers the genuine provider before timeline bootstrap and sends the complete current v2 request envelope from its scalar request helper.
- Retained exact nodes were run with the pinned Runtime and genuine provider: `3 failed in 32.96s`. All three pass the original setup seam and reach Runtime inverse validation.
- Remaining owner/source seams: Runtime `runtime_protocol/timeline_commit_auth.py:1607`, `inverse stage source materialization is outside its physical turnover` for scalar/compound; Runtime `runtime_protocol/timeline_commit_auth.py:1755`, `inverse stage native writes do not cover its authenticated effect image` for separate.
- Public caller check passed: `tests/sdk/test_timeline_commit_provider_runtime.py::test_public_undo_redo_persists_v2_effect_bindings[False]`, `1 passed in 2.72s`.
- `ruff check`, `mypy --follow-imports=skip`, `PYTHONPYCACHEPREFIX=... python -m py_compile`, and `git diff --check` all passed.
- No Runtime or production change was made; a functional green result is blocked outside the assigned test file.
