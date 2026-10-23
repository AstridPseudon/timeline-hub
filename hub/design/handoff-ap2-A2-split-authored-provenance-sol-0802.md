# A2 split/config authored provenance

Worker: ap2-A2-split-authored-provenance-sol-0802. Completed product change, 2026-10-23.
Base: `890b9561666c3619f69335dd747b15e042b3a9a3` on the assigned App worktree/branch.
Plan §3 A2 and `design/handoff-ap2-P1-first-split-conflict-sol-0747.md` read first.
No commit was run; the harness owns Commit A2.

## Change and causal decision

Exactly four tracked files:
- `src/tools/video-editor/lib/serialize.ts`
- `src/tools/video-editor/hooks/useTimelineCommit.ts`
- `src/tools/video-editor/hooks/clip-editing/useClipSplitting.ts`
- `src/tools/video-editor/hooks/useTimelineCommit.test.tsx`

The production path is `useClipSplitting -> useClipEditing.applyConfigEdit -> useTimelineCommit.applyEdit -> serializeResolvedTimelineEdit -> serializeForDisk -> buildDataFromCurrentRegistry -> assembleTimelineData -> scheduleSave -> useTimelineSave -> timelineLocalSaveHandoff.capture -> documentPatchIntent -> localSaveSession`.

The config branch now uses the existing editor-edit serializer and carries output through the registry rebuild. Strict disk serialization still omits output. The unchanged existing raw authoring handoff preserves raw output bytes when the loaded view is unchanged, including its absent/null/default distinctions; intentional output edits remain edits. No output change was reordered.

The label mapper binds raw and previous displayed clips by their existing exact IDs. It restores raw own-label presence/value only when the displayed label was unchanged; actual changed label values and new authored IDs pass through. It does not compare labels to filenames or infer source identity from ID prefixes. The split caller applies that mapping BEFORE the existing split helper copies/allocates the right row. This is necessary: once a copied display label has a new ID, the existing raw handoff correctly treats that new row as authored and cannot infer its source. All three existing split entry points use the mapping. No executor, capture port, schema, fixture or pin was added.

No other product path changed. In particular: no Agent/provider fix; no move/Undo/placement/popup/dataProvider edits; current paired-head/startup and exact durable retry remain on the base implementation. Remote queued work is not present on this base and must be preserved by the integration owner.

## Regression / RED and GREEN

The regression runs the real `useClipEditing` and `useTimelineCommit` hooks, event bus, handoff, patch emitter and persisted session/outbox. Only the transport is a mock; no HTTP call or browser is used. The clip literal retains the original P1 source ID, hold/from/to/speed, absent label and opaque/null/app namespaces, with nondefault raw `out.mp4`. Media is an offline deterministic registry entry, not a live P1 object/pin.

Before the source edit, the two initial cases (absent/authored label) failed: `out.mp4` became `output.mp4`. Log: `/tmp/w-674ebcc09c/red.log`. Afterward they passed; final coverage also includes an explicitly authored label equal to the media display name.

Assertions retain exact split-only changes: one guarded list.insert with the actually allocated right ID and original order, and one guarded source hold 8 -> 2. Both split rows preserve the original authored label state and original app data; no label appears on either absent-label row. All 13 D13 consulted reads are checked for exact paths/states/values/order. The same production caller then authors `intentional.mp4` and `Edited title`, which survive the raw mapping.

## Commands and results

All commands below were run from the assigned App worktree. Vitest uses private scratch configs derived from the repository config, with only module `__dirname` constants materialized for runner loading, private cacheDir, and (for exact) aliases to the private extracted approved artifact. The normal runner attempt directly against the repository config failed at startup with `__dirname is not defined`; the scratch config fixes that tooling limitation without a repo edit. Shared installs were never modified.

Initial RED (exit 1, two assertion failures), then initial GREEN (exit 0, two passes), used:
```sh
timeout 45s node_modules/.bin/vitest run --config /tmp/w-674ebcc09c/vitest.config.mjs --configLoader runner --no-cache src/tools/video-editor/hooks/useTimelineCommit.test.tsx -t 'splits the original raw seed'
```
The earliest corrected-source run still exposed output omission in the existing editor serializer; the final source explicitly carries output after strict disk serialization.

Final normal run (exit 0, **8 files / 162 tests passed**, 10.47s):
```sh
timeout 45s node_modules/.bin/vitest run --config /tmp/w-674ebcc09c/vitest.config.mjs --configLoader runner --no-cache src/tools/video-editor/hooks/useTimelineCommit.test.tsx src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/commands/localSaveSession.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/documentPatchIntent.test.ts src/integrations/runtime/client.test.ts
```
Final private exact run (exit 0, **8 files / 162 tests passed**, 11.98s):
```sh
timeout 45s node_modules/.bin/vitest run --config /tmp/w-674ebcc09c/vitest-exact.config.mjs --configLoader runner --no-cache src/tools/video-editor/hooks/useTimelineCommit.test.tsx src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/commands/localSaveSession.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/documentPatchIntent.test.ts src/integrations/runtime/client.test.ts
```
Logs: `normal-final.log`, `exact-final.log` under `/tmp/w-674ebcc09c`.

The earlier six-file neighbor run also included `src/tools/video-editor/lib/timeline-save-utils.test.ts`: 129 passed, 3 failed. The 3 failures are the existing resolved-config object identity/signature expectations after display-label projection, in unchanged `assembleTimelineData`. Confirmed with all three modified source modules loaded from `git show HEAD:<path>` using a private read-only Vite load plugin:
```sh
timeout 45s node_modules/.bin/vitest run --config /tmp/w-674ebcc09c/vitest-baseline.config.mjs --configLoader runner --no-cache src/tools/video-editor/lib/timeline-save-utils.test.ts
```
Baseline result: exit 1, the **same 3 failures / 24 passes**. Logs `targeted.log` and `baseline.log`. No assertion was changed or skipped.

Other checks:
```sh
timeout 45s node_modules/.bin/tsc -p tsconfig.json --noEmit
timeout 45s node_modules/.bin/tsc -p tsconfig.node.json --noEmit
timeout 45s node_modules/.bin/eslint src/tools/video-editor/lib/serialize.ts src/tools/video-editor/hooks/useTimelineCommit.ts src/tools/video-editor/hooks/clip-editing/useClipSplitting.ts src/tools/video-editor/hooks/useTimelineCommit.test.tsx --max-warnings 0
node scripts/vendor-lock.mjs check runtime.lock.json
git diff --check
```
All exit 0. ESLint was rerun after the final regression change.

```sh
timeout 45s node_modules/.bin/tsc -p tsconfig.app.json --noEmit
timeout 45s node_modules/.bin/tsc -p /tmp/w-674ebcc09c/tsconfig-exact.json --noEmit
```
App typecheck remains **unverified**: normal run and one alone retry each exited 124 after 45s with no diagnostics; private exact types also exited 124 after 45s with no diagnostics. The private config extends the actual App config and replaces only Composition export type paths. This is a qualification limit, not claimed success.

## Source identities and limits

- Runtime lock source stays `34eac0041b0891e9011966b39bcbd26053fde5bc`; lock SHA-256 `eb52cbbb3a1f40caca965eb0cb2c87142100adabb4c876a8582b6894c4281c8e`; vendor-lock check passes.
- Approved Composition archive: `vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz`; SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`. Extracted only inside private `/tmp/w-674ebcc09c/composition-exact` after realpath check; package 0.0.14. Normal shared install reports 0.0.8 and was left untouched.
- Unchanged original P1 source at this base: `tests/e2e/local/three-products.p1-chain.spec.ts`, SHA-256 `cae24b8e5481557f4812e47f06828aed3cf2176c6da92b4ca265095dbefd8175`.
- `package.json` SHA-256 `ce59c57b8f2a9da6e86cccbb31ad71876a86e33f910bb601ebf2dc727d040bdf`; `package-lock.json` SHA-256 `59cd66da9a223eb1ff3cf60fd06dfa5b4b376533786366bd94b74ae3d95140ba`; neither changed.
- Full-v2 request/reply adapters, DTOs, guards, reads, merge/dry-run/idempotency handling, receipt/records/effects/bindings/dependencies/history/undo/publisher/compiler behavior and structured conflict/invalid code/path/hint are unchanged. Existing client, handoff and exact-restart v2 tests pass; no new live server qualification is claimed.
- No HTTP/browser/original test body/service/socket/build/full-suite/test-service request, shared dependency/cache mutation, generated/fixture/pin/package/lock/ops change, commit/merge/rebase/checkout/push or file deletion.
- No H3 GO and no claimed repair of Agent's general sequential-mirror defect.

Next: independent Luna review, then owner-controlled integration preserving queued move/Undo work; complete App typecheck in its qualification environment. Original P1 execution and Agent mirror correction remain with their assigned owners.

