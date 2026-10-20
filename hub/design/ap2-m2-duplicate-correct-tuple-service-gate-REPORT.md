# App duplicate central gate report

## Result

The duplicate gate is **inconclusive / blocked by the test harness**, not a
candidate product failure. The one actual central request was submitted and
was not rerun.

- Candidate App commit: `9caf57adbc07d046b9b10d1bed356526e88f56c3`
- Candidate App tree: `0800de89eac152136380f3031c6447f538e6c145`
- Agent pin: `8130a401bf44a518d5a40ae274d398b8c560be55`
- Runtime pin: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Runtime tree: `7ab412cc4bcbe517efcfa806e092336390312e18`
- Composition: public `0.0.13`
- No `DELETED` claim is made.

## Central evidence

Preflight passed:

`ap2-m2-duplicate-correct-tuple-service-gate-e2e-m2-duplicate-public13-preflight-1020200607-32286`

Command:

```text
env PRELIGHT_ONLY=1 sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-public13-environment-preflight-only/public13-integration-runner.sh "$PWD" duplicate
```

Result: exit 0; Agent, exact Runtime, Composition 0.0.13, Python, Node/npm,
Chromium and duplicate-test selector preflight passed.

The one actual request was:

`ap2-m2-duplicate-correct-tuple-service-gate-e2e-m2-duplicate-public13-integration-1020200640-27314`

Command:

```text
env PRELIGHT_ONLY=0 sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-public13-environment-preflight-only/public13-integration-runner.sh "$PWD" duplicate
```

Result: exit 1 before Runtime/browser journey execution. First failure:

```text
src/tools/video-editor/compositions/playerEvaluation.ts (3:2):
"clipOpacity" is not exported by
"../../app/node_modules/@banodoco/timeline-composition/dist/evaluation.js"
```

The reused runner creates a private public13 graph but does not attach it to
the App snapshot's `node_modules`. The failed build therefore resolved the
shared App install (`@banodoco/timeline-composition` 0.0.8), whereas the locked
graph preflight verified 0.0.13 and its `clipOpacity` export. This is a
runner/package-resolution failure; the duplicate source and journey did not
execute.

The prior ordinary public13 actual-gate log shows the same Composition export
failure, so this is baseline provider infrastructure rather than a duplicate
candidate regression. No provider-neighbor targeted rerun was necessary for
candidate acceptance after the harness failed before product execution.

## Source and local checks

- Existing committed duplicate cut was preserved; no App product source or
  authoring fixture was changed.
- Added only named service entries in `scratchpad/orch/tests/suites.conf` for
  duplicate public13 preflight and integration; the stale
  `e2e-m2-duplicate-three-products` wrapper was not run or altered.
- Predecessor evidence retained: native duplicate assertions and the real
  journey source are already in the candidate; no production
  `duplicateIndependentShot` references remain.
- Worktree remained clean at the candidate SHA/tree.

## Recommended next step

Repair or use the existing effective-build runner that attaches the private
public13 graph to the snapshot and verifies its resolver, then submit one new
central duplicate gate against the same candidate (or its qualified merge
SHA). Do not treat this request as product qualification or mark the deletion
ledger row `DELETED` until that corrected gate passes.
