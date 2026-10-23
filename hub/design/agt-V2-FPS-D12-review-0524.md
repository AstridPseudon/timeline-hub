# PASS — V2 READONLY FPS/D12 review

Date: 2026-10-23 UTC  
Worker: `agt-V2-FPS-D12-review-0524`  
Reviewed commit: `e50beb3063df13b5faa86896eb5161ba1df8cb54`  
Parent: `9cf0fde2f57603813d81733ee8b0f7117ffd634c`

## Ruling

**PASS for the assigned FPS/D12 scope.** The commit changes only:

- `astrid/sdk/timeline/validation.py`
- new `tests/editing_conformance/test_commit_fps_d12.py`

No source edits were made by this review; the worktree is clean relative to HEAD.

## Review findings

- Existing `_number`, `_fps`, `_time_fraction` behavior and exact Fraction distinctions are unchanged. No epsilon, float-round-trip, denominator approximation, new parser, authored-byte rewrite, or speculative equivalence policy is present.
- `_validate_fps` validates candidate FPS values first. A mixed-rate candidate is exempted only when `_fps_basis(candidate) == _fps_basis(baseline)`; that basis retains the exact authored parent/canvas/child declarations, base-parent identity, source shot/revision/internal identities, and occurrence-to-authoring-shot ownership. Thus unrelated edits can preserve an existing legacy mismatch, while declaration changes, removals that leave a mismatch, moved/replaced owners, invalid/nonfinite values, and distinct new rates remain refused.
- The exemption is narrow: later structure, reference, parameter/schema, and timing validation still runs. The focused test explicitly checks that legacy FPS retention does not waive those guards.
- The production caller remains wired at `astrid/sdk/timeline/commit.py:1117-1125`: `validate_final_candidate(..., baseline=...)` runs before document preparation and port accept/preview. The focused production test covers accepted and preview paths with v2 controls and atomic refusal of a modified mismatch.
- Request/reply/idempotency fields are outside this two-file delta and are not dropped or changed here. No generated/schema/pin/executor/HTTP-body changes were found.
- The new test file contains no skip/xfail weakening.

## Commands and results

Environment used for imports:

```
PYTHONDONTWRITEBYTECODE=1
PYTHONPATH=.:/home/user/work/runtime
/home/user/work/venv-agent/bin/python
```

Targeted required suite:

```
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_commit_fps_d12.py \
  tests/editing_conformance/test_commit_v2_validation.py \
  tests/editing_conformance/test_commit_timing_validation.py
```

**PASS: 79 passed in 2.64s.**

Additional author-recorded focused controls on this exact tree: **177 validation/timing/FPS passed** and **242 provider/facade passed**. I independently reran the provider command:

```
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/editing_conformance/test_doc_patch_v2.py \
  tests/sdk/test_timeline_commit_provider.py \
  tests/sdk/test_p4_commit_v2.py \
  tests/sdk/test_timeline_open_commit_v2.py
```

Initial result: **241 passed, 1 failed** because the nested renderer-isolation subprocess lacked `ASTRID_RUNTIME_CHECKOUT`. With the required read-only Runtime checkout variable:

```
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_commit_provider.py::test_move_reload_and_inverse_import_no_renderer
```

**PASS: 1 passed in 1.56s.** This resolves the lone environment-only failure; no product failure was observed.

Quality/integrity:

- Scoped Ruff: **PASS**, all checks passed.
- Normal `make ruff PY=/home/user/work/venv-agent/bin/python`: **PASS**, current=2149 baseline=2149.
- Scoped mypy with available `/home/user/work/venv-agent/bin/python`: **PASS**, no issues in 1 source file.
- Requested private `/tmp/astrid-u2-typecheck/bin/python`: unavailable.
- Fallback full `compare_mypy_baseline` with agent and child venvs: **blocked by environment**, before project checking, on missing PyYAML stubs and a NumPy stub using unsupported syntax. Author trace records the original private environment result **current=1914 baseline=1914**; I do not reclassify that as a fresh run here.
- Vendor lock: **PASS**, `ok runtime.lock.json`.
- Artifact manifest: **PASS**, `artifacts.json is current`.
- `git diff --check`: **PASS**.
- Import provenance: `astrid.sdk.timeline.validation` resolved to this worktree; `jsonschema` and `referencing` resolved from `/home/user/work/venv-agent/lib/python3.13/site-packages`; `runtime_protocol` resolved from `/home/user/work/runtime/runtime_protocol`.

## Known separate evidence

Per the saved author trace, the unchanged legacy-anchor neighbor was run once after the FPS repair and stopped at setup with `candidate.timing: legacy word anchor is missing` during the initial `track.create`. It reached timing validation after FPS parity; the test body did not run. This is the separately assigned next legacy-anchor/D12 issue, not an FPS failure. I did not rerun the failed neighbor or claim 52/54/full-suite PASS.

## Recommended next step

Merge/review this scoped FPS/D12 delta as PASS, preserving the separate anchor setup failure for the assigned Sol repair. Re-run the unchanged neighbor only after that meaningful timing-boundary repair.

