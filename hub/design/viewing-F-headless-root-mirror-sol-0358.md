**PASS — bounded F-headless-root-mirror repair complete.**

Changed only `CommitPatch.finish()` in `_commit_patch.py` and the new `test_headless_root_mirror_effects.py`. The all-parent shortcut now retains complete provider-derived effects when mirror topology changes. Existing ABA/reorder paths remain unchanged.

Proof: the finalized preview/acceptance regressions fail with baseline `CommitPatch.finish()` at “provider effect has a different input value”; repaired code passes through the mounted production caller and unchanged Runtime `step_output()`.

All commands used `PYTHONDONTWRITEBYTECODE=1`, worktree-first `PYTHONPATH="$PWD:/home/user/work/runtime"`, and `/home/user/work/venv-agent/bin/python`:

```bash
python -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 tests/editing_conformance/test_headless_root_mirror_effects.py tests/editing_conformance/test_private_sequential_capture.py tests/editing_conformance/test_authoring_undo_projection.py tests/editing_conformance/test_provider_step_undo_v2.py
# 63 passed in 8.78s

python -m ruff check --no-cache astrid/sdk/timeline/_commit_patch.py tests/editing_conformance/test_headless_root_mirror_effects.py
# All checks passed!

python -m mypy --cache-dir "$TMPDIR/mypy" --follow-imports=silent astrid/sdk/timeline/_commit_patch.py
# Success: no issues found in 1 source file

python scripts/vendor_lock.py check runtime.lock.json
# ok runtime.lock.json

python scripts/artifact_manifest.py --check
# artifacts.json is current

git diff --check
# passed
```

Controls cover invalid before values, created declarations, submitted-step assertions, corrupt effects, foreign-root effects, source bindings, native write ranges, and nested synchronization. No inherited lint/type diagnostics.

Limits: root-absent output is verified at the genuine prepared boundary; Runtime’s current wire schema requires root `clips`. Schema-valid topology changes pass preview, acceptance, and history. No original headless family or full/live/browser suite ran.

Runtime follow-up: development probes accepted isolated corruption of track allocation `owner` and a native write owner ref. Those validation gaps remain outside this repair.

Recommend independent review, then Runtime-owned original-family qualification. Commit message and `DONE` written; no Git writes performed.