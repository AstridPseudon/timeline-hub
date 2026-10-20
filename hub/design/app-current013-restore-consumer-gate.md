# Current013 App restore consumer HTTP gate

**PASS, bounded HTTP integration only.** One new literal named central suite was registered and requested exactly once. **1 test file / 2 tests passed, exit 0**, with the normal actual Runtime provider/server fixture. No fixture block, failure, skip, expected-failure change, or retry occurred. No product, test, configuration, generated client, package, lock, assertion or fixture source changed. This does **not** qualify UI, the root release, a browser journey, or the full project.

## Exact source and dependency identity

| Source | Read-only source path | HEAD | TREE |
| --- | --- | --- | --- |
| App | `/home/user/work/wt/app-m3-current013-restore-consumer-gate` | `cee68b807017efc8669c7d75318cf51aa70ec855` | `b2c510ca8893c4d3c238fb042f9ec7e7252edbc0` |
| Agent | `/home/user/work/wt/app-m3-agent013-current-pair-source` | `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` | `75354d38c898729bac09619679f5421faba319ed` |
| Runtime/server/producer | `/home/user/work/wt/app-m3-runtime013-producer-source` | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` | `7ab412cc4bcbe517efcfa806e092336390312e18` |

All three sources were clean and exact at start and end. The central service's actual snapshot TREE was also exactly `b2c510ca8893c4d3c238fb042f9ec7e7252edbc0` (`result/snap`). No moving integration checkout, historical pair or alternate Runtime server was used. Existing venv entry points were preserved literally: `/home/user/work/venv-agent/bin/python` and `/home/user/work/venv-runtime/bin/python`; no executable realpath substitution or venv write.

Read PLAN first, the prior `app-current013-paired-gate-executor.md`, current normal Agent/Runtime keeper and producer/pin docs, and final cold-source/typecheck report. The manager expressly authorized this narrower no-browser lane independently of the held label-policy review. Previous typecheck evidence was read, not rerun or extended to UI approval.

The unchanged existing `checkCurrent013Sources` preflight passed both producer-backed vendor checks and metadata/pins at both boundaries. The small notes-only read-only audit independently checked all **75/75** Runtime artifact bytes against both their manifest hashes and committed bytes, and **13/13 App + 15/15 Agent** normal lock destinations against the same producer.

- Normal contract/client: **0.2.13**.
- Schema: `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`.
- Artifact: `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`.
- Component manifest: `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`.
- Raw Runtime artifact manifest: `sha256:129abdbbf1f877643618b5290b39a5dd9225ba95b4c8fe8f2bb005ea4cf85497`.
- Public Composition **0.0.12** archive in both consumers: `sha256:0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.
- Own snapshot helper verified all **77 unique safe regular archive files**, exact installed file set and byte equality in read-only `/tmp/app-coherent-deps12/node_modules`, plus **React 18.3.1 / React DOM 18.3.1 / Remotion 4.0.509 / Player 4.0.509**. It was copied from the prior executor with only this worker's allowed `.test-*` prefix and exact App TREE changed.

Only the central service snapshot's ignored `node_modules` symlink was redirected to private12. The original worktree's link still points to `/home/user/work/app/node_modules`. No shared dependency, venv, source or shared cache was written. Existing `.vite` and `.vite-temp` cache file hashes/metadata were read at both boundaries under both shared dependency roots; those records compare byte-equal. This is scoped cache verification, not a full dependency-tree census.

## Actual central run and exact commands

**Gate TestID:** `app-m3-current013-restore-consumer-gate-restore-current013-ad8749a9ce12a699672faf3ad96b4e4cbea9245c2-tb2c510ca8893c4d3c238fb042f9ec7e7252edbc0-integration-1020130731-30085`  
**Result directory:** [app-m3-current013-restore-consumer-gate-restore-current013-ad8749a9ce12a699672faf3ad96b4e4cbea9245c2-tb2c510ca8893c4d3c238fb042f9ec7e7252edbc0-integration-1020130731-30085](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-current013-restore-consumer-gate-restore-current013-ad8749a9ce12a699672faf3ad96b4e4cbea9245c2-tb2c510ca8893c4d3c238fb042f9ec7e7252edbc0-integration-1020130731-30085)  
**Full log:** [log.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-current013-restore-consumer-gate-restore-current013-ad8749a9ce12a699672faf3ad96b4e4cbea9245c2-tb2c510ca8893c4d3c238fb042f9ec7e7252edbc0-integration-1020130731-30085/log.txt)  
**Result:** service PASS / exit **0** / **28 seconds**; Vitest **4.1.5**, **2 passed / 0 failed**, **21.94 seconds** (18.73 seconds in tests), start **2026-10-20 13:07:47 UTC**. Fresh run: no `cached_from`, no resubmission or automatic retry. Cache key: `5545c12ce683750340b14a5fd536dc13`.

The one appended registration is preserved verbatim in `notes/suite-line.txt`; no existing suite or central bin was changed. Every external source/venv binding and the full source/helper cache identity is literal in this command; caller exports were not assumed by request-test:

```text
app restore-current013-ad8749a9ce12a699672faf3ad96b4e4cbea9245c2-tb2c510ca8893c4d3c238fb042f9ec7e7252edbc0-integration flock -w 600 /home/user/work/.app-m1-browser.lock env TIMELINE_CURRENT013_APP_TREE=b2c510ca8893c4d3c238fb042f9ec7e7252edbc0 TIMELINE_CURRENT013_AGENT_SHA=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source ASTRID_CHECKOUT=/home/user/work/wt/app-m3-agent013-current-pair-source ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python TIMELINE_BUNDLE_AGENT_HEAD=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a PYTHONDONTWRITEBYTECODE=1 NODE_OPTIONS=--max-old-space-size=4096 TIMELINE_CURRENT013_CACHE_ID=appcee68b807017efc8669c7d75318cf51aa70ec855-treeb2c510ca8893c4d3c238fb042f9ec7e7252edbc0-agentd8749a9ce12a699672faf3ad96b4e4cbea9245c2-tree75354d38c898729bac09619679f5421faba319ed-runtime2c4ac180c2220bdad966bc01e95ad230e99ce26a-tree7ab412cc4bcbe517efcfa806e092336390312e18-public12-0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3-helper9540174728710a5d4e31001075f52f71831106a7f3c03ee4f31cb53cb65285bb-runner0daeb21ac4d45549eba497d86161436e454643046a3f08811267a912047355fb-audit916f2d310bb3001d6d5b6ad05b1f4a3a6281b775c50094a2335913f4e5da2e8f-preloadf303229cd36c7878c739cad7e7669e3bf66ee416bd927434aca1addeab059f52 bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-restore-consumer-gate/notes/run-lane.sh
```

Exactly one request was made (stdout retained in `notes/result-dir.txt`), followed by waits on that same result:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-m3-current013-restore-consumer-gate restore-current013-ad8749a9ce12a699672faf3ad96b4e4cbea9245c2-tb2c510ca8893c4d3c238fb042f9ec7e7252edbc0-integration > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-restore-consumer-gate/notes/result-dir.txt
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-m3-current013-restore-consumer-gate-restore-current013-ad8749a9ce12a699672faf3ad96b4e4cbea9245c2-tb2c510ca8893c4d3c238fb042f9ec7e7252edbc0-integration-1020130731-30085 1
```

The waiter was polled and the same completed result was read again; there was no second request. The central notes runner imports the **unchanged** `config/testing/vitest.runtime-restore.integration.config.ts` into an external snapshot-bound config that changes only `cacheDir`. Exact test argv, executed by the central service only:

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-restore-consumer-gate/notes/runs/.test-app-m3-current013-restore-consumer-gate-restore-current013-ad8749a9ce12a699672faf3ad96b4e4cbea9245c2-tb2c510ca8893c4d3c238fb042f9ec7e7252edbc0-integration-1020130731-30085/restore.config.ts --configLoader=runner --no-cache --maxWorkers=1
```

The existing preload binds `__dirname` to the central snapshot's `config/testing`; no mocks or source overrides. `TMPDIR`, npm cache, and Vite cache are private beneath this worker's run folder. Those temporary/cache folders were removed after the run. No browser/build/install was invoked. The normal `DirectHarness` HTTPS origin and Runtime door/daemon sockets ran only in the central service; no dist override or fake publication guard was supplied.

Local read-only verification commands (all exit 0; run from the exact assigned worktree):

```sh
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-restore-consumer-gate/notes/audit.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-restore-consumer-gate/notes/source-start.json
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-restore-consumer-gate/notes/audit.py --caches > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-restore-consumer-gate/notes/cache-start.json
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-restore-consumer-gate/notes/central-private12-snapshot.py --verify-only
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-restore-consumer-gate/notes/run-lane.sh
env TIMELINE_CURRENT013_APP_TREE=b2c510ca8893c4d3c238fb042f9ec7e7252edbc0 TIMELINE_CURRENT013_AGENT_SHA=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source ASTRID_CHECKOUT=/home/user/work/wt/app-m3-agent013-current-pair-source ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python TIMELINE_BUNDLE_AGENT_HEAD=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a PYTHONDONTWRITEBYTECODE=1 NODE_OPTIONS=--max-old-space-size=4096 TIMELINE_CURRENT013_CACHE_ID=appcee68b807017efc8669c7d75318cf51aa70ec855-treeb2c510ca8893c4d3c238fb042f9ec7e7252edbc0-agentd8749a9ce12a699672faf3ad96b4e4cbea9245c2-tree75354d38c898729bac09619679f5421faba319ed-runtime2c4ac180c2220bdad966bc01e95ad230e99ce26a-tree7ab412cc4bcbe517efcfa806e092336390312e18-public12-0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3-helper9540174728710a5d4e31001075f52f71831106a7f3c03ee4f31cb53cb65285bb-runner0daeb21ac4d45549eba497d86161436e454643046a3f08811267a912047355fb-audit916f2d310bb3001d6d5b6ad05b1f4a3a6281b775c50094a2335913f4e5da2e8f-preloadf303229cd36c7878c739cad7e7669e3bf66ee416bd927434aca1addeab059f52 node --input-type=module -e 'import {checkCurrent013Sources,readCurrent013Inputs} from "./scripts/testing/current013-integration.mjs"; console.log(JSON.stringify(checkCurrent013Sources(readCurrent013Inputs()),null,2));'
git diff --check
git status --short
```

The audit, cache and wrapper checks were repeated into `source-end.json`, `cache-end.json`, and `pair-end.json`; all three start/end pairs compare byte-equal. The central runner independently repeated its own source/dependency and cache checks in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-restore-consumer-gate/notes/runs/.test-app-m3-current013-restore-consumer-gate-restore-current013-ad8749a9ce12a699672faf3ad96b4e4cbea9245c2-tb2c510ca8893c4d3c238fb042f9ec7e7252edbc0-integration-1020130731-30085` even after test completion; these also compare byte-equal. `notes/pair-start.json` and `pair-end.json` include successful normal producer-backed vendor-check output. The local helper verification did not relink the original worktree.

## Behaviors actually passed

1. **`M1 App restoreHistory uses the actual head pair and preserves the exact immutable closure through the Runtime door`.** Real fixture seed, real Agent intervening move, actual App `RuntimeDataProvider.restoreHistory`, GET timeline + health then restore POST, exact current revision/publication pair in request, accepted original revision with a distinct publication receipt, exact canonical closure returned, fresh-provider readback of parent/shot/internal immutable revisions, history receipt, and both opaque config/clip values. Route ordering and POST traffic assertions are unchanged.
2. **`ShotEditor reads, edits and saves Runtime-valid raw settings without changing unrelated immutable payload data`.** The original absent/null/scalar/array/object loops passed: neutral save, rename, prompt save or visible safe refusal, immutable previous closure, unrelated opaque data including special JSON keys, malformed known-field rejection, and tracked-head 409 refusal retaining the pending draft. No acceptance expectation was removed or weakened.

Inspected the fixture before execution: `DirectHarness.start()` calls `seedRuntime()`, followed by `seedThreeProducts()`, through the existing composition-revisions route before enabling timeline authoring. This route was accepted for those original seed writes on the exact current pair; the feared pre-consumer retired-writer failure did **not** occur. No fixture bypass, safety-guard weakening, raw publication substitute, historical-pair fallback or alternate API was introduced.

## Decisions, limits and handoff

No settled decision was changed and no evidence requiring a plan deviation was found. Used the complete existing restore config/file (both original tests) so the neighboring raw preservation assertions remained part of this one authorized lane. Used an integration-named suite with explicit literal identities so its command participates in service cache identity; used private cache paths to protect shared dependencies.

**Not run / not claimed:** source-worker localhost sockets; browser/UI or cold-label execution; M1 seven-case or Gate5 adversarial browser journey; build; project tsc; install; full suite; capture/export/render/frame/audio parity; owner-film or macOS qualification. This HTTP result does not release the independently held label/root UI review or establish complete project readiness.

No blocker for this bounded task. Recommended next step: manager may record this exact restore consumer pass and continue the separate label-policy review and explicitly authorized remaining gates on their own exact source trees. Do not rerun this lane on unchanged source merely to broaden its claim.

Artifacts: this report in requested local `design/`, ORCH `design/`, and worker `report.md`; notes retain the literal suite and boundary records. Product/test tracked diff is empty; no Git commit/merge/rebase/checkout/push was run. Conventional commit message supplied. `DONE` created after completion; no `BLOCKED`, no retained `KEEP`, no running test or worktree build/temp output.
