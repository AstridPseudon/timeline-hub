# A2/P1 current-port independent review

## Verdict

**SOURCEPASS; CURRENT App TYPEGATEHELD.** The exact current port is bounded to the authorized four files and preserves the reviewed A2/P1 behavior. This is not a global App type PASS: the known inherited `TS2322` at `src/tools/travel-between-images/components/shotTimelineDataProvider.ts:771` remains separately owned by `0b6b5b6b7a50edec9eafed8631a794a51565510b`, which is not an ancestor of this tree. Do not clear the type gate until that owner change is merged and a fresh composed type run passes.

## Actual identity and scope

- Reviewed branch: `tl/ap2-A2-current-port-0932` (same source commit as this review worktree).
- Actual HEAD: `35a7382a45762d9f2f320146e29959e6ec895d4c`.
- Actual HEAD tree: `537a961ef34a1577e5375dfe8835ac76276920ee`.
- Exact base: `ff2d3c1d76c454f0402e48a42335d466a853cfe1`; base tree `84634e56df1aa205405e4a9301a8e6d3bd274f6f`.
- One direct commit only: `35a7382a` has parent `ff2d3c1d`.
- The author handoff’s computed final tree `7ce8eb90f1b177ef4ddfc45b5a05f6d229e73d21` is stale/wrong for the actual harness tree. This report and verdict use the actual `35a7382a` / `537a961e` identity.

`ff2..35a` is exactly these four modified paths, with no deletions or outside blobs:

| path | actual git blob | byte SHA-256 |
| --- | --- | --- |
| `src/tools/video-editor/hooks/useTimelineCommit.ts` | `ef2569f1ba9a9e609880f69fa91dd4351488962d` | `edee1fad387e3952736cf0bb99c2dd7a9b92133290b1dbdfea40db8a14d7cbfe` |
| `src/tools/video-editor/hooks/useTimelineSave.test.tsx` | `bb49ab17d1fdd135c9260f2cda19c6d5a1cfc13c` | `3c967d0b4ac5de8541656ab185a68f88c02ba820ffa850fc59b8389de1031834` |
| `src/tools/video-editor/lib/serialize.test.ts` | `53d92701271deb8cc439d9287b88f0ea6e012c65` | `d206079fd18c2e6a02dc0634e5891b5f02fa934e6fcb9291f79467f4c3f68e76` |
| `src/tools/video-editor/lib/serialize.ts` | `01776e71915a08015888430aa214df18c28ffd7f` | `a4c4c01fbfd21ab080876d6daf3ae6eee83dd60717568917cea89509b51de309` |

The three non-mounted blobs exactly equal reviewed `94b19e363047c1446608ff42ee11b0f34c906c69` / tree `c3752a0ff4978f400feb22e45f65b976188c7807`. The mounted test is the actual current `ff2` file plus exactly `108` insertions and `0` deletions; all pre-existing mounted Undo, move, shared, child, and provenance coverage remains in place. No spec, helper, JSON, fixture, generated, lock, package, dependency, pin, or support file changed.

## Caller and behavior review

The production path is intact: inspector Source In input → `useClipEditing` → `useTimelineCommit.materializeData` → `rowsToConfig` → `withHeldClipSourceFields` → existing local handoff/outbox. The helper is bounded and non-mutating: for a numeric held source it restores only explicitly authored `from`, `to`, and `speed` values removed by row materialization; absent values remain absent, `null` remains `null`, `hold` remains the row-authored duration, and opaque/app/unknown fields are carried by the existing clip spread. Non-held clips are returned unchanged. Other `rowsToConfig` callers are untouched.

The mounted regression exercises split of a local new ID, dependent inspector Source In trim while the split is pending, predecessor ACK, rebase of the dependent intent to the accepted base pair, and final canonical adoption. Its assertions retain API v1, project/timeline scope, base pair, `doc.patch`, exact `before`/`reads`, `merge: fields`, `dry_run: false`, per-step patch, no legacy save, and the new-ID result. Existing focused tests retain the accepted/merged/refused, canonical/digest/head/receipt/records/effects/bindings/dependencies, undo/history, publisher/provider/compiler, and conflict/invalid code/path/hint contract coverage.

## Exact checks

- Focused Vitest command (private Composition graph/config and cache under the worker tmpdir; `--configLoader runner --no-cache`):

  ```text
  ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-b8e50762 timeout 45s node node_modules/vitest/vitest.mjs run --config "$PWD/tmp-vitest-ap2.config.ts" --configLoader runner --no-cache src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/useTimelineCommit.test.tsx src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/commands/localSaveSession.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/documentPatchIntent.test.ts src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/lib/timeline-data.test.ts
  ```

  **PASS, 9 files / 183 tests**.
- Scoped ESLint command: `timeout 45s node node_modules/eslint/bin/eslint.js src/tools/video-editor/lib/serialize.ts src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/hooks/useTimelineCommit.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx --max-warnings 0` — **PASS**.
- `git diff --check` (base-to-HEAD and worktree): **PASS**.
- Unchanged caller guard for `useClipSplitting.ts`, `useClipEditing.ts`, `timelineLocalSaveHandoff.ts`, and `localSaveSession.ts`: **PASS**.
- `timeout 45s node node_modules/typescript/bin/tsc -p tsconfig.node.json` — **PASS**.
- `node scripts/vendor-lock.mjs check config/astrid-cli-surface/vendor.lock.json` — **PASS**.
- Normal origins: Agent `agt-pin-f894c3c9`, Runtime `rt-pin-34eac004`: **PASS**.
- Exact origins: Agent `agt-pin-b8e50762`, Runtime `rt-pin-a5d42583`: **PASS**.
- Shared App install realpath remained `/home/user/work/app/node_modules`; private Composition graph was used read-only.

Not run by task limits: App/root TypeScript, browser/body, HTTP/service, localhost, live socket, build, full suite, or central test service. The known App type failure was not rerun or edited. No live end-to-end behavior or H3 credit is claimed.

## Next step

Keep the remote queue **HOLD** until this source review is accepted and the App type gate clears on a fresh composed run. Then verify the harness-created merge contains only the one A2 commit and rerun the composed App typecheck/focused lane. No stale-ancestry merge.
