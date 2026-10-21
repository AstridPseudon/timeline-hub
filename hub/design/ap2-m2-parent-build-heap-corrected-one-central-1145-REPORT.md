# App parent build-heap correction report

## Result

Applied the approved process-local build-only correction from 1135 in the durable copy of the original 1126 parent runner. The only build-command change is the one-line prefix:

```sh
NODE_OPTIONS=--max-old-space-size=8192 npm run build:hosted
```

The App worktree remained unchanged and clean (`git status --short` produced no output). No product, spec, pin, guard, source, or selected/producer runner changes were made. The corrected parent runner SHA is `da324447737623c000fee43c138e88c7445d2e0105a7984a23cde73a42605b00`, versus the original `d5d8a983...`; the recorded delta is one build-prefix hunk. Runtime/packhost sanitization and stub-failure behavior were preserved.

## Preflight and offline checks

Command:

```sh
sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-build-heap-corrected-one-central-1145/record/aggregate-preflight.sh
```

Result: `aggregate preflight PASS`. It passed source/clean-keeper/spec assertions, exact argv/list1, short child roots/socket paths, credential authority/existing-authority checks, locked graph and Agent/Runtime cohort checks (76 Runtime artifacts and 77 Composition files), Node22/Vite graph checks, sanitized environment, browser lock, disk >=10 GiB, no heavy peer processes, and zero-test retention/refusal probe.

The final `env -i` stub probe executed the exact corrected build line. It observed `NODE_OPTIONS=--max-old-space-size=8192`, argv `run build:hosted`, and stub RC 41; sentinel `NODE_OPTIONS`, `NODE_PATH`, `LD_PRELOAD`, and `PYTHONHOME` remained unchanged after the child. Two earlier malformed stub diagnostics did not invoke npm/build and are not evidence of a run.

## One central run

Exactly one bounded central-service request was made; no retry was submitted:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-build-heap-corrected-one-central-1145 ap2-m2-parent-build-heap-corrected-one-central-1145-e2e-integration --no-cache
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-parent-build-heap-corrected-one-central-1145-ap2-m2-parent-build-heap-corrected-one-central-1145-e2e-integration-1021114743-590
```

Suite ID: `ap2-m2-parent-build-heap-corrected-one-central-1145-ap2-m2-parent-build-heap-corrected-one-central-1145-e2e-integration-1021114743-590`

Result: `fail exit=1 in 668s`. The run reached the source/keeper/hash guards, 76 verified artifacts, private graph (532 packages/34 bins), Runtime lock checks, hosted build transformation of 5586 modules, and a successful Vite build in 57.28s. This confirms the 2 GiB build frontier was cleared by the 8192 MiB correction.

First failure frontier: `normal014 Playwright child exit: 1`; the required `three-products-summary.json` was absent. Browser assertions were not reached. Therefore the original manual ADD title/body and all required original raw/order/opaque/404/ADD/lostACK/restart/retry/undo/zeroLegacy checks are unreached and must not be treated as passing. Trace, error-context, and request/response/console summary artifacts are also absent because the browser stage was not reached.

Fresh retained evidence is under:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-build-heap-corrected-one-central-1145/record/evidence-central-corrected/run/`

The source/hash manifest is `sourceHASH-manifest.txt`; central log and summary hashes are `3467685311347af866c59aba9ae25fb4b57cc79498a3893af1506ac9df4443e5` and `c71bb8228c1947483ba0b04388b9c9501602ab2833bcb6ae7226ec693bbde6fa`. The central result directory is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-parent-build-heap-corrected-one-central-1145-ap2-m2-parent-build-heap-corrected-one-central-1145-e2e-integration-1021114743-590/`

## Resources and next step

After cleanup, latest observed free disk was `13,488,604 KiB` on both `/tmp` and `/home/user/work`, above the 10 GiB floor. Cgroup memory files were unavailable; no heavy peer process was present. Shared dependencies were not modified or reinstalled. The central setup and build succeeded; the remaining issue is the Playwright child failure before browser evidence. Diagnose that failure in a separate decision; this assignment made no second attempt.
