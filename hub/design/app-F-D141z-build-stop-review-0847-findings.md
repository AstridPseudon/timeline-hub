# Findings — F D141z

## F1 — FAIL: production dependency paths are unavailable

`ops-d141z-build-stop/run-final-delivery.py:25-35` points at the worker-evidence
paths for `run-final-services.py`, `core-inventory.json`, and
`delivery_gate_build.py`. Read-only existence checks found all three absent.
The only present D68 source is the six-input safe copy at
`design/runtime-D141z-input-0812-delivery_gate_build.py`. `main()` always calls
`checked_file()` for the core runner, inventory, wrapper, and builder before
dispatch (`:220-224`). Therefore the actual caller cannot reach the lifecycle
from this source venue. The acceptance bypasses this by calling
`candidate.run_wrapper()` directly.

Required follow-up: resolve/publish the exact genuine dependencies into the
normal final venue with their existing hashes, or explicitly keep this source
held as unusable. Do not substitute a fabricated wrapper or runner.

## F2 — FAIL: donor trace custody is not preserved

The installed donor publishes an immutable ready binding and
`d141-append-final.py` reopens the exact descriptor, checks device/inode/owner/
mode/link count and passes `--fd` plus the binding to the validator. The
candidate's `_read_ready()` only checks `line.startswith("ready\t")`; the
opaque binding is stored but never parsed or checked. `_validate_trace()` calls
the validator in path mode, not the donor append-final descriptor path. A
replacement of the trace pathname can consequently be the file read during
monitoring and final validation. This violates the requested append/validator
custody and makes the donor PASS non-transferable.

## F3 — FAIL: one-heavy admission does not interoperate with normal service

The candidate's `HEAVY_LOCK` is a new private `/tmp` flock. The installed
normal service's heavy admission is the `test-run` state scan and per-run
`heavy` marker; its `alive heavy` check never consults this lock, and the
candidate never consults the service state. This is not one shared heavy slot.

## F4 — FAIL: acceptance does not exercise the actual production caller

The exact check passed, but its stop, timeout, sampler, signal, and cancel cases
call `life.run_delivery()` directly. Only one normal case calls
`candidate.run_wrapper()`, and no case invokes `candidate.main()` or the real
D68 wrapper construction. The stub validator ignores donor custody fields.
Thus author PASS booleans do not evidence the whole path
`final caller -> D68 wrapper -> builder`.

## F5 — FAIL: required process/cancellation seams are untested

The check's builder always calls `p.wait()` after spawning its child. It has no
early-leader-exit-with-live-descendant case. Its cancel case uses a timer to
create a local file and direct helper invocation; it does not mount or exercise
the installed caller/parent-death/control-pipe cancellation semantics. The
claimed control set is incomplete even though the harmless process-tree cases
pass.

## F6 — scope discrepancy: tracked bytecode is outside the manifest

The branch tracks two CPython 3.13 timestamp-based `.pyc` files under the
candidate directory, while the author manifest and install map declare four
source/control files only. No deletion was made. The next owner must decide
whether these artifacts are explicitly conserved or excluded before any
installation; this review does not authorize installation.

