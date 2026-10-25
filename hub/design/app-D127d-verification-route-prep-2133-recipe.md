# D127d normal element verification route

Status: `FINITE_UNAPPLIED` / source-only `NOTRUN`.

This packet records the exact current App route and the guard seam that must
be resolved before one future normal original-element body. It is not a
profile, and it does not authorize preflight, bootstrap, service startup,
checkout, install, registration, submission, browser execution, or a body.

## Current route found

The existing D66 route is the browser controller selected by the
`p2-element` suite:

```text
/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs p2-element --submit
```

This command is recorded only as the current source seam; it was **not run**.
`p2-element` is one selector, preserving the existing mounted element test at
`tests/e2e/local/three-products.p2-elements-assets.spec.ts:1038-1131`.
That body performs the catalog element apply (`doc.patch` with a
`list.insert`), exact params patch, authenticated history/readback, reload,
two guarded inverse/Undo phases, and zero legacy-route assertions. The
existing five-second assertion remains part of the unchanged route's source
contract; no test or source was edited here.

## Why this is not currently a normal no-hooks recipe

The current launcher defines `p2-element` with `retainRuntimeLogs: true`
(`scripts/testing/d66-plain-stack.mjs:21-24`). In the normal execution path,
`main()` calls `diagnosticHelperIdentity(..., required: suite.retainRuntimeLogs)`
(`scripts/testing/d66-plain-stack.mjs:702-712`). For this suite that resolves
the selected Runtime checkout's existing
`tests/helpers/p2_commit_phase_capture.py` when present
(`scripts/testing/d66-plain-stack.mjs:248-256`), and the normal run exports
the helper path and digest before launching Playwright
(`scripts/testing/d66-plain-stack.mjs:737-750`). The selected normal Runtime
home currently contains that helper. The same path also sets the retained
Runtime sink and launch ordinal through `playwrightLaunchEnv()`
(`scripts/testing/d66-plain-stack.mjs:289-305`).

The `--submit` path itself is additionally a two-stage D73 flow: it requests
the four exact checkouts, waits for receipts, registers preflight and normal
recipes, runs preflight, then requests the normal suite
(`scripts/testing/d66-plain-stack.mjs:627-689`). That is the required future
ordering, but it is not executable under this source-only task.

The current App source guard deliberately recognizes normal, reviewed,
reviewed-new, and reviewed-profiler helper arms
(`tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts:525-553`). It
does not provide a supported “normal route with helper/sink disabled” arm.
The current launcher therefore has no existing, source-supported way to leave
all optional diagnostic/sampling/profiling hooks off for this body. No env
flag, source patch, hook injection, CJS loader, or collector was invented.

## Conditional future handoff

After the Runtime cost candidate is independently `READY`—author receipt,
independent review/source receipt, exact SHA/tree, and immutable checkout
receipt with the controller's own absolute output root—the manager may resolve
the no-hooks source seam and then use exactly one ordinary D66 four-tuple
request, separate source preflight, and one persistent normal ID. The future
run must retain Node `v20.19.4`, the existing dependency reuse, one genuine
5.2 GB admission check and 4 GB stop threshold, one body, the original
five-second assertion, canonical/history/reload/guarded-Undo assertions, and
zero legacy-route traffic.

Until that source seam is resolved, this packet is finite `UNAPPLIED`; it
grants no functional credit and no early body. Runtime remains the sole cost
author and offline-benchmark owner. The D130 SWAP/WAL/recovery/full-tour hold
remains in force.
