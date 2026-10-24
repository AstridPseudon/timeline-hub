Implemented:

- Added opt-in, harness-only observer: `tests/helpers/p2_commit_phase_capture.py`
- Added focused coverage: `tests/test_p2_commit_phase_capture.py`
- Captures bounded, redacted phases with `UNKNOWN` for absent phases, concurrency isolation, transparent failures, and attach/detach lifecycle.
- Actual mounted `RuntimeHTTPServer` smoke confirmed route/provider/acceptance/receipt/HTTP observation.

Tests:

```text
8 passed in 1.03s
ruff: clean
pyright: 0 errors
compileall: pass
git diff --check: pass
```

Exact JUnit command used and evidence written to:

`/tmp/.../workers/rt-P2-element-phase-1700/evidence/phase.xml`

Helper hashes:

```text
p2_commit_phase_capture.py e68425c1f128609e77d2b5cf914af55e02d7fbdf732faf46cf73d2937887ec7b
test_p2_commit_phase_capture.py a5115e8953a6a4311fef1705441820fd4f342d6a262b3e89ea23a6d4eac59af4
```

App wiring distinction: App’s normal launcher spawns `python -m runtime_protocol.cli start` in a separate subprocess and currently has no mechanism to import this test helper. App must explicitly add `PYTHONPATH` plus a worker-start activation call:

```python
capture = install_p2_commit_phase_capture(os.environ["P2_PHASE_SINK"])
# run normal Runtime worker
capture.stop()
```

No App files, product Runtime files, contracts, packages, or pins were changed.