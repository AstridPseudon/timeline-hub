# agt-V2-boundaries-review-0606

## Result

- **Bounded D12a fix: FAIL.** The intended timing-boundary behavior is covered by passing tests, but `validation.py` adds two unrelated inherited-invalidity exemptions. If the baseline and candidate both contain a clip with a missing track, or a clip whose asset is absent, `_validate_clip_list` accepts the unchanged invalid state (`validation.py:241-243` and `255-258`). A direct reproduction accepted both cases. This violates the settled requirement that there be no inherited unrelated invalidity laundering.
- **Outstanding original-three scope case: FAIL (known and retained).** The author report and the independent Viewing0545 report document 2 PASS / 1 FAIL. The remaining stale-window case changes the legacy source search window and must continue to refuse under the unchanged-target contract. I did not rerun that known-failed case.

The diff is otherwise limited to the assigned files: `validation.py`, `_commit_timing_validation.py`, and the new `test_commit_boundaries_d12.py`. No production caller/API/receipt metadata was removed; `commit.py:1117-1125` still invokes `validate_final_candidate` with baseline, schema inputs, realm, and source bundles.

## Checks

From `/home/user/work/wt/agt-V2-boundaries-review-0606`, with `PYTHONPATH=.:/home/user/work/runtime` and `/home/user/work/venv-agent/bin/python`:

- `pytest -q -p no:cacheprovider tests/editing_conformance/test_commit_boundaries_d12.py tests/editing_conformance/test_commit_legacy_text_reference.py tests/editing_conformance/test_commit_fps_d12.py tests/editing_conformance/test_commit_anchor_d12.py tests/editing_conformance/test_commit_v2_validation.py tests/editing_conformance/test_commit_timing_validation.py` — **133 passed**.
- `pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_provider_occurrence_fork.py tests/editing_conformance/test_recipe_occurrence_fork.py tests/editing_conformance/test_native_word_anchor_vectors.py tests/editing_conformance/test_recipe_m2_clip_add.py` — **93 passed**.
- Scoped Ruff over the two production files and new test — **passed**.
- Scoped mypy with `/home/user/work/venv-agent-typecheck-v2/bin/python --follow-imports=skip` — **passed**.
- `make ruff PY=/home/user/work/venv-agent/bin/python` with private `RUFF_CACHE_DIR` — **2150/2150 baseline**.
- `scripts.reshape.compare_mypy_baseline` with private `MYPY_CACHE_DIR` — **1915/1915 baseline**.
- `scripts/vendor_lock.py check runtime.lock.json` — **ok**.
- `scripts/artifact_manifest.py --check` — **current**.
- `git diff --check` — **clean**.

The first quality attempt used the supplied `tmpdir` locator, which is a regular file rather than a directory; Ruff failed only to initialize its cache. All quality checks were rerun with private directories under `/tmp/agt-V2-boundaries-review-0606-qual/`.

## Source/import evidence

The tested validation modules resolve from this worktree:

- `astrid.sdk.timeline.validation` → `astrid/sdk/timeline/validation.py`
- `astrid.sdk.timeline._commit_timing_validation` → `_commit_timing_validation.py`
- `astrid.sdk.timeline.commit` → this worktree's `commit.py`

The runtime protocol imports used by these direct checks resolve read-only from `/home/user/work/runtime/runtime_protocol`. No shared dependency was modified.

## Decision and next steps

This was a readonly review; no source or fixture was edited, and no original test expectation was weakened. Remove the two missing-track/missing-asset exemptions or otherwise prove they are not reachable for invalid baselines, then rerun the targeted matrix. Separately, the orchestrator must decide the protected stale-window fixture/contract conflict. Do not claim 52/54/3-green or all-green acceptance until both issues are resolved. No full/browser/socket/heavy/native14/farm suite was run.
