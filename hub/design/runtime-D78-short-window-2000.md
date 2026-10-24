# D78 Runtime short-window qualification

## Result

No Runtime/product source change was made. Runtime `P2CommitPhaseCapture` already
supports the caller-selected interval. The App owner’s current D78 source is
`860e9755c876ce510aabc5af0511ffe1886626f6` (`Merge tl/app-P2-D78-early-watchdog-bootstrap-1952`).
The exact source diff is reproducible with:
`git -C /home/user/work/app diff HEAD^ HEAD -- scripts/testing/d66-plain-stack.mjs scripts/testing/sitecustomize.py tests/e2e/local/support/harness.ts`.

The route-specific values are:

- ordinary `p2`: `ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS='20'`;
- isolated `p2-element`: the early window `...='2'`;
- `p1`/`p3`: the variable is empty, so those routes do not select a watchdog interval.

## Exact Runtime helper contract

- Runtime helper: `tests/helpers/p2_commit_phase_capture.py`.
- `DEFAULT_WATCHDOG_SECONDS = 20.0`.
- `DEFAULT_MAX_WATCHDOG_CAPTURES = 1`.
- Constructor bound: `watchdog_seconds > 0`; non-positive values raise
  `ValueError("capture bounds must be positive")`. The helper has no upper-bound check.
- App `sitecustomize.py` adds the only input parser: absent/empty preserves the Runtime
  default; a value must parse as finite and positive, otherwise bootstrap fails closed.
- The timer is created only when the existing `enabled=True` activation is started with
  a sink. It is daemonized, request-owned, and canceled on dispatch return, raised or
  aborted return, `stop()`, and restart. The all-Python-thread dump remains private
  `0600`; the global allowance remains cap 1.

## Concrete normal D66 launch path

Read-only inspection of App D66 source at the current App checkout shows:

1. `serviceRecipe()` selects `2` only for `p2-element`, `20` for ordinary `p2`, and
   empty for other suites.
2. `DirectHarness.start()` creates the private `D66_RUNTIME_LOG_DIR` sink and starts
   the neutral Runtime.
3. `seedRuntime()` calls `enableTimelineAuthoring()`, which restarts the Runtime with
   `timelineAuthoring=true`.
4. `startRuntime()` allocates the launch-ordinal sink, adds App `scripts/testing`, the
   selected Runtime, and the selected Agent to `PYTHONPATH`, and launches the normal
   `python -m runtime_protocol.cli start ...` command.
5. Existing `sitecustomize.py` imports before that module command, consumes the exact
   watchdog variable, imports the selected Runtime helper, calls
   `P2CommitPhaseCapture(..., enabled=True, **options)`, and registers `stop()` at exit.
6. With D66 `deferTimelineInitialization=true`, `seedThreeProducts()` invokes the
   native seed through `commitNativeSeed()` after this authoring Runtime is active.
   Later real App dispatches use the same observed daemon. A restart gets a new sink
   ordinal and activates the helper again.

This proves a real source-supported activation/propagation path; no hypothetical
endpoint, body, browser, or new Runtime/product hook is involved.

## Cap-1 limitation

The cap is global to one capture instance. A slow but ultimately successful native seed
can consume the single 2-second watchdog capture before the later element request. The
later request can still be phase-observed, but it will not receive a second stack dump.
This is an honest bounded-helper limitation; no expanded cap/framework is justified by
the current evidence.

## Evidence commands

- `/home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/test_p2_commit_phase_capture.py --junitxml=<private evidence path>` → `12 passed in 2.72s`.
- `/home/user/work/venv-runtime/bin/python <private sanityhelper>/qualify_p2_short_window.py` → `default=20.0 positive=2.0 cap=1 invalid=0,-1,-0.001 rejected helper_compiles=true`.
- The App D78 diff is clean under `git diff --check`; no App files were changed by this worker.

## Source hashes

```text
aa68327d6ad8c886c7d7d7bbe42bca2c7e1c28a36ab58f9e3c25d66dd51bb41c  Runtime tests/helpers/p2_commit_phase_capture.py
e9cc10fbaefe9fbb02336b2ccab889cd288f408d2b986951c8a48b0c65e24f9f  Runtime tests/test_p2_commit_phase_capture.py
83c28b437417753a221e0fec36047dd6bb267256366dd4acacb8ef8d8137615e  App scripts/testing/sitecustomize.py
92f1261bc3213824f8323202e6a7f3d117892dda5ef6a847f0fd571a6cf81956  App tests/e2e/local/support/harness.ts
b54449cd3dfc9ddf09741ae24553a6ea799b0a4be667cc8607750845c929ed4b  App scripts/testing/d66-plain-stack.mjs
f94bc51863ac6be7b9f88c06f46988ae4d9561215b20665b58121e113b10e9bb  App tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts
```
