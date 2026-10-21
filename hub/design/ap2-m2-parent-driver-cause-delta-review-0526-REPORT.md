# AP2 M2 parent driver cause/delta review

## Verdict

HOLD for one durable-registration correction; no App source change is needed
in this review worktree.

The exact 26621 first failure is the frozen durable driver's stale ancestry
guard, not cleanup loss or a product failure. Its line 168/182 executes:

```text
git -C "$app_root" merge-base --is-ancestor \
  7e85d89120227f336a2e8dbf8e0ea44d98311da0 "$observed_app_head"
```

Against the approved keeper `a304dce02a185a4774ff514d5aa451c9702aa46f`, the
guard returns `1`. `set -e` exits before `run_root` is created, so the later
`runner.log` absence is expected. The current App source already carries the
reachable anchor `84ec385a463fd4907628e68e87aabbe717202a96`; the same
ancestor check returns `0`.

The smallest exact candidate is therefore a byte-for-byte promotion of the
current App driver source to the owned durable executable, followed by a new
final hash binding. The current source bytes are:

```text
path: tests/e2e/local/support/run-parent-manual-drop-evidence.sh
sha256: 34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2
git blob: c0c185090c8511060694d7a4d0e0d815ca50a719
```

The stale durable executable remains unchanged at SHA-256
`40c7b57b6f327bafa82f26daaa4053f405e89f7bd48b5aacdadd21b2393867f0`.
The frozen keeper gate remains unchanged at SHA-256
`2fe1bf06d796d1342870a02a06a0d0f10057ba20bc2a29e0cad8a43deaaf16e1`, with
its old `DRIVER_SHA=40c7...` binding. I do not approve a future actual until
the durable copy and that binding are updated together and independently
rehash-verified.

The first-cause worker's larger source patch (failure-stage context and a
base-Python assignment) is not the smallest exact repair: it does not update
the external durable executable that actually failed. It should not replace
the existing selector, timeout, assertion, source, or authority controls.

## Custody and controls

- Keeper source remained immutable: HEAD `a304dce02`, tree
  `a3c82aa91f1336b86491191acf857d88c56179b2`, clean status.
- Original durable driver, helper (`af83e829f73ebcf9613e67808f81cab06c2e78f70c21bc850550cde1b5885fa4`), source runner, and keeper gate were read-only during this review.
- Existing App source selector remains the exact mounted manual-drop case at
  `three-products.spec.ts:1440`; no argv, timeout, assertion, source pin, or
  authority guard was weakened.
- No credential-bearing shell trace was used. The offline stubs emitted only
  fixed diagnostic text; no environment values or tokens were printed.
- The current driver retains runner output before disposable-root cleanup;
  its existing probe also refuses a planted zero-test result.

The real driver branch was exercised offline with private temporary build and
Playwright child stubs, while traversing the real setup path through the
existing child seam. The controls passed:

1. Positive: source/artifact verification, private node graph, vendor-lock
   update/check, exact one-test collection, build boundary, child dispatch,
   required-case verification, and evidence retention; exit `0`.
2. Negative: the stubbed child wrote `diagnostic child stderr` and exited
   `73`; the driver returned `73`, retained that stderr in `runner-tail.log`,
   and recorded `runner_status=73` before disposable cleanup.

These controls used `NORMAL014_USE_BASE_PYTHON=1` as the already-established
offline prerequisite. A run without it correctly reached helper-owned pip
setup and refused because network/package resolution is unavailable; no
install or shared dependency mutation occurred.

## Verification

Commands run in this review worktree:

```text
sh -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh — pass
NORMAL014_RECORD_DIR=<private> sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh probe — pass
git diff --check — pass
git merge-base --is-ancestor 7e85... a304... — exit 1 (stale anchor)
git merge-base --is-ancestor 84ec... a304... — exit 0 (current anchor)
```

No parent actual, browser, localhost/socket, real build, full suite, install,
source mutation, or central test request was run. The offline child controls
used only private temporary stubs and were cleaned up. The review worktree is
clean.

## Remaining prerequisite

Promote the exact current source bytes above to the durable executable,
update the owned keeper gate's `DRIVER_SHA` to `34ee03...`, rehash the final
keeper executable, and run its existing negative custody controls. Then—and
only then—one newly authorized future actual may be requested. Live callers
and suite selectors remain unchanged.
