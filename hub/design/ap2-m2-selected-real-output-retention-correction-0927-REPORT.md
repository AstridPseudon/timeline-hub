# AP2 M2 selected real-output retention correction — 0927

## Result

Copied the approved 0903 runner into this worker's owned artifact directory,
kept the 0903 source copy immutable, and made one minimal retention-only
correction. No App source, helper, selected spec, selector, budget, pin,
authority, launcher, or test was changed.

```text
immutable 0903 copy:
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-real-output-retention-correction-0927/artifacts/source-0903-run-owned-selected-final95.sh
corrected runner:
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-real-output-retention-correction-0927/artifacts/run-owned-selected-final95.sh
0903/source SHA-256: 4459f2c9acd7ce411f92beab33c216e549c98fe1fad996706998e6c5aaab85a3
corrected SHA-256:   ff79ff6f32d248989b6227790cebbe34c1ffd4711b8b3dc90c0708fe6e7a8c8e
0858 reverse/source SHA-256: b3fb1336b36bd3703e3fc460ca9fe0932e9601b39c721215e07c5ca35bf535e5
```

The corrected hunk removes the requirement for a standalone DOM file. Trace,
error-context, and DOM are independently detected and copied when actually
present. The identity manifest records `*_present` and `*_retained` flags;
missing output is represented honestly rather than treated as a reason to
discard the child log and available Playwright evidence. Unsafe destination
and copy failures still return a nonzero retention result, and the child
status remains the outer status when retention succeeds.

The minimal reverse diff (corrected runner back to 0903) is exactly the
removal of the three presence/retention flag assignments and the restoration
of the three missing-artifact refusals plus all-or-nothing artifact copy:

```diff
@@ identity manifest @@
-dom_present, error_context_present, trace_present
-dom_retained, error_context_retained, trace_retained
+dom_retained, error_context_retained, trace_retained from source-path presence
@@ retention validation/order @@
-record each source presence; initialize retained flags false
-if any artifact exists, create browser-output
-copy DOM, error-context, and trace independently when present
+require trace, error-context, and DOM whenever output_files is nonzero
+create browser-output and copy all three only after those requirements pass
```

No other source/keeper/graph/Node/Vite/argv/list1/shortpath/child-status,
cleanup, or auth guard differs from 0903; the immutable source copy remains
SHA-256 `4459f2c9…` and the frozen 0858 source remains `b3fb1336…`.

## Real output mapping

The bounded fixture used the existing selected `MODE=run` launch-stub seam.
It emitted exactly the formats observed in the 13522 failure: nested
`error-context.md` and `trace.zip`, with no HTML/DOM file, then exited 17.
The retained packet was:

```text
browser-output/error-context.md  sha256 d27b851969fe1e1e39c93c8a5da46095f747c1a6a934562d50619caa0e83d0c0
browser-output/trace.zip         sha256 0efb3d7a43af40edf8d47cefe23876939ea22b0bbde9c847819562e98f9eafd2
child.log                        sha256 356db59611b56b8da4226db632ad14922a6b58409bf9d42f06b019407445c724
identity.txt                     sha256 45217ed9d77e0a77ea3ab53d681dc49a32b9aec9328b2fe2dc6f410cb2bc0721
```

Identity flags were `phase=BODY`, `child_status=17`, `child_started=1`,
`body_started=1`, `dom_present=false`, `dom_retained=false`,
`error_context_present=true`, `error_context_retained=true`,
`trace_present=true`, and `trace_retained=true`. `SHA256SUMS` verification
passed. The disposable `RUN_ROOT` was absent after EXIT cleanup. The direct
child log contains one fixture invocation and the runner's launch seam was
entered once; no browser was started. Here `BODY` means the selected child
reached its Playwright-output-producing phase; it does not claim that P1/P2,
page/DOM setup, or the full selected behavior ran.

## Exact commands and results

Syntax and manifest checks:

```sh
sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-real-output-retention-correction-0927/artifacts/run-owned-selected-final95.sh
# PASS
(cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-real-output-retention-correction-0927/artifacts/retained-evidence-real2 && sha256sum -c SHA256SUMS)
# PASS: error-context.md, trace.zip, child.log, identity.txt
```

Literal bounded run-mode command (the fixture is the existing launch-stub
seam, not a direct call to `retain_failure_evidence`):

```sh
NORMAL014_USE_BASE_PYTHON=1 \
APP_KEEPER_ROOT=/home/user/work/wt/app-pin-a50ca4a0 \
SELECTED_FINAL95_MODE=run \
SELECTED_FINAL95_LAUNCH_STUB=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-real-output-retention-correction-0927/artifacts/fixture-failure-trace-context-only.sh \
SELECTED_FINAL95_DURABLE_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-real-output-retention-correction-0927/artifacts/retained-evidence-real2 \
sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-real-output-retention-correction-0927/artifacts/run-owned-selected-final95.sh \
/home/user/work/wt/ap2-m2-selected-real-output-retention-correction-0927
# exit 17 (expected; original child status preserved)
```

The first setup-only attempt omitted `NORMAL014_USE_BASE_PYTHON=1`, reached
inherited Python preparation, and exited 1 before the fixture child; its
truthful PREBODY packet was retained and its temporary root was cleaned. It
was not counted as the bounded fixture proof. The corrected command above is
the single fixture-failure run.

## Scope and next steps

No selected actual, browser, build, daemon, socket, install, full suite, or
central service submission was run. Existing 0903 controls for physical-root,
destination, child-status, cleanup, source identity, and copy-failure guards
remain unchanged; the new proof specifically exercises the real emitted
trace+error-context/no-DOM shape. Independent first review should inspect the
29-line retention diff and verify the final runner hash above.
