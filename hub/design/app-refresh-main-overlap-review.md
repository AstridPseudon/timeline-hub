# App MAIN refresh overlap and safety audit

2026-10-20. Worker `app-m2-refresh-overlap-review`. **Read-only product audit complete. Accept the inspected refresh resolution; hold the old boot change and do not apply the staged render-download implementation wholesale.** This is a source verdict, not merge, live, current-tuple, or release qualification.

## Sources and scope

Read PLAN and App INBOX 09:36/09:38, including the instruction that MAIN infrastructure wins. Compared:

- Original MAIN `60aa26b9529dcfa94f8ffdbd5edf42fa6c1babd2`.
- New MAIN `44f0b9ca9d0247d909f86f56955a04ef6c18a2aa` (17 commits after that base).
- Current integration / this worker HEAD `18becfbede00038830b97e63345445eeef54fa42`.
- Staged root `c866da88e6acb92e6f7194324e0a29bfacab3b4b`.
- Boot branch `tl/app-m4-runtime-boot-loading-owned-fix`, tip `8d486c25313379287ad06fafa8322ae8ed6bfeca`.
- `design/app-media-cors-proposal-revision.patch` and its accompanying report.

Also inspected, read-only, the refresh worker's resolved uncommitted files at `/home/user/work/wt/app-m2-refresh-main-current`. Its HEAD was still `18becfbed`; these files are **not an immutable merged ref**. Exact hashes of the 10 files checked are in [source-audit.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refresh-overlap-review/notes/source-audit.json). Recheck changed files if that worker revises them. No other worker files were written.

## Separate correctness, ownership, and verdict

| Area | Correctness | Ownership | Verdict / smallest action |
| --- | --- | --- | --- |
| Auth / URL / query roots | MAIN removes URL-dependent session bypasses, preserves failed same-origin workspace URLs behind manual recovery, and treats canonical project/timeline routes as Runtime authority. | MAIN app/auth infrastructure; no new Timeline authority. | **Reuse MAIN unchanged.** Do not restore `sessionlessDocument`, local/runtime mode switches, or `astrid-bridge` reconnect invalidation. |
| Boot first-failure proposal | Safe against granting authentication, but changes an explicit NEW MAIN assertion from loading=true to false after reading one. | App owns provider; MAIN now defines the behavior. | **HOLD old boot patch.** MAIN 44f's deterministic two-reading expectation supersedes the old baseline-failure premise. |
| Media CORS revision | HTTP(S)-only configured-origin addition fixes the original DOM CORS expectations and preserves blob mode. Does not make `/objects/:id/content` a valid byte route. | Shared-media owner, beyond editor-only paths; task authorizes review only. | **Source approve as a separate one-file proposal**, with permanent unchanged-mode controls and owner landing. No boot hunk. |
| `createDefaultTimeline` | MAIN canonical-ID precedence and concurrent pointer refresh are needed; neither source implements command-based bootstrap completion. | App bootstrap caller; Runtime owns adoption safety/receipts. | **Reuse MAIN selection/CAS code.** Later replace only the publisher seam with the already-settled create→init flow. |
| Render route / admission | MAIN selects `/api/astrid`, obtains ready capability identity, leaves canonical bytes to Runtime, removes redundant editor-counter `expected_version`, and reads admitted seam warnings. | Viewing render owner; App owns host/barrier and package composition. | **Reuse MAIN admission**, preserving Timeline command flush and independent async/task-scope fences when composing c866. |
| Render download | MAIN already fixes the missing-Origin navigation, supports picker streaming and blob fallback, and disables native video download/context menu. c866 adds distinct integrity/scope behavior but duplicates download ownership. | Viewing render owner; port/host integration coordinated with App. | **Do not reapply c866's whole controls/download change.** Reconcile distinct safety cases separately; preserve original tests. |
| Proxy / project chat | New MAIN changes rename/Main-selection/external-agent behavior, not the hidden credential selection lifetime. | App proxy/chat scripts; Runtime's direct-client handle cannot own this proxy. | **Keep MAIN chat changes.** Continue the separately owned operation-binding design; keep unsupported automatic requester closed. |
| ShotEditorView | Resolved file preserves the full raw-settings defense and uses MAIN canonical URL identity. Existing direct publication remains a legacy writer. | App shot caller/adapter; Runtime publishes receipts. | **Accept exact inspected resolution.** Preserve until native replacement qualifies; no claim of writer retirement. |
| TimelineEditorShellCore | Resolved file preserves MAIN mobile/portal behavior and Timeline recovery/conflict handling. | App shell; Viewing preview delivery. | **Accept the four-hunk resolution.** Do not restore the older portal/remount arrangement. |

## 1. Explicit auto-merge audits

### ShotEditorView: preservation is intact

The resolved file is byte-equal to `18bec` with only MAIN's import and two calls changed from `hasLocalModeUrlParams` to `hasRuntimeDocumentIdentity`. This preserves the new URL behavior and all Timeline raw-preservation code (`ShotEditorView.tsx:160-204` in the inspected resolution):

- Compare submitted normalized form values with the normalized editing-base projection; an unchanged form publishes nothing.
- Overlay only changed fields on the raw object; preserve absent fields, explicit nulls and opaque keys/default distinctions.
- Refuse replacing an unrepresented root or a changed compound value containing hidden authored content, while retaining the dirty draft and original editing base.
- Publish against the editing base's expected parent head; do not substitute a newly polled head as authorship authority.

Read the actual assertions in `ShotEditorView.test.tsx:109-331`. The **entire** `direct shot writer raw payload preservation` block is byte-identical in the resolved file, including success for ordinary compound edits, ordered arrays, explicit null and undefined clears, no default insertion for absent/null/empty roots, `__proto__` as an own data key, no input mutation, shared-occurrence isolation, refusal with draft/clean-snapshot retention, and a subsequent successful safe edit. This is not merely a test-name inventory. The only test-file change is the setup URL, now `?project=...&timeline=...`.

Limit: these tests use a mocked publication port and inspect constructed Runtime payloads. They prove neither real Runtime acceptance nor zero legacy publication traffic. `updateCanonicalShotSettings` still builds a graph and `canonicalShotComposition.publish` reaches `dataProvider.ts`'s `publishParentComposition`. Keep the guards until the native command replacement lands in the same qualified step; MAIN does not remove this migration requirement.

### TimelineEditorShellCore: exact four-hunk composition

The resolved shell is exactly NEW MAIN plus:

1. Import `TimelineCommandRecovery`.
2. Suppress legacy realtime conflict handling while `commandSession.state.status === 'conflict'`.
3. Apply the same suppression to the legacy conflict banner.
4. Mount `<TimelineCommandRecovery commandSession={chrome.commandSession} />` beside shared recovery banners, outside the desktop/touch layout branches.

The three original Timeline shell tests remain byte-identical: explicit persisted-owner recovery, exact retry without snapshot recovery actions, and retained command conflict without “Keep my changes” / “Use latest version” replacement choices. Their assertions were read, including the no-automatic-recover and exactly-one-recovery-surface checks.

Keep MAIN's `previewPanelSurface = {...previewSurface, portal: null}` and exactly one shell-owned `previewPortal`. MAIN's preview hook deliberately preserves the mounted Player across physical layout-slot movement; do not restore the old `attachmentGeneration` key or the old phone/condensed portal condition. MAIN's tests assert one portal on phone and across layout transitions, mobile undo/redo/scrubber placement, sheet opening, safe touch targets, and the sidebar Video tab. Resolved `useTimelineState` changes concern touch/label geometry, not the command session or save barrier. Preview delivered-revision metadata remains present. No new writer is introduced by these shell changes.

## 2. Boot proposal: real behavioral collision with NEW MAIN

The old branch changes only the provider's final connecting branch to `isBooting: outcome === null` and adds four tests: pending permission/probe, first failed reading, and subsequent recovery. On the old source this satisfies the earlier AuthContext expectation without opening `RuntimeConnectionGate`: `isConnected` stays false.

However, NEW MAIN's `src/shared/contexts/__tests__/AuthContext.gated.test.tsx` now explicitly asserts:

```ts
expect(fetchMock).toHaveBeenCalledTimes(1);
expect(screen.getByTestId('isLoading')).toHaveTextContent('true');
// advance POLL_INTERVAL_MS
expect(fetchMock).toHaveBeenCalledTimes(2);
expect(screen.getByTestId('isLoading')).toHaveTextContent('false');
```

This was introduced by `44f0b9ca9` itself, titled “gated hosted-auth tests assert the one-path design, deterministically.” It is not an incidental waitFor timeout now. **Do not call the old fix a required baseline repair, lengthen/change this assertion, or merge the branch wholesale.** Report this evidence to the orchestrator; retaining MAIN needs no product follow-up. If a first-reading UX change is still desired, it is a deliberate new behavior decision with both assertions considered, outside this audit.

NEW MAIN also exports `POLL_INTERVAL_MS`, exposes health `schemaDigest`, and fixes inherited-property refusal lookup. c866's provider delta adds another own-property lookup helper to the older provider. MAIN's `Object.entries(...).find(...)` already solves that lookup: **drop the duplicate helper**, retaining MAIN's digest, export, and tests. Neither old provider file should replace the refreshed one.

## 3. Render reuse and the distinct remaining safety work

### Admission / receipts

Reuse MAIN's changes in `useRenderState`, `renderRouter`, `renderPipeline`, and `renderRuntime`:

- Construct `AstridLocalClient({projectSlug})` so catalog/task calls use the configured `/api/astrid` door, rather than the timeline provider's `/api/runtime` base. MAIN tests assert both same-origin and hosted prefixes.
- Keep the durable save barrier. Integration's `useTimelineSave.ts:397-402` already flushes the command session first, then the remaining snapshot barrier. Removing the wire `expected_version` must not remove this ordering.
- Use Runtime's timeline resolution and admission snapshot, not the App display counter, as export authority. Preserve MAIN's operation-scoped v3 key and advisory seam report from admitted task `spec.spec.inputs.timeline_authority`.
- Do not restore the old client seam blocker or stale-editor-counter rejection tests. The upstream replacement tests explicitly admit render and surface advisory warnings; these are MAIN behavior changes, not a Timeline worker silently dropping a behavior.

Current Runtime `store.py:1698-1777,1936-1960,2069-2123` independently verifies project/timeline, optional canonical expectations, retained closure/media, and resolves the actual `config_version`. Historical `canonical_revision` is an additive closed five-field revision/publication selector, checked against commit history and receipts. App's current `canonical_head_revision_id` metadata is a mutable expectation, **not** that historical selector; neither MAIN nor c866 should be credited with the pending historical-render/requester workflow. Keep the normal `/v1` receipt path; no new protocol/receipt ledger is needed.

**Remaining provenance issue, present in MAIN and c866:** `useRenderState` still assigns `renderRevisionRef.current` from the number returned by the local save barrier and `commitRenderResult` labels it as the result's revision. `TimelineRenderControls` prints “Timeline version N.” Command-session projection advances this local config counter independently of Runtime document version. Removing it from admission is correct but does not make that result label authoritative. Small follow-up: populate result identity from the admitted task's Runtime `timeline_authority` (version and immutable parent identity where available), or leave it unknown until available. Add one targeted case with local display counter 7 and Runtime admitted version 12; expect the Runtime identity, never relabel an old result on a later ACK. Do not add a second head read as a substitute.

Task admission already parses the neutral `{data, receipt}` mutation using `runtimeTaskMutationSchema` before projecting the app-facing task (`taskRoutes.ts:100-115`). It currently returns only `{task}`. This refresh does not bypass Runtime receipt validation, but that projection alone is not sufficient proof of a separate resumable requester continuation. Retain the existing requester/outbox acceptance linkage requirements rather than treating any task poll or equal head as an ACK.

### Download: MAIN equivalent fix, distinct c866 safety tests

MAIN `a32707cc9` already handles the concrete bug: CORS fetch sends Origin; HTTP failure saves no body; picker cancellation is quiet; picker streams via `response.body.pipeTo`; fallback uses a blob URL and the film filename. MAIN's controls also retain dismissed-error/seam-warning UI and mobile compact mode, and disable video-menu download and context-menu Save. All four download cases were read at NEW MAIN `TimelineRenderControls.test.tsx:242-338`.

c866 adds a separate hook-owned `downloadRenderResult`/`managedRenderDownloadRef`, `projectObjects.read`, size/digest verification and stale-result disposal; its older controls version would remove MAIN's picker streaming, native-download suppression, compact props and newer warning/dismissal UI. **Do not take that whole file or duplicate Download implementation.** Keep MAIN controls as the starting point.

Not equivalent: c866's `useRenderState` scope-generation fences across admission/poll/cancel and wrong-task/project output rejection remain useful independent safety deltas. Port those hunks onto MAIN while preserving its seam-report handling and absence of `expectedVersion`. Preserve their tests. Do not restore `expectedVersion` option/type/key/error helper from c866's older router.

c866 also has tests that refuse missing storage, bad size/digest, stale pending reads, and unmount/project/timeline/provider disposal. Those are stronger than MAIN's raw fetch. **Do not delete or weaken them to claim the whole staged fix is redundant.** The minimal orchestration follow-up is a Viewing-owned split: MAIN download/admission plus the independently necessary scoped-result checks; explicitly reconcile the strict project-object/digest download assertions with MAIN's streaming behavior before adopting that part. Source equivalence establishes that the original door-error bug is fixed; it does not settle this stronger integrity/streaming tradeoff. No replacement design or behavior decision is made here.

## 4. Bootstrap and proxy designs after MAIN

**Bootstrap:** MAIN adds canonical-ID-over-alias precedence, refetches concurrent Main reassignment, refuses an unresolved concurrent alias instead of returning it, and retains metadata CAS/spread so chat state is preserved. Keep all of it. The newer tests add four positives/refusals to the original behavior set; do not transplant an older whole helper/test file when wiring `bootstrapInitialization` later.

`publishEmptyTimeline` still publishes `expected_head: null` with deterministic revision/key. `ensureProjectHasTimeline` still treats a truthy head as reuse and sends headless repair through the legacy publisher. These are not proof of pristine accepted history or native-init completion. The original lost-ACK test asserts identical publisher request/key under an in-process fake transport; its stub receipt contains only `receipt_id`, and it proves no browser restart or real server adoption. Preserve these success requirements, adding MAIN's alias/CAS cases to the already-settled create→verified H0→guarded init/track batch→accepted receipt/history/immutable proof migration. Runtime F1/F2 republication remains a release prerequisite; do not qualify the old 0.2.9 tuple here.

**Proxy:** the base→NEW MAIN diff has no changes to `scripts/runtime-discovery-proxy.mjs`, `src/integrations/runtime/client.ts`, or `dataProvider.ts`. `astrid-project-chat.ts` adds rename, external-agent detection and guarded promotion of a newly created session to Main. Its discovery-backed `runtimeChatClient` still resolves endpoint/token independently for every `getProject`, `updateProject`, or `listProjects`; `ProjectChatRegistry.change` can therefore cross a hidden binding between its read and CAS update. Equal project versions do not establish an actor/realm lifetime. This is an existing open boundary, not a regression attributed to the new rename code.

Keep MAIN's chat semantics and tests. The App-owned lifetime design must cover compound chat operations/retries and the proxy's actual selection, not just its browser caller. Runtime's direct `OperationHandle` contract explicitly excludes a credential-reselecting proxy. No browser token exposure, new endpoint/DTO, permissive fallback, or automatic requester activation is justified by this refresh. Exact retry after a newly negotiated equal actor/realm binding remains allowed as already settled.

## Verification performed and limits

No behavior tests were necessary for this source-only audit. **No Vitest, full suite, build, project tsc, install, browser, socket, or localhost run was made/requested.** Other workers' pass counts are not claimed as this worker's evidence. Shared dependencies, caches and venvs were not modified.

Executed this repeatable static source/assertion check:

```sh
python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refresh-overlap-review/notes/audit_sources.py
```

**PASS, exit 0: 14/14 static checks.** It compares the actual resolved sources to exact refs, hashes the inspected files, proves complete raw-test-block and three shell-test preservation, and checks the exact two-reading MAIN assertions. It does not execute application behavior. Output: `workers/app-m2-refresh-overlap-review/notes/source-audit.log`. Final `git diff --check`, `git status --porcelain=v1`, and `git apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-media-cors-proposal-revision.patch` in this audit worktree exited 0 with no output: no product/repo changes; the media patch applies to this worker's 18bec base. MAIN's helper is byte-identical, but this apply check is not a qualification of the refreshed full tree.

Recommended next steps: finish/harness the reviewed refresh; retain MAIN's boot semantics; land the shared-media-only proposal through its owner with permanent controls; split the c866 render cohort and correct Runtime result labels; rebase bootstrap/lifetime work narrowly onto MAIN; then let the owning manager qualify the final refreshed tuple. This worker does not request a merge or another full run. No decision was changed, and no product edit was made.
