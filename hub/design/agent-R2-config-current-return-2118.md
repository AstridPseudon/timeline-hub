Completed the ordinary R2 repair. **Final acceptance: 137 passed in 57.13s. No blockers.**

- Retained `4b874103e` and added exactly the reviewed 13-line `State.get/set` support for `parent.occurrences`.
- Ported the captured neighbor regression byte-for-byte, preserving every assertion; appended six permutation and 15 negative controls.
- `_root_inverse.py` is unchanged. No G5 changes or ancestry were imported.

The exact five-file command was:

```bash
PYTHONDONTWRITEBYTECODE=1 \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f \
PYTHONPATH=.:/home/user/work/wt/rt-pin-8ea0766f \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
tests/editing_conformance/test_nested_config_root_history.py \
tests/editing_conformance/test_nested_parent_mirror_ranges.py \
tests/editing_conformance/test_inverse_aba_partition.py \
tests/editing_conformance/test_nested_inverse_order.py \
tests/editing_conformance/test_captured_config_root_mirror.py
```

Results:

- Before repair: **115 passed, 1 failed, 58.45s**; native `parent.occurrences` state was absent.
- Reviewed repair with unchanged tests: **116 passed, 56.37s**, including the existing 22 tampering controls.
- Final tree: **137 passed, 57.13s**.
- An intermediate control run had seven fixture errors; corrected the fixture to use the captured pre-inverse boundary, retaining all assertions.

Quality commands passed:

```bash
/home/user/work/venv-agent/bin/ruff check --no-cache \
astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/_command_state.py \
tests/editing_conformance/test_nested_config_root_history.py \
tests/editing_conformance/test_captured_config_root_mirror.py

/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy \
--follow-imports=silent --no-incremental --cache-dir "$TMPDIR/r2-current-mypy" \
astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/_command_state.py \
tests/editing_conformance/test_nested_config_root_history.py \
tests/editing_conformance/test_captured_config_root_mirror.py

/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check \
runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004

/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

Mypy diagnostic identities were empty for `07e6`, inherited parent, and final source; `07e6` was checked using `--shadow-file` for both product files.

Scope and identity verification passed: exactly four cumulative paths versus `07e6`, all **3,429 outside-scope tracked identities unchanged**, and only `4b874103e` in existing ancestry above `07e6`. Module origins remained this worktree and Runtime `rt-pin-8ea0766f`; sampled module hashes were unchanged except `_command_state.py`:

```text
before 030d06a398ba0cde929651859a51108fa70a2e043b461130d8b24be8c594f4e0
after  5584a8d08edecf480aa223c3dcf73a5e3064cee14758ebbeef19836043db0384
```

Credential-pattern findings: zero. No full suite, original c271 body, HTTP, browser, or journey runs performed.

Commit message and `DONE` are ready. Next: independent cumulative four-path review, followed by the separate own-only clean port and normal merge.