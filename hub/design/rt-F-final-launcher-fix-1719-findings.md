# F-final launcher findings

## Fixed in this private successor

- The registered `python3 -c` hash-check/`exec` row now inserts `str(p.parent)` into `sys.path` immediately before executing the unchanged caller. This is the smallest production-path correction and avoids global `PYTHONPATH` trust.
- The current live registry preimage is `0495919f…`; the installer now authenticates that exact registry and the exact three selected final-row preimages.
- The installer replaces only those three rows in place, preserving every other byte and all four Runtime proof rows. Existing owner, mode, no-follow, tuple, source, lifecycle, native-heavy and 4GB guards remain.

## Original harness gap

The earlier harness loaded the caller with a candidate-directory `sys.path` entry. The registered row executes the absolute file with `python3 -c exec` from the service directory, so the sibling `delivery_lifecycle` module was absent. The acceptance script reproduces the old failure and then runs the exact successor row shape with inherited `PYTHONPATH`, `PYTHONHOME`, and `NODE_PATH` removed.

## Remaining limits

- No canonical registry write, real delivery builder, staging, ZIP, or production dry-run was performed. The acceptance uses a private full-path D68 stub to prove argv/source/lifecycle propagation and intentionally stops before builder/staging.
- The existing lifecycle body was not duplicated; one normal stub run produced a PASS trace and reap record. The prior SAME33 lifecycle receipts remain the controlling evidence for unchanged lifecycle behavior.
- Product types, lint, and suites are N/A because this is a private packaging-row candidate; only changed Python Ruff F and shell syntax were run.
