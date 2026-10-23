# A3 mounted child-placement return — ap2-A3-child-mounted-sol-0742

Implementation complete; independent review and manager-owned live qualification remain required. Both independent failures (0729 and 0738) were read and their missing mounted consumer finding is addressed.

## Exact source

- Assigned App worktree: `/home/user/work/wt/ap2-A3-child-mounted-sol-0742`.
- Base/current HEAD: `21c518a5ba176dc81abd988bcfc46b4165e95d25`; base tree `7c95fec8901bec0b50e1e8c18aed3c8ba1445332`.
- Final tracked worktree candidate tree: `c85d0c7bc1e0031368250c7a56e1d0836a247b2f`. This is the Git tree SHA calculated from all tracked worktree modes/blob bytes without writing the index/object database. The harness must verify it when committing; the final commit SHA does not exist yet and must be recorded by the harness/manager.
- Cumulative comparison baseline before inherited child WIP: `cffa91c93`. Inherited commits: `577d4b810`, `cc918bd9f`, `21c518a5b`. Current worker changes 13 files; cumulative allowlist is exactly these 14 paths (one inherited test file is unchanged by this worker):

- `src/app/hooks/useAppExternalDrop.ts`
- `src/features/gallery/hooks/useGalleryPageState.ts`
- `src/pages/shots/hooks/useShotImageMutations.ts`
- `src/shared/hooks/shots/__tests__/addImageToShotHelpers.test.ts`
- `src/shared/hooks/shots/__tests__/useShotGenerationMutations.test.ts`
- `src/shared/hooks/shots/addImageToShotHelpers.ts`
- `src/shared/hooks/shots/useShotGenerationMutations.ts`
- `src/shared/lib/placement/__tests__/placementService.test.ts`
- `src/shared/lib/placement/placementService.ts`
- `src/shared/state/selectionClipData.test.ts`
- `src/shared/state/selectionStore.ts`
- `src/tools/image-generation/hooks/useImageGenActions.ts`
- `src/tools/video-editor/contexts/VideoEditorProvider.test.tsx`
- `src/tools/video-editor/contexts/VideoEditorProvider.tsx`

No generated/schema/pin/lock/package/ops files, original P1/P3 fixtures, shared popup/media adapter, Undo, or move code changed. Nothing deleted. No commit/merge/rebase/checkout/push performed.

## Real mounted trace and decisions

1. `src/tools/video-editor/contexts/VideoEditorProvider.tsx` → `AgentChatBridgeRegistration` already owns the mounted editor's clip catalog and `agentSelectionOwner`. It now registers the Runtime-provided acknowledged `shots.canonicalComposition`, project identity, and timeline identity alongside that same catalog in `src/shared/state/selectionStore.ts`. The existing active-owner switch, replacement/disposal, and project reset govern both. No new persisted selection, lookup by shot ID, or unmounted optional prop is introduced.
2. The actual editor selection APIs (`userSelectTimelineClips` / `editorSelectTimelineClip`) retain selected display clip IDs for that mounted owner. `getShotPlacementTarget` obtains their identities from the existing `projectCanonicalComposition(...).clipIdentities` map. Multiple child clips are allowed only when every verified identity belongs to the same occurrence and requested source shot/project/timeline. Empty, foreign, ambiguous, non-addressable, duplicate display identities, and unrelated data-item selections refuse. No array-order or byte-equality ownership inference is used.
3. App `Layout` mounts the app-wide `GenerationsPane` outside the editor provider. `GenerationsPane` → `useGenerationsPaneController` → `src/features/gallery/hooks/useGalleryPageState.ts` previously had only current/last affected shot IDs. It now reads the existing active editor registration at action submission and passes real selected `ownerRef`, `timelineRef`, and one freshly reserved destination `shot_id` into both add and position mutation options (including pooled addition).
4. The other review-identified topmost producers also pass these concrete options: `src/tools/image-generation/hooks/useImageGenActions.ts` (ImageGenerationToolPage), `src/pages/shots/hooks/useShotImageMutations.ts` (ShotsPage), and `src/app/hooks/useAppExternalDrop.ts` (App's DndContext handler).
5. Every other real `useAddImageToShot` consumer is covered by the existing mutation hook's public submit wrappers, which resolve the same selection context before invoking React Query: `src/features/editor/components/ShotsPanelContent.tsx`; `src/features/tasks/components/TasksPane/hooks/useShotActions.ts`; `src/shared/components/ShotImageManager/hooks/useExternalGenerations.ts`; `src/tools/travel-between-images/components/hooks/useModalImageHandlers.ts`; `src/tools/travel-between-images/components/ShotEditor/hooks/actions/useDropActions.ts`; and `src/tools/travel-between-images/components/ShotEditor/useShotEditorController.ts` → its mutation refs → `src/tools/travel-between-images/components/ShotEditor/hooks/actions/useShotActions.ts`. These files remain untouched. `src/app/App.tsx` passes its mutation object to the external-drop handler. The only direct production `runAddImageMutation` caller is the add hook; the only position-hook consumers are gallery and image-generation actions.
6. The App QueryClient really retries mutations once. Both submit wrappers therefore capture owner and fresh destination once before retry, rather than allocating inside `mutationFn`. Explicit caller owner options are preserved unchanged. Regressions verify identical target requests across both attempts. The wrappers preserve stable callback identities and async rejection behavior.
7. Caller options → `useAddImageToShot` → `runAddImageMutation` (or position hook directly) → existing `placementService.placeGeneration` → existing `forkOccurrence` → A2 `LocalSaveSession`/outbox → Agent semantic `occurrence.fork` → accepted-basis reload → existing parent placement. The existing fork command/service algorithm was not rewritten. A small selected-timeline guard refuses if the legacy default-timeline resolver returns a different timeline; it never applies a same-named occurrence from another editor timeline. Nondefault selected timelines currently refuse rather than retargeting the service.
8. No canonical mounted context means the original parent-only options/path remain unchanged. With a canonical context, a shot ID alone cannot select an occurrence: missing/foreign/ambiguous selection refuses. Hosted/legacy parent behavior and explicit-owner service behavior remain covered by the original tests.

D15 remains intact: Agent execution commit `4edc4b321cae5cfc58252d7ed89e3f0408238646` / tree `f17b84c48bae3461dd11cedb8719bd17495a8210` contains registered `native_occurrence_fork.py` with the closed `{shot_id}` grammar. Normal CLIENT producer `34eac0041b0891e9011966b39bcbd26053fde5bc` is unchanged. C0 request/reply/undo/history code is unchanged: the existing v2 API/scope/base pair/commands/label/step patch+reads/merge/reads/dry-run/key and accepted/merged canonical/head/digest/receipt/effects/bindings/dependencies/history/undo/publisher/provider/compiler/conflict/invalid handling remain in A2.

## Exact commands and results

Final targeted command (13 files, including all original five-file/61-test placement/hook coverage, mounted provider registration, mounted gallery add/position/pooled → fork/outbox → fresh placement read, selection refusal controls, real existing callers, and retry identity controls):

```sh
npm exec -- vitest run --config /tmp/w-23219a8016/vitest.private.config.mts --configLoader=runner --no-cache src/shared/hooks/shots/__tests__/useShotGenerationMutations.test.ts src/shared/lib/placement/__tests__/placementService.test.ts src/shared/lib/placement/__tests__/placementService.workspaceV1.test.ts src/shared/hooks/shots/__tests__/addImageToShotHelpers.test.ts src/tools/video-editor/commands/commitSession.placement.test.ts src/shared/state/selectionClipData.test.ts src/shared/state/selectionActions.test.ts src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/features/gallery/hooks/__tests__/useGalleryPageState.test.ts src/pages/shots/hooks/useShotImageMutations.test.ts src/app/hooks/useAppExternalDrop.test.ts src/tools/travel-between-images/components/ShotEditor/hooks/__tests__/actions/useShotActions.test.ts src/tools/travel-between-images/components/ShotEditor/hooks/actions/__tests__/useDropActions.test.ts
```

Result: PASS, 13 files / 181 tests. The private config imports the repository's existing Vitest config, supplies its expected configuration directory for the runner loader, sets a private cacheDir, and maps all Composition public exports to their exact immutable private archive targets, with longer subpaths before the root. No tests or expectations are removed, skipped, disabled, or weakened.

```sh
npm exec -- tsc --noEmit --incremental false
npm exec -- tsc -p tsconfig.app.json --noEmit --incremental false
npm exec -- tsc -p tsconfig.node.json --noEmit --incremental false
```

Result: PASS (root, actual App, actual Node). Final App check pending completion at report draft; update before DONE.

```sh
npm exec -- eslint src/app/hooks/useAppExternalDrop.ts src/features/gallery/hooks/useGalleryPageState.ts src/pages/shots/hooks/useShotImageMutations.ts src/shared/hooks/shots/__tests__/useShotGenerationMutations.test.ts src/shared/hooks/shots/addImageToShotHelpers.ts src/shared/hooks/shots/useShotGenerationMutations.ts src/shared/lib/placement/__tests__/placementService.test.ts src/shared/lib/placement/placementService.ts src/shared/state/selectionClipData.test.ts src/shared/state/selectionStore.ts src/tools/image-generation/hooks/useImageGenActions.ts src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.tsx --max-warnings 0
git diff --check
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
```

Result: scoped ESLint/diff/App normal Runtime lock PASS. From `/home/user/work/agent`:

```sh
python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
```

Result: PASS, producer manifest matches. Agent and normal Runtime producer worktrees have clean `git status --short`.

```sh
python /tmp/w-23219a8016/check-private-graph.py
```

Result: PASS: archive SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`; every one of the 80 regular archive files byte-identical to the existing private graph; package `0.0.14`; all public export targets exist. Public resolution was independently checked with:

```sh
NODE_PATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P3-env-final-0407/record/private/node_modules node --input-type=commonjs - <<'JS'
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const privateModules = process.env.NODE_PATH;
const pkgRoot = path.join(privateModules, '@banodoco/timeline-composition');
const pkg = JSON.parse(fs.readFileSync(path.join(pkgRoot, 'package.json'), 'utf8'));
for (const [subpath, entry] of Object.entries(pkg.exports)) {
  if (subpath === './package.json') continue;
  const resolved = require.resolve('@banodoco/timeline-composition' + subpath.slice(1), { paths: [privateModules] });
  assert.equal(fs.realpathSync(resolved), fs.realpathSync(path.join(pkgRoot, entry.import)));
}
console.log('PASS: all public Composition exports resolve into the exact private graph');
JS
```

Result: PASS. The exact private graph used by final tests is the existing paired-head qualification graph; it was read only.

## Tooling incident and limits

Initial targeted Vitest invocations used `--no-cache` with the repository's default bundled config loader. That loader still touched `/home/user/work/app/node_modules/.vite-temp` (directory mtime 07:53Z; inspected empty afterwards). This violates the brief's shared cache restriction; it is explicitly reported rather than claiming zero shared-install touches. No shared package payload/install/symlink was intentionally edited and no manual cleanup or deletion was attempted. Final evidence uses `--configLoader=runner` plus a private config/cache and exact private Composition exports. Manager should assess whether the initial temporary-cache touch affects concurrent qualification.

Other setup attempts: the root repository config cannot use the runner directly because it references `__dirname`; the first private config had root-before-subpath alias ordering and failed import resolution. Both were corrected only in worker scratch before final green evidence. An actual App nullable-project type error and callback exhaustive-deps errors were corrected; no checks were waived.

No browser, localhost/socket, HTTP/live Runtime admission, service request, build, full suite, or central test-service request ran. The service tests use the existing in-memory fake Runtime; the real provider test mocks unrelated editor-state hooks but exercises the real mounted provider/adapter/registration lifecycle. Accepted/merged physical-binding and original P1/P3 journey proof remain manager-owned and unverified here. No contract decision was found wrong; the default-timeline restriction is now explicit and fails closed.

Next: harness commit and verify the calculated tree, independent Luna review of the cumulative 14-file source, assess the cache incident, then the manager-owned original integrated proof. Do not merge a red source.
