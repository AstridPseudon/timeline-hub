# Runtime 0.2.13 App pin independent review

**APPROVE — bounded normal pin, 2026-10-20.** No blocking product issue found. This approves the reviewed pin diff; it does not establish coordinated consumer activation or completion of project gates.

Read PLAN.md, runtime-current-tuple.md and app-runtime013-root-normal-pin.md before reviewing. No settled decision was changed or contradicted by the evidence.

## Reviewed identity and scope

| Item | Exact identity |
| --- | --- |
| Review worktree | `/home/user/work/wt/app-m3-runtime013-pin-independent-review` |
| App HEAD | `171a259acbeb3ced855ca8f72fed0943a2f5a5cb` |
| App tree | `f33b5268678efe390a5732022d81b53f35ccf509` |
| Base | `0ea988bdd2907c876b82fd2620820e3fb6d6ea84` |
| Producer checkout, read-only | `/home/user/work/wt/app-m3-runtime013-producer-source` |
| Producer HEAD | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` |
| Producer tree | `7ab412cc4bcbe517efcfa806e092336390312e18` |
| Protocol / both client versions | `workspace.v1` / `0.2.13` |
| Schema | `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4` |
| Artifact version | `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56` |
| Raw artifact manifest SHA256 | `129abdbbf1f877643618b5290b39a5dd9225ba95b4c8fe8f2bb005ea4cf85497` |
| Binary diff SHA256 | `580f01c8add619dadd837c6518b8a3a94232290739ced563756dd8d6b58a933c` |

The diff is exactly four files, +29/-10: runtime.lock.json and the generated client, metadata and timeline DTO files. All other tracked paths equal base, including MAIN behavior, CORS, parity harness, public12 artifact/package locks, Agent public-boundary lock, editor clamp/supersession/label behavior and safety tests. The three existing `it.fails` markers in useClipDrag.test.tsx are byte-preserved. No new marker, handwritten type, caller or test change exists.

## Findings

- Independently checked all 75 manifest artifact hashes against producer working and committed bytes. Recomputed the artifact version from canonical sorted artifact-map JSON and checked the raw manifest hash. Producer HEAD/tree were asserted, and the producer checkout stayed clean.
- All 13 locked destinations equal producer working bytes, producer committed bytes, manifest hashes and lock hashes. Lock destinations and source mappings are unchanged. The lock is the prior lock with only the selected source, artifact version and generated-file hashes replaced. The nine response fixtures and timeline schema are unchanged.
- All 99 prior DTO names remain. The 19 added names, optional `OccurrenceAddMediaArgs.consumed`, exports and metadata are exact producer bytes. They introduce no App writer activation.
- The generated `createTimelineView` signature now requires options and an idempotency key and sends `Idempotency-Key`. Source inventory found no production `.createTimelineView(...)` caller. Runtime client scopes already include `projects:write`. This signature change therefore requires no App caller adaptation in this diff.
- Independently compared all 77 installed Composition files with the checked-in immutable public12 tarball, SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`. No mismatch. Composition files, six peer manifests and shared/private dependency cache metadata were unchanged across the local tests.

These checks establish preservation relative to the assigned base. They do not re-prove MAIN behavior, CORS, editor gestures or rendered parity by executing their suites.

## Commands and results

All local commands ran in the review worktree. Node v22.22.0, Vitest 4.1.5. Only this worktree's ignored node_modules symlink was redirected to `/tmp/app-coherent-deps12/node_modules`. Shared dependencies, runtimes and venvs were not modified. The notes config imports the repository config unchanged except for a worker-local cacheDir. The required snapshot preload supplies the config loader's `__dirname`; it does not mock Git or tests.

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
N="$O/workers/app-m3-runtime013-pin-independent-review/notes"
git rev-parse HEAD
git diff --stat 0ea988bdd2907c876b82fd2620820e3fb6d6ea84 HEAD
git diff 0ea988bdd2907c876b82fd2620820e3fb6d6ea84 HEAD
git -C /home/user/work/wt/app-m3-runtime013-producer-source rev-parse HEAD 'HEAD^{tree}'
git -C /home/user/work/wt/app-m3-runtime013-producer-source status --short
python3 -B "$N/review-audit.py" > "$N/source-audit.json"
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/app-m3-runtime013-producer-source
node scripts/vendor-lock.mjs check runtime.lock.json
git diff --check
git status --short
```

All checks exited 0; both worktrees were clean. The audit script asserts both source trees, and it and the complete per-destination hashes remain in worker notes.

One local narrow test invocation:

```sh
env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
  node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/compositions/vendoredTimelineCompositionAliases.test.ts \
  src/integrations/runtime/client.test.ts \
  src/integrations/runtime/vendorLock.test.ts \
  --reporter=default --reporter=json --outputFile.json="$N/narrow.json" \
  > "$N/narrow.log" 2>&1
```

Local result: **33 passed / 11 failed**, exit 1. Package suite: **6/6 passed**. Public Runtime client suite: **25/25 passed**, including current-digest acceptance, prior/mismatched digest refusal, restart fencing, credential scopes and mutation/read behavior. Vendor suite: 2 static tests passed; all 11 fixture-dependent tests failed at fixture `git init` with `spawnSync git EPERM`, before product assertions. No test was changed, weakened, mocked or retried locally.

Only after that fixture EPERM, requested the existing authorized central vendor suite:

```sh
"$O/bin/request-test" app-m3-runtime013-pin-independent-review vendor-lock-cachefree-integration
"$O/bin/wait-test" app-m3-runtime013-pin-independent-review-vendor-lock-cachefree-integration-1020115309-29608
```

**13/13 passed, exit 0**, on exact App tree `f33b5268678efe390a5732022d81b53f35ccf509`. Central command:

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs \
  node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 src/integrations/runtime/vendorLock.test.ts
```

Logs and summary are in `orch/tests/app-m3-runtime013-pin-independent-review-vendor-lock-cachefree-integration-1020115309-29608/`. Local logs, source audit and identical deps-before.json/deps-after.json are in the worker's notes. Fixture/cache scratch was removed; no build output or temporary files remain in the worktree. Unique passing behavioral coverage here is 44 tests across three files; the original local EPERM failures remain documented.

## Limits and next step

No product, pin or test was edited. No 2,055-test rerun, new full, tsc, build, browser, live socket/localhost, actual Runtime acceptance/reload/restart/undo, pixel/audio parity, owner-film or macOS qualification was run. No Agent matching pin was reviewed. The source pin report's Agent-pair and activation qualifications remain pending evidence outside this task.

No blocking issue or decision escalation. Recommend accepting this bounded App pin, then obtaining the matching Agent Runtime0.2.13/public12 SHA and running the separately authorized composed typecheck and current-tuple qualification. Existing owner field/opacity holds are unchanged. No KEEP requested or created.
