# App M2 producer physical startup final custody review — 0551

## Result: HOLD — concrete custody/qualification defect

The final App source is internally consistent and the 0545 probe uses the
existing `DirectHarness`/`startRuntime` path, but I cannot approve the tuple for
producer actual. The required central source-preflight and startup-only result
does not exist, and the startup gate does not hash-bind all worker-owned
executables/probe bytes before invocation.

This is a process/custody defect, not a Runtime or App product finding. No App
source, Runtime guard, test, wrapper, or 0545 artifact was changed by this
review. Existing live callers remain unchanged.

## Frozen source and wrapper identity

- App keeper: `/home/user/work/wt/ap2-m2-producer-physical-keeper-startup-preflight-0545`
- App HEAD: `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7`
- App tree: `fd16d32fd3487e56c9fe1ff16582dba240f63b77`
- Source ancestry: `00bbc22d63b4abe7275cfe9ad5f3762157d7394f` → the single changed path
  `scripts/testing/run-producer-public13-list.sh`
- Committed successor wrapper SHA-256:
  `329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352`
- Successor gate SHA-256:
  `c365641bdeca10b9d740d5968c9a1161db7b18f8bf49e9d8bd46f14aae60cfab`
- Startup gate SHA-256:
  `8f3be0c8fcb18ab474b8d5b31c8b6a17b1cdc3d02324b4159d184c266357013c`
- Startup probe SHA-256:
  `4beb7c22dfa06e04d28253dbab02f76ff2a9953f0accd4b12247514e4f0608f6`
- Frozen Agent: `8130a401bf44a518d5a40ae274d398b8c560be55`, tree
  `236c3e57e0265c52b81ba8085de3193026176bff`
- Frozen Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`

The successor gate diff against approved `cc7` is limited to keeper path,
HEAD/tree, wrapper hash, and KEEP path. The App keeper is clean, the node_modules
link is the expected read-only `/home/user/work/app/node_modules`, and the
wrapper-only source delta is preserved.

## Code/probe review

The startup probe imports the existing
`tests/e2e/local/support/harness.ts` module and calls
`new DirectHarness().start({ seed: false })`; that existing `start()` calls the
unchanged public `startRuntime()`, waits for direct `/v1/health`, and the probe
also checks the Runtime door health before `harness.stop()`. The negative case
plants a symlink at the realm root and requires Runtime startup refusal. The
probe does not invoke Playwright, Vite, a build, or a producer test/body, and it
does not print credentials or tokens.

The startup gate creates a physical short `/tmp/tla-startup-*` carrier, clones
the exact Agent/Runtime commits, sets the same Agent/Runtime pins and physical
`TMPDIR`, and invokes only the probe. Browser executable, browser/cache paths,
Chromium args, and timeout options in the committed wrapper remain unchanged.
Runtime’s source guard and the planted symlink negative remain untouched.

## Blocking defects

1. `producer-startup-only-gate.sh` invokes the worker-owned
   `producer-startup-only-probe.ts` through
   `"$KEEPER/node_modules/.bin/tsx"` but has no literal probe SHA-256 check.
   It likewise does not bind the `tsx` executable/module bytes. A final suite
   command cannot safely claim the exact probe from the gate as written.
2. No named central suite entry or literal command for
   `producer-startup-only-gate.sh` is present in `orch/tests/suites.conf`, and
   no result directory exists for this 0545 source preflight/startup smoke.
   Therefore there is no authoritative result proving candidate source
   preflight, real daemon startup/health, teardown, or body count zero.
3. The 0545 startup gate runs only `producer-physical-keeper-gate.sh
   preflight` before the smoke. The previously approved `cc7` evidence proves
   the inherited wrapper’s drift/unknown-mode/zero-test/child-RC behavior, but
   it is not a central result for this successor tuple. Those guards must be
   rerun or explicitly bound through the final successor command.

The prior 0538 report explicitly said startup proof was not run; the 0528
`cc7` preflight is for the old `17d2518c/tree d63fe4f1` tuple and cannot be
relabelled as proof of this `b8cc7e1c/tree fd16d32f` candidate.

## Commands and results

Passed read-only checks:

```text
git status --porcelain --untracked-files=all                         PASS (keeper clean)
git diff --name-status 00bbc22d... b8cc7e1c...                       PASS (wrapper only)
diff -u approved-cc7-gate successor-gate                           PASS (only ROOT/HEAD/TREE/wrapper/KEEP bindings)
sha256sum wrapper/gates/probe                                       PASS (hashes above)
sh -n producer-physical-keeper-gate.sh producer-startup-only-gate.sh PASS
physical keeper/node_modules and locked graph checks                 PASS
DirectHarness/startRuntime/source-path audit                         PASS (read-only)
```

Not run by this worker: any local daemon/socket/browser/build/install/producer
execution; no App test suite; no replacement central request. The required
central result is absent rather than failed.

## Smallest correction required

Have the gate owner add literal final hashes for the startup gate, the owned
probe, and the exact `tsx` executable/module (or make the central command bind
those bytes directly), register one uniquely named central source-preflight and
startup-only command, then run that same result once. Preserve the existing
Runtime guard, physical carrier, wrapper/body bytes, exact Agent/Runtime pins,
all inherited drift/unknown-mode/zero-test/child-RC guards, and no producer
actual until the result is PASS with teardown and body count zero.
