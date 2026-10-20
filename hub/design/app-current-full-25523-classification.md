# App current full 25523 classification

**Disposition: INPROGRESS. Do not treat this run as pass or fail.**

The central test service run
`app-full-current-standard8-m1-compat-integration-1020102149-25523` was
requested once for App integration source `7bb885b638838588a0dff81b64b7c34960ac07f3`
and snapshot tree `065b46ac13026d3e3a1d760b44bab1ab8e1e930e`. At the last
observation its status was `running`; no `summary` or `exit` file exists, and
the log has no Vitest terminal counts. Therefore the current run has no
classifiable finished failed nodes, collection delta, skip/unrun set, or
unhandled-error set yet.

The repeated React/jsdom error diagnostics in the live log are expected test
fixture output and are not classified as failures without the terminal Vitest
summary. The expected result remains zero actual failures, but that is not an
observed result.

## Classification state

| Category | Current classification |
| --- | --- |
| Finished failed nodes | Pending terminal summary; none claimable from the live log |
| Collection delta | Pending terminal summary |
| Authorized expected failures | Precheck found 3 markers and 0 forbidden markers; terminal expected-test count pending |
| Skipped/deselected | Pending terminal summary |
| Unrun files/tests | Pending terminal summary |
| Unhandled errors | Pending terminal summary |

The three authorized markers are unchanged `useClipDrag.test.tsx` cases at
lines 774, 1120, and 1230. No marker was added or weakened.

## Source and environment

The suite command is the central standard8 runner:

```sh
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/central-standard8-snapshot.py && \
env ASTRID_CHECKOUT=/home/user/work/wt/app-m1-full-agent-source \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m1-full-runtime-source \
NODE_OPTIONS=--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs \
npm test -- --configLoader=runner --no-cache --maxWorkers=2
```

The preparation log verifies the isolated `/tmp/app-m2-coherent-deps8/node_modules`
target, the Composition 0.0.8 archive with all 77 files matching, and the four
peer versions (React 18.3.1, React DOM 18.3.1, Remotion 4.0.509, and
`@remotion/player` 4.0.509). Only the test snapshot’s ignored `node_modules`
symlink was repointed; shared App dependencies and caches were not modified.

The explicit compatibility inputs are:

- Agent: `/home/user/work/wt/app-m1-full-agent-source`, commit
  `4a75f68f32049a69fd86135c645fa64c51175c14`.
- Runtime: `/home/user/work/wt/app-m1-full-runtime-source`, commit
  `4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136`.

Those paths and commits are historical-compatible safety inputs only. They do
not qualify the current Runtime, public-12 browser release, browser/e2e
journeys, renderer parity, or writer retirement. The run’s moving `ext` metadata
(`agent=e2ad59584addc892f1a6dd9fd644c75f80a2e28f`, `runtime=c0dcd3871d78c405184506eb6735565592498c77`,
`composition=e80c46baf5aa4b50a10b77a5ceadcb7ec4ab27ab`) is recorded but is not
used as environment qualification.

## Bounded CORS controls and prior comparison

The source diff from the current App integration parent to `7bb885b...` is
exactly these two modified files:

```text
src/shared/lib/media/mediaCrossOrigin.ts
src/shared/lib/media/mediaCrossOrigin.test.ts
```

It is 48 insertions and 6 deletions. The direct-control file adds two test
declarations: one seven-case parameterized preservation test and one HTTPS
gateway test. That is **+8 expanded test cases** (8 declarations/cases added
relative to the prior file’s expanded count), for 8 declarations total in the
file. The independent bounded command covered the helper and the two original
gateway regressions: **2 files, 23 tests passed, exit 0**, with no cache and one
worker. This is source/control evidence only; it does not replace the pending
full-run result.

The prior full 20880 run was historical-compatible only: 18,496 passed, 2
actual CORS failures, 3 authorized expected failures, 1,469 files, and exit 1.
Its two retained nodes were the unchanged
`HoverScrubVideo.gateway.test.tsx` poster/video CORS assertions. The new direct
controls are intended to remove those two failures, but the current full run
must reach its terminal summary before that can be classified as verified.

## Limits and next step

No duplicate full run was requested. No source, product, dependency, cache,
build, TypeScript, browser, socket, install, or test expectation was changed
by this classifier. No extra failure-proof targeted run was started because the
full run is not terminal. After the central service records `summary`, `exit`,
and final `status`, classify the exact failed nodes, collection delta,
expected/skip/unrun/unhandled counts, and only then decide whether any new
targeted proof is necessary.
