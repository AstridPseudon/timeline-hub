# App refresh onto owner main — resolved source ready; ancestry blocked

Worker/worktree: `app-m2-refresh-main-current`, `/home/user/work/wt/app-m2-refresh-main-current`, branch `tl/app-m2-refresh-main-current`. Source is frozen for the imminent merge/full; `KEEP` is set.

## Exact inputs and result

| Input | Commit | Tree |
| --- | --- | --- |
| Integration / worker HEAD | `18becfbede00038830b97e63345445eeef54fa42` | `44d514b44c864ff9dbb3b99aba2b0a41891af83f` |
| Verified local origin/main | `44f0b9ca9d0247d909f86f56955a04ef6c18a2aa` | `85ab85d225f106990cb04b0a22e4eaff1d0c8035` |
| Resolved working source | harness commit pending | `74d6c8033b1e006e8dbd4accc361b4e1288093e9` |

Merge base: `60aa26b9529dcfa94f8ffdbd5edf42fa6c1babd2`. All 17 upstream commits incorporated in the prepared source: **270 paths, +7298/-7595**, with rename detection. No fetch was needed; exact refs still match at final verification. Read PLAN, App INBOX including 09:36/09:38 authorization, App STATUS and the harness before work.

## Blocker: external harness must establish merge ancestry

The authorized command `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/merge-forward app-m2-refresh-main-current origin/main` failed **before any changes**, exit 128:

```text
fatal: update_ref failed for ref 'ORIG_HEAD': cannot lock ref 'ORIG_HEAD': Unable to create '/home/user/banodoco/reigh-app/.git/worktrees/app-m2-refresh-main-current/ORIG_HEAD.lock': Read-only file system
```

This sandbox cannot modify Git metadata. No permission bypass, manual commit, checkout, rebase, push, or integration-worktree edit was attempted. The worker computed Git's real three-way source merge using `git merge-tree --write-tree` with objects redirected to its own temporary notes directory and the repository object store read-only, materialized only changed paths, then resolved the conflict. A private index was used only to calculate the final source tree and complete binary patch; repository index/refs were untouched. Temporary object/index files were cleaned up after recording the result.

**The requested two-parent upstream merge has NOT been established.** The normal exit harness may commit the prepared source as a single-parent commit; that alone must not be accepted as this task's final outcome. The outer harness needs to establish origin/main ancestry outside this sandbox, preserving the tested tree above. Then verify both exact inputs are ancestors and the committed tree equals the recorded result before the gated integration merge. `BLOCKED`, rather than `DONE`, records this remaining requirement.

Complete source handoff including newly added files: [refresh.patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refresh-main-current/notes/refresh.patch). Apply/review through the normal external harness; patch is against exact integration `18becfbede…`. [Source audit](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refresh-main-current/notes/source-audit.json).

## Conflict resolution and overlap review

Only conflict: `src/tools/video-editor/components/TimelineEditorShellCore.tsx`, one import hunk. Kept main's `TimelineEditorShellToolbar, TimelineUndoRedo` import and integration's `TimelineCommandRecovery` import. The command recovery component, command-conflict exclusion of snapshot recovery, explicit owner selection and exact retry assertions remain.

There are **14 overlapping paths** (integration changes 208 paths; main changes 270):

- `src/integrations/runtime/createDefaultTimeline.test.ts`
- `src/tools/travel-between-images/pages/ShotEditorView.test.tsx`
- `src/tools/travel-between-images/pages/ShotEditorView.tsx`
- `src/tools/video-editor/components/PreviewPanel/PreviewPanel.tsx`
- `src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx`
- `src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.test.tsx`
- `src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.tsx`
- `src/tools/video-editor/components/TimelineEditorShellCore.test.tsx`
- `src/tools/video-editor/components/TimelineEditorShellCore.tsx`
- `src/tools/video-editor/hooks/useClipDrag.test.tsx`
- `src/tools/video-editor/hooks/useClipDrag.ts`
- `src/tools/video-editor/hooks/useTimelineState.ts`
- `src/tools/video-editor/hooks/useTimelineState.types.ts`
- `src/tools/video-editor/runtime/processes/astridAcpBridge.test.ts`

Every overlap was inspected against both parents. All **194 integration-only paths** (including deletions) remain exact to integration; all **256 main-only paths** remain exact to main. Zero exceptions in the blob audit. No extra repair, proposal, baseline change, test expectation change or package adoption was added beyond the upstream changes and import conflict resolution.

- **Shot settings:** retained raw-root overlay, malformed-root and compound-edit refusals with dirty drafts retained, raw encoder/digest preservation and canonical immutable publication. Main's route checks use canonical project/timeline identity. All raw settings/name tests remain. `ShotEditorView.tsx` differs from integration only by main's three route-identity substitutions.
- **Root/transition opaque data:** existing serialize, internal snapshot boundary, data provider, raw shot records, transition preservation and no-op/clear safety implementations are unchanged. No snapshot replacement or writer added.
- **Commands/persistence/history/outbox:** command session and outbox implementations, guarded recovery, retry identity, publication history boundaries and lifecycle hooks remain exact integration. `useTimelineState`/types merge main's removed touch precision state and responsive label width while retaining command ports, history ownership and snapshot-write blocking. Drag keeps the durable command capture path, plus main's touch selection and label geometry changes.
- **Preview:** main's single portal ownership and continuous Player lifetime across physical layout moves win. Revision labels, unavailable-target honesty, local-after-ACK handling, mailbox delivery and project/timeline scope remounts remain. Main itself updates the physical-slot test from remounting to retained Player identity; this was adopted as upstream layout behavior, with all separate revision/scope safety assertions preserved. No new expected-fail/skip markers were introduced.
- **Route/auth/settings:** main's one URL/Runtime path, canonical-ID/alias normalization, AuthGate/AuthContext and Connection settings section are retained. Main's reconnect deletion of the `astrid-bridge` query root remains; no retired modes/providers restored.
- **Render:** `TimelineRenderControls.tsx`, `renderRouter.ts` and `createDefaultTimeline.ts` are all **byte-identical to main**. Download fetches through the CORS path, using a streamed file-picker save or Blob fallback; admission uses Runtime catalog/timeline authority rather than the local save counter. No older render cohort was imported.
- **ACP:** main's new chat becomes Main; the integration listen-error rejection fixture fix stays, and the socket tests passed centrally.
- **Mobile:** upstream thumb controls, inspector, text editing, touch geometry and one preview portal are retained. Focused shell/mobile/editor/render controls pass; browser journeys were not run.
- **Bootstrap:** main's canonical-ID preference and concurrent primary assignment handling stay, as do integration's CAS/lost-ack bootstrap tests. This refresh does not close the already known provider-backed initialization/`timeline.init` work or the Runtime F1/F2 republish requirement.

## Deletions / renames

All upstream deletions remain: `localModeUrl.ts` and its test; `AstridAcpSessionControls.tsx` and its test; `TimelineModeSwitcher.tsx`; `WorkspaceConnectionRecovery.hosted.test.tsx`; `useAstridBridgeDiscovery.ts` and its test. The old workspace recovery component and regular test are moved to shared `RuntimeConnectorRecoveryBanner` paths, as main specifies. Their complete upstream intent was retained; no Timeline safety tests were deleted independently.

README/docs only change as carried by upstream (`docs/structure_detail/tool_video_editor.md`). `package.json`, `package-lock.json`, `runtime.lock.json`, vendored artifacts and generated clients remain exact integration: **Composition 0.0.8 / Runtime client 0.2.1**. Public12/client029/root candidate and baseline proposals remain outside this unit.

## Evidence

**982 passed, 3 unchanged existing expected failures, 47 test files, 0 unexpected failures.** Exact complete commands and per-run logs: [test-commands.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refresh-main-current/notes/test-commands.md).

| Focused run | Result | Duration |
| --- | --- | --- |
| Overlap + immediate safety, 10 files | 231 passed / 3 existing expected failures | 46.54 s |
| Durability + opaque fields, 17 files | 355 passed | 39.79 s |
| Upstream render/mobile/route/auth/settings, 18 files | 377 passed | 64.77 s |
| Central vendor-lock + ACP socket, 2 files | 19 passed | 10 s service / 6.86 s Vitest |

The three expected failures are unchanged `useClipDrag.test.tsx` cases: free multi-clip move to a new bottom track, pinned group cross-track move, and pinned group move to a new track. No new `it.fails`, skip, assertion weakening or fixture replacement was added. Shell ESLint and `git diff --check` pass. Central run `app-m2-refresh-main-current-vendor-lock-cachefree-integration-1020095333-11171` used the exact final tree above, the required preload, `--configLoader=runner --no-cache --maxWorkers=1`, and this worktree's physicaldeps8 symlink.

No full suite, install, build, browser, localhost direct run, or project-wide TypeScript check was run/requested. No current Runtime/Agent pair, real MP4/download, frame/audio parity, owner film, native writer retirement or M2/M3 exit qualification is claimed. Shared dependencies/runtimes/venvs were read-only, including Vite caches. The upstream-controls run emitted only an old caniuse-lite data notice; no dependency change was made.

## Next steps

1. Outer harness establishes actual upstream merge ancestry, preserving tree `74d6c8033b1e006e8dbd4accc361b4e1288093e9`; verify both exact parents are ancestors. Review the binary patch if needed. This is the only blocked part of this worker's result.
2. Manager requests the one authorized post-refresh batch full, then gates the refresh into integration. No full was requested here.
3. Rebase/review pending connector-lifetime, bootstrap and render/current-pair units against this refreshed source. In particular `scripts/astrid-project-chat.ts`, main's render save/admission and canonical bootstrap logic have changed. Keep coordinated package adoption separate.
