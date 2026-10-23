# R2 c271 current port — 1944

## Result

Ported the reviewed `70be7e9fcf3dc29c4195993755bebee0c3126b7a` change onto current `07e6d83df69146c7dddea207f32330dc8b58dbc5`, limited to:

- `astrid/sdk/timeline/_step_undo.py`
- `tests/editing_conformance/test_captured_config_root_mirror.py`

The `_step_undo.py` preimage was verified byte-for-byte before editing:

- current preimage: `db1dd6cc09a6f9b7cf59f8af9e49cdb9d682eb74`
- `89c38c935` preimage: `db1dd6cc09a6f9b7cf59f8af9e49cdb9d682eb74`

Both resulting blobs match the reviewed source commit exactly:

- `_step_undo.py`: `0bdefdb813c9ffcbe94c7a627512784e60da3532`
- new test: `9d3e3330b24dba2e3c2b9d5e14c0e46677c30fa5`

No other product, test, schema, Runtime, pin, environment, or Git files were changed.

## Tests

Command:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_captured_config_root_mirror.py tests/editing_conformance/test_inverse_aba_partition.py tests/editing_conformance/test_transient_root_baseline.py
```

Result: **51 passed, 1 failed** across 52 collected tests.

The single failure is `test_captured_config_root_redo_preserves_exact_history`. It fails in unchanged `astrid/sdk/timeline/_root_inverse.py:198` while guarding `parent/occurrences` (`original authored guard changed`), before the changed mirror-partition logic is reached. I preserved the exact reviewed two-blob port and did not broaden scope to repair this existing root-baseline seam.

## Static and integrity checks

- Scoped Ruff on both touched files: passed.
- Private mypy on both touched files: passed; no issues in 2 source files.
- Ruff ratchet: current 2149, baseline 2149.
- Mypy ratchet: current 1912, baseline 1912.
- Vendor lock: `ok runtime.lock.json`.
- Artifact manifest: current.
- `git diff --check`: passed.
- Scope identity: exactly the two assigned paths.
- Import origins: Agent from this worktree; `runtime_protocol` from pinned Runtime `rt-pin-2a9e347f`.
- Credential-pattern scan over touched files: 0 matches.

## Decisions and limits

The settled plan required a mechanical leaf port from the reviewed `70be` commit over the verified `89c` preimage. I made no semantic adjustment for the inherited root-baseline failure and did not run full, HTTP, browser, or live-socket suites.

Recommended next step: the orchestrator should decide whether the unchanged `_root_inverse.py` guard failure is an integration prerequisite before accepting this exact port.

