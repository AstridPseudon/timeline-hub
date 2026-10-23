Implemented the scoped R2 correction. **Final acceptance: 116 passed in 57.69s.**

- Changed only `_step_undo.py` and new `test_nested_config_root_history.py`.
- Independently reproduced old RED offline from packet SHA256 `8bf50adeb0b21c0d3e621d890dadd5d26221c415d048c12505f69be4a3dbb13d`: authentic redo `txn-cf7414…` failed with `history_unavailable`.
- Final code authenticates that exact history and reaches the existing `intervening_write` refusal. Exact closure reversal and public 409 refusal without preparing or writing pass.
- Added 22 tampering controls using lossless captured history. Existing strict controls remain unchanged.

The correction admits the full native config input after aggregate clip writes only while its clips equal the initial mirror and no earlier config/compiler observation intervenes. An initial candidate exposed the existing native-order rejection; tightening this condition restored it.

Final acceptance command:

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

Additional checks passed:

```bash
/home/user/work/venv-agent/bin/ruff check astrid/sdk/timeline/_step_undo.py tests/editing_conformance/test_nested_config_root_history.py

/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy --follow-imports=silent --no-incremental --cache-dir "$TMPDIR/mypy" astrid/sdk/timeline/_step_undo.py tests/editing_conformance/test_nested_config_root_history.py

/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004

/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

Mypy: no issues in either changed file; parent-shadow comparison also had no diagnostics. All 3,435 checked tracked files outside the allowed paths retained their HEAD identities. Credential scan: zero findings.

Scope: `07e6`’s mirror seam also rejects this history, with a compiler-observation error. That was a function-level probe using current source within the draft environment, not whole-current qualification. This patch is against `f120159f`; no ancestry join or merge was performed.

No blockers. Commit message and `DONE` written. No original public body, full suite, browser, or journey run. Recommend independent review, then the manager’s single authorized meaningful body run. G5 remains P1-gated.