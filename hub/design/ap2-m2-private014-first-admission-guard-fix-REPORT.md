# Private014 first admission guard: verified fixture defect and bounded fix

## Result

The selected Gate 5 case starts a fresh **neutral Runtime**, then waits for a durable command owner before enabling the Astrid authoring profile. That order cannot admit this seeded legacy publication. Its immutable revision exists, but `parent_composition_heads.publication_id` is NULL and the public commit-history read returns **409 `history_unavailable`**. A healthy door/handshake and matching generated schema do not establish a verified authoring baseline.

Fixed only the App-owned journey fixture: `openCommandTimeline` now awaits the existing `harness.enableTimelineAuthoring(ASTRID_PYTHON)` before inspecting/opening the page. The helper is already idempotent and already performs the intended Runtime restart with `--authoring-profile astrid`. The Runtime's existing startup verifier installs the original publication identity. No accepted revision or publication is invented by the test.

The main-suite regression executes the actual registered Gate 5 and dependency-conflict callbacks with a fresh fixture, stopping at navigation. It proves both request authoring first and that failed authoring startup prevents navigation. It failed before the source change and passes afterward.

**This is a verified first-admission fixture repair, not a Gate 5 pass.** No central/browser rerun was requested: the brief requires the new harness source to be committed first, and this worker cannot commit. A later reset-gesture assumption also needs source review before selecting Gate 5 alone again (below).

## Exact source and authority

- App base: `8cfcee9c0403d113463c7859f6c835d3bfd79668`, tree `d44bc9c76eee46f34de77e1ef1ee87e7fe347518`.
- Agent: `3c4f6de4fa777323b3386c01c7266b619b86af6d`, tree `aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c`.
- Runtime: `202074110717146fc7f08af2306a8dd7f695b0b1`, tree `ee39286bd0eb27d4075074cc4785d6d15e33f243`.
- Producer: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`; ancestry independently rechecked.
- Artifact version: `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`.
- All 75 Runtime artifact bytes independently compared to producer a0 and their manifest hashes.
- Manifest SHA-256: `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`.
- Agent/Runtime edit-command schema bytes equal; SHA-256 `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Effective private App metadata: **0.2.14**, wire digest `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
- Private generated client SHA-256: `c422ce38279e6df9eb93c5b53993d57e68339b0807d34ed69d85b2408ed98be2`; metadata SHA-256 `9b3b8723a8d86a78d57bf83f43eb82914d1d0cd81ae89ebdf993b1560ddc57dd`.
- Locked graph archive unchanged: `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`; effective Composition package remains 0.0.13. That graph does not supply App's relative `./generated.ts` / `./generated-contract-metadata.ts` imports.
- Approved recovery files unchanged: `useTimelineSave.ts` blob `875073964dfe7db945fbbc66e6944ba79f8772ec`; recovery-test blob `a8fc03b984f081055c9162e960bdbcb36e1c8e2c`.

No source-floor movement, 357 mixing, public lock/pin/adoption, release, renderer requirement, new DTO/store/endpoint, forceReady, timeout adjustment, or identity/authority/draft/epoch guard change.

## Verified first-failure trace

The native probe imports exact archived Runtime202 and Agent3c4 code through PYTHONPATH, using the shared venv only for dependencies. It creates a disposable realm through the existing service/store APIs, publishes a minimal ordinary composition through the same public publication method as the browser harness, captures actual service health/handshake/history/immutable-parent responses, closes the neutral service, reopens it, and loads/registers the real existing Astrid provider. It does not patch Runtime or Agent code or insert history directly.

The private App probe mounts the real `RuntimeDataProvider`, generated `WorkspaceClient`, `useTimelineSave`, `usePollSync`, `useTimelineCommit`, command session, and outbox. Only transport delivery, IndexedDB and browser lock scheduling are adapters. The command-session wrapper records the readiness argument and calls the real hook. RuntimeHandler normally adds daemon.instance_id to health; the socketless transport supplies a labelled offline instance ID for that field. It does not purport to be a live daemon launch.

| Guard/state | Neutral fixture | Existing Astrid startup |
|---|---|---|
| Health | `ok` | `ok` |
| Handshake | correct 014 digest, actor, realm, exact product scopes and targeted-execution capability | same admitted authority |
| Effective generated metadata | imported `CONTRACT_VERSION === 0.2.14`; accepted real native 014 handshake | same |
| Effective generated history method | spy verifies actual `WorkspaceClient.prototype.listTimelineCommits` invocation with project/timeline/limit | same |
| Native commands enabled | true | true |
| Initial recovery check | true (real cold adoption/check completed) | true |
| Raw bundle | absent/null | unchanged |
| Immutable revision | `seed-r1` | same `seed-r1` |
| Display publication | NULL | original publication receipt `txn-1ec4b129ad9546c0aba1ee1e7b3c5c4f` |
| Public history | **409 refused: `history_unavailable`** | 200; one verified legacy entry and pinned head |
| Verified command basis | blocked before parent read | constructed from pinned immutable parent |
| Command state | `error`, `conflict: history_unavailable` | `saved`, no error |
| Durable owner / lease | 0 / 0 | 1 / 1 |
| Writes/rendering from App initialization | none | none |

Neutral calls stop at health, handshake, realm and `/commits?limit=50`. No immutable-basis read or owner lease occurs. Authoring proceeds through `/composition-revisions/seed-r1`, projects an accepted head and exposes the capture port. The actor and realm agree in both captures; only baseline installation enables history. This is runtime-tested effective-module evidence, beyond artifact inspection.

The previous central run's disposable trace was deleted by its runner, so these are **fresh socketless traces**, not recovered historical browser telemetry. The probe uses a minimal composition without the full Gate 5 media/shot closure; it establishes the baseline/profile admission defect, not full-cohort gesture qualification or exclusion of every other initialization race.

## Source path explaining the defect

1. `DirectHarness.start()` starts neutral Runtime and seeds main's public composition API.
2. `seedThreeProducts` adds its publication before authoring startup.
3. Standalone `M2 real gate 5` called `openCommandTimeline` immediately. Its first `enableTimelineAuthoring` was inside `prepareAfterAckLossMoves`, reached only **after** owner readiness and reset.
4. Earlier serial cases enable authoring. Running the whole serial file can hide this missing prerequisite; selecting only Gate 5 cannot inherit it.
5. Runtime202 `publish_parent_composition` deliberately leaves `publication_id=NULL` for an untracked legacy publication. `register_timeline_commit_provider` installs only a verified baseline. A neutral `list_timeline_commits` cannot fabricate that baseline and refuses with `history_unavailable`.
6. App `loadTimelineCommandBasis` begins with public history; the refusal prevents owner creation. App correctly preserves its authority guard.

## Changed files

- `tests/e2e/local/three-products.spec.ts`: await existing authoring setup at the shared command-timeline opening boundary, with one explanatory comment.
- `src/test/threeProductsAuthoring.test.ts`: three focused main-suite cases; both real standalone journey entrypoints establish authoring before navigation, and an authoring refusal stops navigation. No live fixture, credential, server, browser or socket is launched by this regression. Temporary dummy credential files are removed after each test.

No old initialization source was edited, so no foreign initialization proposal or owner-side merge of an old seam is needed for this repair.

## Commands and results

Worker root `W` below is the absolute directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-private014-first-admission-guard-fix`.

### Native reproduction

```sh
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH="$W/sources/runtime:$W/sources/runtime/packages/python:$W/sources/agent" \
/home/user/work/venv-app2-native/bin/python "$W/native-probe.py"
```

PASS: healthy neutral fixture has head revision + NULL publication and 409 history; real Astrid startup preserves the revision and installs its original receipt, then history is 200. Source directories were extracted with `git archive` at the exact immutable SHAs, with no checkout/commit/ref mutation.

### Main-suite focused regression

```sh
node --require "$W/vitest-runner.cjs" node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism src/test/threeProductsAuthoring.test.ts
```

- Before fix: **3 failed**, specifically no authoring call before navigation and startup refusal not observed.
- After fix: **3 passed**. Final unit-shim refactor was rechecked with the same command: **3 passed**, 2.55 seconds.

### Exact private014 targeted run

The worker's `offline-app-probe.sh` originally invoked this exact selection:

```sh
bash "$W/offline-app-probe.sh" \
  src/test/native014Admission.test.tsx src/test/threeProductsAuthoring.test.ts \
  src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts \
  src/integrations/runtime/timelineCommit.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx \
  src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
```

PASS: **9 files / 137 tests**, 26.20 seconds. The first invocation had this selection inline; the retained script accepts it as arguments. It copies the App only into this worktree's `.private014-admission`, verifies/copies exact generated014 producer bytes into that private copy, runs local vendor-lock checking, links the immutable locked graph, and runs Vitest with `--configLoader=runner --no-cache`. Its EXIT trap removes the copy. The installed graph and native venv remain read-only.

A second **diagnostic-only** invocation recorded the two complete App traces without rerunning the other suites:

```sh
bash "$W/offline-app-probe.sh" src/test/native014Admission.test.tsx --reporter verbose
```

PASS: **2 tests**, 4.52 seconds. Neither is a browser test.

### Lint and whitespace

```sh
node node_modules/eslint/bin/eslint.js \
  src/test/threeProductsAuthoring.test.ts tests/e2e/local/three-products.spec.ts \
  --no-cache --max-warnings 0
git diff --check
```

Both PASS. No full suite, project-wide typecheck, central request, localhost, browser, live socket, new Chromium smoke, or complete Gate 5 was run. The prior central Chromium PASS is historical context only.

## Remaining source observation and next steps

Gate 5 still contains a setup reset drag hard-coded as **5 -> 0**, while `seedThreeProducts` creates that clip at **0**. The reset helper calibrates scale from the supplied `from`, so this also assumes serial predecessor state. The same block appears in the dependency-conflict case. This is later than the first admission failure, and was not exercised by the admission-only probes. Do not infer that the selected full journey will pass solely from this fix.

App owner/orchestrator should first commit/review this bounded admission-fixture repair, then reconcile that reset prerequisite with both fresh and serial head state before authorizing the single fresh exact014 central Gate 5. Keep original gesture/ACK-loss/retry/undo assertions and all authority/source guards. No blind retry is justified by this report, and no claim is made about recovery/outbox end-to-end qualification.

No blocker remains for the bounded first-admission fix. Browser qualification and the later reset prerequisite remain outside the evidence claimed here.

## Portable evidence

All small artifacts are flat files next to this report, prefixed `ap2-m2-private014-first-admission-guard-fix-`:

- `native-admission.json`: actual exact-source service responses.
- `neutral-app-trace.json`, `authoring-app-trace.json`: full mounted App status/call traces.
- `authoring-red.log`, `authoring-green.log`, `private014-targeted.log`, `private014-trace.log`.
- `native-probe.py`, `native014Admission.test.tsx`, `offline-app-probe.sh`, `vitest-runner.cjs`: private reproduction sources; scripts use the worker root above and require the exact archived source directories described here.

Only the requested worktree and this worker's own orchestrator paths were written. No shared dependency/cache, integration checkout, foreign worker worktree, branch/ref, public pin or old App initialization seam was changed. The private App copy was verified absent after both runs. No archive, environment or dependency tree was copied into design/.
