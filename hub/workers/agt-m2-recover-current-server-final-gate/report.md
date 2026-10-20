## Report

Implemented and qualified AG-RECOVER.

Changes:
- Selected Runtime `3b900c3`.
- Preserved original catalog retry version/body.
- Preserved raw transport ambiguity for `timeline.restore` retries.

Test:

```text
env ... ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime
pytest -q -o addopts= -p no:cacheprovider -m integration
tests/sdk/test_timeline_checkout_history_runtime.py::test_catalog_recover_uses_real_http_and_preserves_closure_before_revision_restore
```

Result: **1 passed in 7.27s**. No other cases or full suites ran. `git diff --check` passed.

Audit: current Agent integration `53af5383` still lacks the AG-RECOVER candidate changes in `remote.py`, restore facade tests, and related CLI tests. The AG-RECOVER deletion row must remain **HELD** pending independent Agent review and merge onto `tl/integration`; do not mark it DELETED yet. Runtime `3b900c3` / reviewed `2eacf2f` is already merged.

Commit message and `DONE` marker written.