## Report

Implemented opt-in P2 Runtime phase capture wiring.

- Updated [harness.ts](/home/user/work/wt/app-P2-safe-phase-wire-1715/tests/e2e/local/support/harness.ts).
- Added [sitecustomize.py](/home/user/work/wt/app-P2-safe-phase-wire-1715/scripts/testing/sitecustomize.py), importing the real Runtime helper from `tests/helpers/p2_commit_phase_capture.py`.
- Added focused bootstrap coverage at [p2-runtime-phase-bootstrap.test.ts](/home/user/work/wt/app-P2-safe-phase-wire-1715/tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts).
- Capture is enabled only with `D66_RUNTIME_LOG_DIR`, uses private TMPDIR output, 0700 directory/0600 sink, bounded summaries, and flushes on exit.
- Normal Runtime launch command remains unchanged: `python -m runtime_protocol.cli start ...`.
- Runtime helper verified identical to `04de3cc`; Runtime source HEAD is `2c1bf08771565fc77de4e6d92f7454f27d988f4d`.
- No Runtime production hooks, D66 launcher files, original specs, or product code changed.

Validation passed:

```text
Node 20 focused bootstrap test: PASS
ESLint scoped files: PASS
tsc --noEmit -p tsconfig.node.json: PASS
git diff --check: PASS
six original journey spec hashes unchanged: PASS
```

The actual browser/service P2 journey was not run, as required; it remains ready for the manager’s existing case-1 recipe with `D66_RUNTIME_LOG_DIR` set to a private TMPDIR child.

Commit message written and `DONE` marker created.