# App M2 automatic-placement adapter independent review

## Scope and source

- Reviewed `25e828af6d96f2cc0182a5014eb90ebeab4fec11` against `316073355a67d46f98168ec2152141e0748198a9`.
- Reviewed `/home/user/timeline-hub/hub/design/app-auto-host-client-lifecycle-adapter.md` and the complete bounded diff.
- Reviewed tree: `3b69f7cb30daca7bf498519acae32b5827ccaad5`.
- Product worktree was not modified.

## Verdict

**Adapter delta: verified for integration. Automatic placement: not complete and not approved.**

The adapter preserves the existing task/client contract and operation lifetime. Production still supplies no `imagePlacementHost`, so the checked UI correctly remains visibly unavailable. This is the concrete remaining gap, not evidence to activate automatic placement.

## Independent checks

- Existing bounded evidence: the worker report records the proportional eight-file run as **8 files / 484 tests passed**, exit 0; scoped ESLint and `git diff --check` also passed.
- Independent nearest controls, with the shared dependency tree read-only and a worker-owned temporary directory:

  ```text
  TMPDIR=/tmp/app-m2-auto-adapter-independent-review-cache node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/integrations/runtime/operationHost.test.ts src/integrations/runtime/clientLocalAdapter.test.ts
  ```

  Result: **2 files / 61 tests passed**, exit 0.

- A direct invocation without the repository snapshot runner stopped at config load with `ReferenceError: __dirname is not defined`; no tests ran in that attempt. No full suite, project typecheck, build, browser, localhost/socket, install, or live qualification was run.

## Invariant review

- **Exact task bytes/key and pre-admission reservation:** `clientLocalAdapter.ts:98-109` validates the canonical request, checks the reserved key, persists `reserve(...)`, then calls `admitPreparedTask(...)` with the same canonical body/key. The serializer mirrors the existing `taskRoutes.ts:91-116` order. Response project, key, capability, and digest are checked at `clientLocalAdapter.ts:110-112`.
- **Callback ordering:** after reservation, `assertCurrent()` runs before admission; after the Runtime response it runs before and after `reservation.admitted(...)` (`clientLocalAdapter.ts:102-119`). The editor callback itself checks the claim, identity, and owner before/after every async boundary (`editorImagePlacement.ts:24-29, 42-45, 83-118`).
- **One pinned transport, no rediscovery:** `operationHost.ts:198-202` constructs `WorkspaceClient` with the operation's existing `transport` and no token. Capability, object, and verified-media reads use that generated client (`operationHost.ts:252-254`). Exact prepared admission uses the same pinned `transport` directly (`operationHost.ts:221-237`) because the generated convenience `admitTask` would reserialize the request and cannot guarantee the saved bytes. There is no second client or discovery path.
- **Actor/realm/project/claim fences:** operation negotiation validates the captured actor/realm/runtime identity before publication; `run(...)` checks the binding before and after async operations (`operationHost.ts:176-215`). The adapter binds the editor project and rejects mismatched admission projects (`clientLocalAdapter.ts:94-100`); the reservation/owner checks cover the browser claim before and after awaits.
- **Retirement ordering:** `commitSession.dispose()` retires the image-placement host before releasing the claimed outbox/session (`commitSession.ts:503-517`). Operation retirement aborts the bound requests and cleans the operation handle.
- **Retry continuity:** the existing eight-file evidence covers exact accepted admission/commit retry, matching new bindings, callback retirement, and retained placement identity. The adapter adds no fresh key, body, or generated ID on replay.
- **Security/wire compatibility:** operation requests use `credentials: 'omit'`; supplied `Authorization` or operation-handle headers are rejected before forwarding, and only the existing operation handle is attached. No new endpoint, DTO, default scope, credential, hop header, or wire header was added. Existing normal-client paths, pins, root, and b1 behavior remain outside this seven-file delta.

## Exact production gap and next binding

The canonical owner is the existing App editor lifecycle:

1. `VideoEditorProvider.tsx:1142` installs the App runtime context and remounts on project/timeline/user/provider identity (`VideoEditorProvider.tsx:877-884`).
2. `editorRuntimeAssembly.tsx:650` calls `useTimelineState`.
3. `useTimelineState.ts:629` calls `useTimelineSave`.
4. `useTimelineSave.ts:99-102` calls `useTimelineCommandSession` without `imagePlacementHost`.
5. The session seam already accepts and forwards the optional host (`useTimelineCommandSession.ts:15-16, 115-117`), and `bindEditorImagePlacementHost()` exists at `clientLocalAdapter.ts:136-138`, but it has no production caller.

Minimal next binding: add an optional internal App-only operation source/factory to the existing runtime/editor lifecycle, construct one `RuntimeOperationHost` for the captured editor identity and project, bind it with `bindEditorImagePlacementHost(host, projectId)`, and pass the resolved host through the existing `useTimelineSave` → `useTimelineCommandSession` seam. Keep the host absent (and the current unavailable message) until the async bind succeeds. Dispose/retire that host on scope, identity, or unmount; the existing session dispose must remain the first retirement point before outbox release. The real source must be active on the candidate under test; do not inject fake hosts into consumer tests. Keep integration activation held until the real browser/Runtime proof on the matched official pair.

The legacy generation writer remains outside this delta at `src/shared/lib/placement/placementService.ts:placeGeneration`, reached through `src/shared/hooks/shots/addImageToShotHelpers.ts:runAddImageMutation` and `src/shared/hooks/shots/useShotGenerationMutations.ts`.

## Blockers / next real gate

- No production caller currently creates or injects the operation host; automatic placement must remain unavailable.
- Real browser/Runtime qualification is unverified: matched Agent/Runtime pair, S2 occurrence-image completion and five-field selection, reconnect/reload, lost admission/commit acknowledgement with exact retry, canonical reload, guarded undo/redo/ABA, claim/retirement races, and zero legacy traffic.
- Parent automatic placement remains deferred to the next reviewed official pair.
