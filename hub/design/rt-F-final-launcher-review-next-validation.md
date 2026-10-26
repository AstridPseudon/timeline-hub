# F-final protected review validation

Review result: **FAIL** on the intrinsic dry-run row finding in `findings.md`.

Commands and results:

1. `sha256sum /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-launcher-fix-1719/evidence/check-launcher.py` — PASS; `a850c28bb5872e9f8adad7ebb35730f5369078630e2cacf4094e5198c0338413`.
2. `TMPDIR=<review evidence/tmp> python3 <author evidence/check-launcher.py>` — PASS. This ran the supplied unchanged acceptance script. It covered AST/JSON/private compile/Ruff F/bash syntax, the original final-row import failure, candidate final-row startup and harmless stub, and private scoped-CAS controls.
3. `python3 <author evidence/candidate/receiving_controls.py>` with `TMPDIR`, `TMP`, and `TEMP` set to review `evidence/tmp` — PASS; actual private installer/readback/backup/fsync/drift/wrong-row/outside-byte/poisoned-caller controls.
4. Exact hashchecked `python3 -c` launch from `/home/user/work/runtime`, with `PYTHONPATH`, `PYTHONHOME`, and `NODE_PATH` unset, caller `--help`, snapshot-only: original registered row — FAIL exit 1 (`ModuleNotFoundError: delivery_lifecycle`); candidate row with only `sys.path.insert(0,str(p.parent))` — PASS exit 0.
5. Independent `shlex` comparison of current registry rows against candidate rows — FAIL: `delivery-v2-final` has the intended parent-path insertion plus path/tuple substitutions; `delivery-v2-dryrun` additionally loses `--wrapper-sha`, `--builder`, `--builder-sha`, and `--receipt`, and changes the wrapper value to `delivery-v2-receipt.json`.
6. Source manifest closure hash/mode audit — PASS for all 11 candidate files, pinned caller/helper/D68/builder/core/inventory/tuple files, and current registry hash `0495919f9ab694d034ca53d77877c90d5553560ac3bbcbf7e90e8b268e227e15`.
7. Review monitor — PASS: available bytes stayed above the 4 GB floor; the review monitor recorded a real child PID, exit 0, `wait`/reap, and 5-second samples in `disk-trace.txt`.

No full suite was requested. No real builder, dry-run, clone, request-test, staging, canonical installation, ZIP, or product test was run.
