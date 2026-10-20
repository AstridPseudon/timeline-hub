# Requester final boundary fences — source complete, activation inactive

2026-10-20. Worker `app-m2-requester-final-boundary-fences`, worktree `/home/user/work/wt/app-m2-requester-final-boundary-fences`, branch `tl/app-m2-requester-final-boundary-fences`. Base **eaabdd8f8e30e36f432dc11bc99da2dba3f076bf** (`tl/app-m2-continuation-fence-compose`). Read PLAN first, then the exact retained independent review source/tests and its final report. No settled decision changed. This is a local source repair; **no real Runtime acceptance or production activation is claimed**.

The fix adds **34 net authored product lines** (51 added / 17 removed) across `commitOutbox.ts` and `placementRequester.ts`. The only other repository change is permanent requester tests. No generated client, wire DTO, endpoint, queue, store/journal, timer, coordinator, dependency, lockfile, editor pin, UI activation or writer retirement changed.

## Behavior and local seam

- The existing exclusive claim exposes `assertActive()`, reading the same in-memory lifetime flag set false in the existing claim `finally`. It runs directly beside task POST and the capture/transmit callback invocation, with no further await before invoking them. The generation-checked disk reads and existing owner lock remain in use; the flag does not pretend to synchronously read disk generations.
- Async authenticated identity discovery remains. Its actor/realm snapshot is checked against the saved original scope, followed by the existing generation-checked read and a synchronous live-host assertion. That assertion repeats at the actual callback boundary, closing promise propagation after the helper returns.
- Existing outbox placement methods and `dispatch` accept an optional synchronous assertion. They execute it **inside** their existing generation-checked IDB mutation handler, covering approval reservation, task locator, immutable pin, capture linkage/refusal, pending reservation, commit ACK pruning and permanent rejection. Lifecycle interruption escapes the capture-error catch. No accepted result or permanent refusal may consume work under another identity.
- Preserve the original uncertain request body/key, original approval/read closure/pin/created IDs and dependent B/C/inverse guards. A lifecycle interruption of a transmission retains the existing retry classification (`transport_error`) and exact pending request. Retry bookkeeping can be recorded under the same live owner even when authenticated identity is unavailable: it never consumes an intent, links acceptance, or creates permanent conflict. This deliberately preserves all existing passing retry assertions.

**Missing host binding stays inactive and explicit.** The generated `WorkspaceClient` offers no synchronous authenticated lifecycle. `AstridRuntimeClient` has async `ensureSession`/`reconnect`/`getRecoverableIdentity` and a synchronous `assertNotFenced`, but its cached handshake and observed restart fence cannot establish that the connector's currently authenticated actor/realm has not changed. Supabase's unrelated auth listener is not Runtime authority. Therefore no cached identity is promoted to synchronous authority, and no production client/auth code was changed.

The smallest local seam is the requester client's optional **`isCurrentIdentity(expected: { realmId, actorId }): boolean`** port. The authenticated host adapter must check its own current authenticated lifecycle, including invalidation/reconnect, and return literal `true` synchronously; it must belong to the same binding used by the operation callbacks. Missing port throws `Authenticated requester identity lifecycle binding is unavailable` before reservation or task dispatch; recovery reports retry explicitly. False, thrown errors (including API-shaped auth failures), and promises are lifecycle interruptions, not semantic refusals. The fixtures alone bind this port to their actual mutable identity. A separate control proves host invalidation blocks ACK consumption even when actor/realm strings remain unchanged. A future real host binding is still required for activation; a field-equality check over a cached handshake would not satisfy it.

## Permanent tests and preservation

Imported all **16** retained review cases into the existing requester test file, sharing the single original fixture: 12 actor/realm × task POST/capture success/capture failure/ACK/rejection/API refusal cases, one real promise-reaction lock-release POST case, and three lock-release mutation controls. Every safety expectation remains an ordinary passing test on the repair. The reviewer tests also asserted the *observed buggy recovery* (e.g. no retry after wrong-identity ACK pruning); those external RED-only diagnostic assertions now expect the required original-identity replay/recapture instead. No previously passing repository behavior was rewritten. All four handoff test statements are byte-exact and occur once.

Added seven further test cases: two parameterized field cases each exercise six actual IDB get-success mutation boundaries; two promise-reaction controls prevent capture/transmit callback invocation after owner release; missing-binding and async-binding refusal controls; and unchanged-identity host invalidation with original-identity recovery. The fixture adds a synchronous live identity check and an optional before-write fault hook in its existing fake-IDB rollback adapter. No second fixture/storage/acceptance implementation is introduced.

The AST audit preserves every inherited complete `it` statement at its original multiplicity: **176 statements / 360 composition tests**, **164 statements / 339 base tests**, and **89 statements / 145 fence tests** (the cohorts overlap; they are not duplicated). The other six complete test/fixture files are byte-identical to the base. The five inherited combined A/B/C/inverse recovery cases still run, including exact pending replay and duplicate completion after each later ACK/inverse. No source `skip`, `fails`, or `todo` annotation was introduced.

## Exact commands and evidence

All commands below ran in `/home/user/work/wt/app-m2-requester-final-boundary-fences`. Define:

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-requester-final-boundary-fences
V=node_modules/vitest/vitest.mjs
```

Initial RED before production edits, after importing the 16 review cases:

```sh
node --require "$W/notes/runner-paths.cjs" "$V" run --config "$W/notes/focused.config.ts" --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/placementRequester.test.ts > "$W/notes/red.log" 2>&1
```

**Exit 1: 13 failed / 73 passed, 86 tests, 1.64s, 08:42:17 UTC.** No setup/collection failures. The unchanged product was exactly base `eaabdd8f8`.

A reproducible second RED uses the **final permanent test source** and exact base product modules copied with `git show` into `notes/baseline`. The notes-only `red.config.ts` maps the two relative imports to those retained files; no product source is overwritten:

```sh
node --require "$W/notes/runner-paths.cjs" "$V" run --config "$W/notes/red.config.ts" --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/placementRequester.test.ts -t 'independent residual fence counterexamples|independent claim and microtask handoffs' > "$W/notes/red-final-source.log" 2>&1
```

**Exit 1: the same 13 failures / 3 passing controls, 1.37s, 08:46:42 UTC.** The CLI name filter leaves 77 unrelated tests unselected (Vitest prints them as skipped); no source tests are skipped/disabled. The RED log includes actual POST entry with claim callback returned and lock released, and identity changes during genuine successful final reads. The final GREEN below has no test-name filter.

Final focused suite:

```sh
node --require "$W/notes/runner-paths.cjs" "$V" run --config "$W/notes/focused.config.ts" --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/placementRequester.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/integrations/runtime/bootstrapInitialization.test.ts src/integrations/runtime/createDefaultTimeline.test.ts > "$W/notes/targeted.log" 2>&1
```

**PASS, exit 0: 7 files / 383 tests, 16.64s, 08:46:02 UTC.** This is 360 inherited + 16 review + 7 further cases. [Final log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-requester-final-boundary-fences/notes/targeted.log).

```sh
node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/commitOutbox.ts src/tools/video-editor/commands/placementRequester.ts src/tools/video-editor/commands/placementRequester.test.ts > "$W/notes/lint.log" 2>&1
node "$W/notes/audit.cjs" > "$W/notes/audit.log"
git diff --check
git status --porcelain=v1 --untracked-files=all
```

**All exit 0**. ESLint and whitespace are clean; audit has zero failures; status contains only the three intended tracked modifications. [Audit](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-requester-final-boundary-fences/notes/audit.json), [lint](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-requester-final-boundary-fences/notes/lint.log), [exact patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-requester-final-boundary-fences/notes/source.patch).

Intermediate runs, retained honestly: `first-green.log` used the same focused config/runner/flags with requester/outbox/session only, **217 passed / exit 0 / 9.99s**, 08:43:25 UTC. `boundary-tests.log` used requester only after adding the extra controls, **92 passed / 1 failed / exit 1 / 1.77s**, 08:45:08 UTC: the new missing-binding test accidentally omitted its fixture outbox injection, so its `recover()` reached unavailable global IDB. Fixed that new test's injection, kept the expected missing-binding behavior unchanged, then ran the final 383-test suite. No product workaround or weakened assertion was used.

## Exact source and isolation

| File | Base → final lines | Final SHA-256 |
| --- | --- | --- |
| `src/tools/video-editor/commands/commitOutbox.ts` | 583 → 600 | `3132ecfdb0b31f284c1a9e6ca4a0c919390992eb693ad542f4ca73366221ca98` |
| `src/tools/video-editor/commands/placementRequester.ts` | 277 → 294 | `b38a98fbc8aa8778012f0b3cae7210956429fc65d1969a6ee7b953911534d728` |

Repository binary patch SHA-256 relative to the base: **`4ebe22e6d9fb0d71291cd6ec20e7d524987183981b82334dab780758aa577c05`**. `notes/audit.json` records blob IDs and SHA-256 hashes for all seven test files, both product modules, generated/client source, config and package files, plus the exact retained review sources. No source edits occurred after the final GREEN.

The worker's own ignored `node_modules` symlink resolves to **`/tmp/app-coherent-deps12/node_modules`**, Composition **0.0.12**, Vitest **4.1.5**. Every shared dependency directory, runtime and venv stayed read-only, including `.vite` / `.vite-temp`. `--configLoader=runner` avoids bundled-loader temp writes; `--no-cache` disables result caching; notes-only config sets its explicit cache directory beneath this worker's notes. The preload supplies the original config's project-root `__dirname`. No install, shared package/cache/link edit, full suite, build, tsc, browser, socket/server, pin change or UI activation was run. No build/temp output remains in the worktree. No git commit/merge/rebase/checkout/push/ref mutation was performed.

## Decisions, limits and next step

Routine decisions: preserve the existing lock/generation and async discovery lifecycle; add a single local live-host boolean callback rather than treat cached identity as authority; run final assertions inside existing mutations; retain harmless uncertain retry classification required by inherited positives. No PLAN decision is contradicted. The known lack of a synchronous authenticated host lifecycle remains explicit; **do not activate or retire automatic writers based on these tests**.

No blocker prevents completion of this bounded source task. Activation remains blocked on a genuine authenticated host binding and its independent review, authoritative Agent automatic placement capture, approved producer preparation/same-store composition, and supported current-pair qualification. Native browser locks/durability, real Runtime task/commit acceptance/provenance, canonical reload, guarded actual undo/redo and zero legacy traffic remain **UNRUN**. The opaque fixture ACK/capture proves local storage/dispatch behavior only.

Recommended next step: independently review this exact patch, verify the host seam contract against the real connector lifecycle, then assign its minimal real binding and targeted integration qualification before reconsidering activation. Retain all original approval/pending replay/duplicate-completion expectations.

Artifacts: [design report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-requester-final-boundary-fences.md), [notes](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-requester-final-boundary-fences/notes), [report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-requester-final-boundary-fences/report.md), [commit message](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-requester-final-boundary-fences/commit-msg), [KEEP](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-requester-final-boundary-fences/KEEP), [DONE](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-requester-final-boundary-fences/DONE).
