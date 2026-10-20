Source port complete on corrected root `85efd0ffa5cefc4ba38c63e0fb75e50258c5c28c`. Native parent-delete source is ready for review; actual safe Runtime pair/browser/reload/undo/retry qualification and zero legacy traffic remain **OPEN**. No blocker or evidence requiring a PLAN decision change.

Ported only `c866da88e6acb92e6f7194324e0a29bfacab3b4b..f1410193f6717ef53ccbeacdb5902028d5863a70`, once, across its 17 paths. The capture, gesture, their tests and frozen golden are byte-identical to the reviewed candidate. The existing root interfaces accepted the narrow types/ports/dispatcher additions without further product adaptation. Added 78 test lines: delete B authored after unknown move A, with/without an ordinary label suffix, retained original guards, no implicit retransmission, reload recovery and exact request bytes/key; plus an ordinary snapshot property suffix visibly refused while preserving the delete draft. Existing lost-delete-ACK recovery also checks exact persisted request bytes/key.

The current root lacked configured-gateway CORS, so the only additional paths are the exact CURRENT helper/direct tests from `7bb885b638838588a0dff81b64b7c34960ac07f3`. No other MAIN change was copied.

Single supported parent delete uses native capture → finish → submit on the existing session/outbox. Eligibility uses exact raw parent closure and known project/timeline/display binding; authored `app.canonical` stays opaque, with no suffix inference. Whole-row/collection/order guards, null/absence/prototype data, original source closure, one compiler and no-created-ID semantics remain. Capture/submission failure is visible and has no fallback; mixed native patches refuse atomically. No media or registry cleanup writer was added.

Original group/multi/occurrence and direct prepared-media writers remain unqualified and unchanged until native coverage qualifies. The entire original `useClipEditing.test.ts`, including line 261, is byte-identical to both corrected root and c866; all 21 tests pass. SHA-256: `1beea75106b059db7462b080059253688c47a77db16d55ecfbaf438c62ba9fce`. New ingress positives also retain grouped and prepared-media success when the native delete port is present. No original behavior expectation was weakened, no test was skipped, and no failure marker was added.

All other corrected ROOT paths are byte-preserved: public12 package/lock; development-only Runtime 0.2.9 lock/generated contracts; SDK/provider/bootstrap/settings/raw-settings/generation guards; mobile single portal and corrected mobile behavior; clean focus and explicit label intent; sourceMailbox/render/download/no-mode paths; original after-ACK A/B scheduler, label state and tests. Existing mounted test content only gains imports/new cases. No alias cleanup, None/PARAM/split/auto imports, root raw-renderConfig field, native wire/schema change, new provider or manager-branch integration.

Changed-path census against corrected ROOT (includes new untracked files): **+1,339 / −9, net +1,330 lines**. Product **+377 / −9, net +368** = reviewed parent-delete product **+356**, authorized CORS product **+12**. Tests **+961**; frozen golden **+1 line** (46,406 bytes). This is a source slice census, not the entire Timeline core.

Exact change/dependency allowlist (19 paths = 17 delete + 2 CORS):

| Path | Added | Removed |
|---|---:|---:|
| `src/shared/lib/media/mediaCrossOrigin.test.ts` | +30 | −0 |
| `src/shared/lib/media/mediaCrossOrigin.ts` | +18 | −6 |
| `src/tools/video-editor/commands/clipDeleteCapture.test.ts` | +126 | −0 |
| `src/tools/video-editor/commands/clipDeleteCapture.ts` | +204 | −0 |
| `src/tools/video-editor/commands/clipDeleteGesture.test.ts` | +61 | −0 |
| `src/tools/video-editor/commands/clipDeleteGesture.ts` | +42 | −0 |
| `src/tools/video-editor/commands/commitSession.clipDelete.test.ts` | +355 | −0 |
| `src/tools/video-editor/commands/commitSession.ts` | +42 | −0 |
| `src/tools/video-editor/commands/fixtures/recipe_m2_app_clip_delete.json` | +1 | −0 |
| `src/tools/video-editor/hooks/clip-editing/types.ts` | +5 | −0 |
| `src/tools/video-editor/hooks/clip-editing/useClipDeletion.ts` | +17 | −1 |
| `src/tools/video-editor/hooks/useClipEditing.ts` | +8 | −0 |
| `src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx` | +89 | −0 |
| `src/tools/video-editor/hooks/useTimelineCommandSession.ts` | +10 | −0 |
| `src/tools/video-editor/hooks/useTimelineCommandsService.ts` | +10 | −0 |
| `src/tools/video-editor/hooks/useTimelineOps.clipDelete.test.ts` | +300 | −0 |
| `src/tools/video-editor/hooks/useTimelineOps.ts` | +14 | −1 |
| `src/tools/video-editor/hooks/useTimelineState.ts` | +5 | −1 |
| `src/tools/video-editor/hooks/useTimelineState.types.ts` | +2 | −0 |

Dependencies consumed unchanged: authoringBundle, clipMovePrimitives/Recording, clipMoveCapture, trackLabelCapture, durable commitOutbox/session machinery, generated EditCommand/CommandRecord/AgentSelection, TimelineData/Patch/Editability, current store/commit dispatcher. Golden SHA-256 `091bc1c7fa9c57583dde8fcc6d6af9226513bf4f214369ef0892cc1db492f0aa` equals the reviewed fixture and current Agent fixture.

Validation on the final tree:

- Core, 6 files: **116 passed**, exit 0 (`notes/core-final.log`). This is the original reviewed 113-case core plus 3 new cases.
- Neighbor/CORS, 12 files: **401 passed**, exit 0 (`notes/neighbors.log`): original 380-neighbor cohort plus 21 current CORS cases. Total repository selection: **18 files / 517 passed** (the original 493-case approval plus 3 new cases plus CORS 21).
- Exact original opaque-parent counterexample, copied without input/assertion changes: **3 passed**, exit 0 (`notes/counterexample.log`). SHA-256 `abf193bdf89c1ca812c9f53a87395d634f5ada6b4f6023491bd1a56b6f344a34`.
- Existing Agent SDK native subset: **2 passed**, exit 0 (`notes/native-subset.log`): complete frozen command/record/after equality, opaque app.canonical, guarded inverse restoring both originals. No server/history redo claim.
- Scoped ESLint, all 18 changed TS/TSX files: exit 0, no diagnostics (`notes/lint.log`).
- Known-failure audit: exit 0, exactly 3 previously authorized drag markers, 0 forbidden (`notes/known-failures.log`). `git diff --check`: exit 0.
- Exact source allowlist/preservation/golden/public12 audit: pass (`notes/source-audit.json`). Public12 archive SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; all 77 installed regular members byte-equal to this root's archive.
- Shared dependency/cache metadata audit: before/after snapshots byte-equal. Read-only `/tmp/app-coherent-deps12/node_modules` supplies public12 with shared React/DOM 18.3.1 and Remotion 4.0.509; only this worker's ignored dependency link was changed, then restored. Runner uses `--configLoader=runner --no-cache --maxWorkers=1`; external repro cacheDir is inside own notes. No shared dependency file/symlink/cache/venv was written.

Exact final commands (cwd `/home/user/work/wt/app-m2-refreshed-parent-delete-source-port`; temporarily point this worktree's own `node_modules` symlink at `/tmp/app-coherent-deps12/node_modules` for reproduction):

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-parent-delete-source-port/notes/runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/clipDeleteCapture.test.ts src/tools/video-editor/commands/clipDeleteGesture.test.ts src/tools/video-editor/commands/commitSession.clipDelete.test.ts src/tools/video-editor/hooks/useTimelineOps.clipDelete.test.ts src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-parent-delete-source-port/notes/runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/lib/keyboard-delete.test.ts src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/shared/lib/media/mediaCrossOrigin.test.ts
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-parent-delete-source-port/notes/runner.cjs node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-parent-delete-source-port/notes/counterexample.config.ts --configLoader=runner --no-cache --maxWorkers=1
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-parent-delete-source-port/notes/native-subset.py
node node_modules/eslint/bin/eslint.js src/shared/lib/media/mediaCrossOrigin.test.ts src/shared/lib/media/mediaCrossOrigin.ts src/tools/video-editor/commands/clipDeleteCapture.test.ts src/tools/video-editor/commands/clipDeleteCapture.ts src/tools/video-editor/commands/clipDeleteGesture.test.ts src/tools/video-editor/commands/clipDeleteGesture.ts src/tools/video-editor/commands/commitSession.clipDelete.test.ts src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/hooks/clip-editing/types.ts src/tools/video-editor/hooks/clip-editing/useClipDeletion.ts src/tools/video-editor/hooks/useClipEditing.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.ts src/tools/video-editor/hooks/useTimelineCommandsService.ts src/tools/video-editor/hooks/useTimelineOps.clipDelete.test.ts src/tools/video-editor/hooks/useTimelineOps.ts src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/hooks/useTimelineState.types.ts
node scripts/quality/check-known-failures.mjs
git diff --check
python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-parent-delete-source-port/notes/audit-deps.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-parent-delete-source-port/notes/deps-after.json
cmp /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-parent-delete-source-port/notes/deps-before.json /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-parent-delete-source-port/notes/deps-after.json
```

Earlier setup/run history: one initial public12 setup assertion detected the missing CORS helper and aborted before switching the dependency link; the shell still ran the initial core on the borrowed 0.0.10 environment (**113 passed**, `notes/core-initial.log`). That run is not final public12 evidence. After copying authorized CORS and switching only the worker-owned link, the unchanged core passed **113** on public12 (`notes/core-public12-initial.log`); final expanded core passed **116**. No product/test expectation was changed to obtain those passes.

No full suite requested/run; no build, project TypeScript check, install, browser, localhost/socket, actual Runtime acceptance or integration worktree mutation. All executions here were bounded targeted/offline checks. No commits, merges, checkout/rebase, pushes, branch/ref changes or KEEP artifacts. No temporary/build output remains in the worktree.

Recommended next step: review/integrate only this source allowlist, then separately authorize qualification against the actual safe Runtime/Agent/public12 pair through the central service. Keep native group/multi/occurrence replacement, global legacy-writer deletion and production retirement claims OPEN.
