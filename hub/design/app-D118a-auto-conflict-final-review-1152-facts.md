# D118a protected final independent review

Verdict: **PASS**.

## Source identity

- Base `tl/app-D118a-auto-completion4-1134`: `0ad49261ed36f043b059c07de989bd39cd3a5889`.
- Reviewed author/final source: `4319be817c413c9ab51547c1cb34d3bf8f850ec2`.
- Clean pinned Runtime: `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`.
- Target test SHA-256: `24181b4206844cea66c3ca3dcd43b26b889f6cfac9b17cf4e3d7b1c8cc7e6ac1`.
- Frozen R4 candidate SDK does not contain the target test file.

## Exact-source verdict

The author commit changes only `tests/editing_conformance/test_commit_runtime_parent_auto_completion.py`, replacing the conditional expected reason with strict `expected_reason = 'value_conflict'`. The reverse proposal check passes against the applied author tree; the proposal's one-line change and context apply cleanly in reverse. No request reads, authored timing/media inputs, status/reason unions, or optional guards were changed.

The only changed path versus base is the allowed test file. Normalized AST matches base after normalizing only the `expected_reason` assignment. The original strict reason assertion, SQL no-write predicate, candidates/rows/head assertions, and CAS/staging/snapshot byte equality remain present.

Production SHA-256 is unchanged from base for every reviewed blob:

- `astrid/sdk/timeline/native_auto_placement.py`: `c46e23ac43dc506ba8362abc0dbb2bf145f96ed6365b594936f83476d5490907`
- `astrid/sdk/timeline/native_parent_media_commands.py`: `673643ab9dd0f094c57da49f78c581fba5f08e7b00c7b364a41e20a0a13d5964`
- `astrid/sdk/timeline/_recording.py`: `85aefe0328a7c9787a18c2b7e19eb8b3e4220a1c53627d1e16102b42b29c8b43`
- `astrid/sdk/timeline/_commit_patch.py`: `76224a62434ade240e298bf6a1d14b64bdc2ed650923c2160cf22bdbb23a4a50`

The production caller records genuine anchor field reads for `at`, `at_ms`, `track`, `hold`, `from`, `to`, and `speed`; it emits one ordinary `clip.add-media` row with literal authored values. The classifier maps non-collection field guards to `value_conflict`, collection guards to `selection_changed`, and scope guards to `dependency_changed`. This matches C0 §3 lines 604–612 and 637–648. Approved comparison commits `cb35bd4fb5619f55edb4029f899b71f4c0d0dd57` and `824e03f6a2139561af65a9c69779ea7a1a7a0a4c` classify the same parent-auto field path as `value_conflict`.

## Exact four-node run

Command used the existing `/home/user/work/venv-agent` and clean `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-42aad0e9`, with no socket/browser/full suite:

`python -m pytest -q -o addopts= -p no:cacheprovider -m integration --junitxml=.../evidence/four-node.xml tests/editing_conformance/test_commit_runtime_parent_auto_completion.py::test_relevant_stale_reads_refuse_before_accept_and_any_persistence[image-at] ...[image-hold] ...[video-at] ...[video-hold]`

Result: `4 passed in 5.05s`.

The actual tiny JUnit receipt is preserved in `four-node.xml`; stdout/stderr is in `four-node.log`. It reports four testcases with zero errors, failures, or skips.

## Static checks

- Ruff: pass.
- Mypy `--follow-imports=skip`: pass.
- `PYTHONPYCACHEPREFIX=/tmp/app-D118a-final-review-1152-pycache python -m py_compile ...`: pass.
- `git diff --check HEAD^ HEAD`: pass.
- `git diff --check 0ad49261ed36f043b059c07de989bd39cd3a5889..HEAD`: pass.
- Normalized AST conservation: pass.

No blocker. Recommended next step: manager may proceed with the normal protected remote merge flow.
