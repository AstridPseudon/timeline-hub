**PARTIAL — bounded Agent repair complete; production qualification remains FAIL.**

Changed only the three allowed production files and the new focused test. Published item tokens now resolve through verified placement-local mappings; aggregate storage preserves local IDs; inverse folding retains source boundaries. Missing/corrupt/nonbijective mappings, foreign owners, changed revisions, local aliases, and equal-byte retargeting are refused.

The original offline accept/preview controls changed from **2 failed to 2 passed**. Existing media tests and all **59 original ABA assertions** remain unchanged.

Validation used worktree-first `PYTHONPATH="$PWD:/home/user/work/runtime"`, `PYTHONDONTWRITEBYTECODE=1`, and private `$TMPDIR`:

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 --tb=short tests/editing_conformance/test_authoring_landing_projection.py tests/editing_conformance/test_headless_root_mirror_effects.py tests/editing_conformance/test_authoring_undo_projection.py tests/editing_conformance/test_private_sequential_capture.py tests/editing_conformance/test_provider_step_undo_v2.py tests/editing_conformance/test_authoring_item_observation_boundary.py
# 132 passed in 13.07s

/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 tests/editing_conformance/test_recipe_occurrence_media.py tests/editing_conformance/test_occurrence_media_manifest_inverse.py
# 113 passed in 9.31s

/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_command_state.py astrid/sdk/timeline/inverse.py astrid/sdk/timeline/native_occurrence_media_commands.py tests/editing_conformance/test_authoring_item_observation_boundary.py
# All checks passed

/home/user/work/venv-agent/bin/python -m mypy --cache-dir "$TMPDIR/mypy" --follow-imports=silent astrid/sdk/timeline/_command_state.py astrid/sdk/timeline/inverse.py astrid/sdk/timeline/native_occurrence_media_commands.py tests/editing_conformance/test_authoring_item_observation_boundary.py
# Success: 4 source files

/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
# ok runtime.lock.json

/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
# artifacts.json is current

git diff --check
# passed
```

**Remaining blocker:** retaining two shared occurrences in the strict Runtime control produces **2 failures**:

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 --tb=short "$TMPDIR/test_materialized_item_boundary.py" -k test_same_alias_inverse_observations_validate
```

Runtime’s [`timeline_commit_auth.py:1160`](/home/user/work/runtime/runtime_protocol/timeline_commit_auth.py:1160) rejects translated published item paths with `inverse stage native write membership differs from its authenticated stage`. This requires owner review of the authenticated stage-address seam; no Runtime change or guard relaxation was applied.

Numeric `assets` and `audio_bindings` paths remain unchanged. No full media repair, original11466, live, browser, full-suite, or integrated-home qualification is claimed.

Recommend independent review, then Agent/Runtime owner coordination on the remaining mismatch before integration or the original managed run. `commit-msg` and bounded-completion `DONE` were written.