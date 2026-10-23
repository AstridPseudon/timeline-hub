Implemented the two-file R2 port; **acceptance is blocked: 115 passed, 1 failed**.

- Changed only `_step_undo.py` and new `test_nested_config_root_history.py`. Both match reviewed `830fba00b` bytes exactly; no test adaptation or weakened assertions.
- Independently reproduced current `07e6` RED: **1 failed**, `history_unavailable: nested inverse compiler observation differs from native history`.
- After porting, the captured regression and all **22 tampering controls pass**, including exact reversal and public `intervening_write` refusal without preparation or writes.

The literal acceptance command exits **4** because current lacks `tests/editing_conformance/test_captured_config_root_mirror.py`. Its unchanged reviewed copy was tested from `$TMPDIR`:

```bash
PYTHONDONTWRITEBYTECODE=1 \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f \
PYTHONPATH=.:/home/user/work/wt/rt-pin-8ea0766f \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
tests/editing_conformance/test_nested_config_root_history.py \
tests/editing_conformance/test_nested_parent_mirror_ranges.py \
tests/editing_conformance/test_inverse_aba_partition.py \
tests/editing_conformance/test_nested_inverse_order.py \
"$TMPDIR/test_captured_config_root_mirror.py"
```

Result: **115 passed, 1 failed in 56.01s**.

The failing neighbor test, `test_captured_config_root_redo_preserves_exact_history`, authenticates successfully, then fails in `restore_root_baselines` at `parent.occurrences`. Its capture contains an accepted native occurrence-order write; current `State.get` returns absent for that address. Draft `f120/830` adds support in excluded `_command_state.py`. `_root_inverse.py` is identical between current and reviewed source. I left that precondition untouched.

Additional checks passed:

```bash
/home/user/work/venv-agent/bin/ruff check --no-cache astrid/sdk/timeline/_step_undo.py tests/editing_conformance/test_nested_config_root_history.py

/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy --follow-imports=silent --no-incremental --cache-dir "$TMPDIR/r2-current-mypy" astrid/sdk/timeline/_step_undo.py tests/editing_conformance/test_nested_config_root_history.py

/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004

/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

Parent/current mypy diagnostic identities are both empty. Current contains **3,431 tracked files**, with all **3,430 outside-scope identities unchanged**. HEAD remains `07e6d83df`; neither `f120` nor `830` ancestry was added.

Module origins remained this worktree and Runtime `rt-pin-8ea0766f`. `_step_undo.py` SHA256 changed from `459151d59444197628e0ebd3a74f1b4efdce33a97597e3e1e04878f022fcf21c` to `e47e880cfd43772415b8b8711fcf06cc21d2b93f2c86b075233cc62c014c52b1`; other sampled module hashes and Runtime/producer identities remained unchanged. Capture digest verified; credential-pattern findings: zero.

No full suite, original c271 body, browser, HTTP, or SQL run. Commit message and `BLOCKED` written; no `DONE`.

Next: independent cumulative review and an owner decision on the incompatible neighbor/precondition before claiming full acceptance. G5 remains isolated and P1-gated.