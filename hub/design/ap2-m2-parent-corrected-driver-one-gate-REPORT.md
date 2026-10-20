# Corrected parent-media driver review

## Result

**HOLD / blocked on central test-service cache.** The correction is safe, but
the required genuine-drop gate did not execute, so no genuine File or retained
browser evidence is proven by this worker.

Reviewed donor `tl/ap2-m2-parent-snapshot-tree-guard-source`:

- original App `HEAD`: `74643bed98fc9bf3102f544bc189e6464510f58b`
- original App full tree: `a75e27930df49a0c4ee9005806d59b14f16d2361`
- donor worktree: clean

The App correction changes identity acceptance only to exact full-tree plus
clean-source validation, and records the observed synthetic App `HEAD` in the
returned identity/source report. Agent, Runtime, and Runtime-producer checks
still use strict exact `checkHead` SHA checks. The private driver keeps the
original expected App `HEAD` and tree metadata, validates the observed
synthetic `HEAD` as a full SHA, requires the exact tree and clean status, and
retains source/evidence before disposable-root cleanup. No unsafe fallback or
ancestry acceptance was found.

## Tests

- `node --test --experimental-test-isolation=none scripts/testing/current013-integration.test.mjs` in the donor — **16 passed, 0 failed**.
- `node --check scripts/testing/current013-integration.mjs` — passed.
- `node --check scripts/testing/current013-integration.test.mjs` — passed.
- `git diff --check HEAD^ HEAD` — passed.
- `sh -n .../run-parent-manual-drop-evidence.sh` — passed.
- `sh .../run-parent-manual-drop-evidence.sh probe` — passed.

The one authorized central request was:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-snapshot-tree-guard-source ap2-m2-parent-retained-evidence-real-gate) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Request ID: `ap2-m2-parent-snapshot-tree-guard-source-ap2-m2-parent-retained-evidence-real-gate-1020224738-5811`.

Result: **cache hit; not re-run**. The service returned the prior exact-tree
result `ap2-m2-parent-snapshot-tree-guard-source-ap2-m2-parent-retained-evidence-real-gate-1020224252-16049`, **exit 1 in 1s**, before build/browser/socket execution. That prior run failed on the old exact-`HEAD` driver guard. No trace, request/response, console, native refusal, wire, or retained evidence was produced by the cached result. This is not browser or genuine-drop evidence.

No second request was submitted, and no local browser, socket, or full suite was
run.

## Next step

The test-service cache must be invalidated by the orchestrator through its
normal controlled mechanism, then the same named gate may be run once against
the unchanged donor and corrected driver. Until then, retain this HOLD and do
not count the cached `16049` failure as qualification.
