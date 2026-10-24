Implemented the source-only normal-maker join on exact base `ab6d49bfb` / tree `a494ab2f`.

- Authenticate Farm inputs before Store selection; bind component authority alongside bootstrap authority.
- Retain and revalidate the original schema Git archive, complete receipt, and separate test2 wheels at staging, final, and reuse.
- Preserve the 140-test body, proof.lock236d, complete-root guards, and 8 GiB reserve.

Imported only the reviewed component/test blobs from `234eeb443`:

- Component: `0558a58a28496607cfbe668484ed37815442b8da`
- Tests: `ee1bb8cb6ed56ca44bef195dff54e7bccbdefb1c`

Source author is **Codex HARD Sol1012**; reviewer “Claude” wording describes Git/harness metadata.

Validation:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider ops-handoff/child-dependency-reuse/tests/test_farm_distribution_join.py ops-handoff/child-dependency-reuse/tests/test_farm_distribution_inputs.py ops-handoff/child-dependency-reuse/tests/test_dependency_reuse.py --timeout=45 --junitxml=$TMPDIR/farm-join.xml
```

**267 passed, 1 failed, 1 warning; 100.58s.** All 54 join and 74 component controls passed. The unchanged baseline guard fails because historical maker `e4c0a9…` differs from approved install1023’s live `c1197e…`.

Ruff, source mypy, normalized mypy (**9/9 identical; zero new**), compilation, bash syntax, manifests, pins, installed-baseline checks, and diff checks passed.

Acceptance is **BLOCKED** by that baseline discrepancy. Commit message and `BLOCKED` marker written. Next: orchestrator reconciliation and independent cumulative security review.

Authentic schema remains **HELD**; real Farm child remains **NOT QUALIFIED**. No acquisition or live installation occurred.