# App M2 automatic-placement owner binding: independent review

Date: 2026-10-20 UTC. Reviewed the settled `PLAN.md`,
`app-auto-production-operation-owner.md`, and
`app-auto-adapter-independent-review.md`. Compared the assigned App worktree
(`774007bdf7eb7d3f1958807f064eaa6b0a551bfc`, tree
`9358d4f1bad2103cdffc333624d10abca6d9cecf`) with `25e828af6`.

## Verdict

**APPROVE the bounded production owner-binding source change.**

This approves the source wiring and lifecycle ownership only. It does **not**
approve automatic-placement activation or claim completion of the real browser /
Runtime gate. That gate remains required and held.

## Source findings

The three-file diff is the intended minimal production binding:

- `VideoEditorProvider.tsx:911-928` directly creates one
  `RuntimeOperationHost` for the keyed editor instance and calls
  `bindEditorImagePlacementHost(operationHost, projectId)`. There is no optional
  factory prop, injected fake host, or alternate production source.
- The host is published only after the asynchronous same-origin operation bind
  succeeds (`VideoEditorProvider.tsx:1159`). Before that, and after failed or
  hosted negotiation, the context omits `imagePlacementHost`; the existing
  `IMAGE_PLACEMENT_UNAVAILABLE` surface therefore remains visible and refuses
  the placement draft.
- `useTimelineSave.ts:41,99-103` forwards that exact context object into the
  existing `useTimelineCommandSession` seam. The command session creates the
  existing editor-owned placement continuation and existing outbox; no second
  outbox or rediscovery client is introduced.
- The provider key at `VideoEditorProvider.tsx:879-886` remounts the instance on
  project, timeline, `userId`, and data-provider identity generation changes.
  Each Strict Mode effect setup creates a fresh host. Cleanup marks the bind
  stale and disposes the exact host. A late bind cannot publish into the old
  instance and explicitly retires its newly returned binding (`:917-927`).
- `commitSession.ts:504-521` retires the bound operation before releasing the
  claimed editor outbox/session. The callback fences in the existing placement
  implementation still check claim, operation identity, and owner before and
  after each await.
- `RuntimeOperationHost.bind()` rejects non-empty `runtimeOrigin()`, so this
  owner is same-origin local Runtime only. Its generated clients share the
  already-negotiated operation transport; they do not discover a session,
  select credentials, or create a second transport. Bound requests use omitted
  credentials. The Vite operation proxy strips authorization/cookie headers
  and response `set-cookie`/CORS credentials.
- `clientLocalAdapter.ts:94-119` preserves the approved admission boundary:
  project and canonical task shape are checked, the exact serialized body/key
  is reserved before admission, the same bytes/key are sent through the pinned
  operation, and response project/key/capability/digest are checked. The
  editor placement code retains original approval, raw occurrence owner,
  lane/anchor, fallback/policy, accepted basis/read closure, IDs, and exact
  task bytes/key. Equal actor/realm retry on a new binding remains possible;
  changed scope or request remains refused.
- Placement remains S2 occurrence-only (`occurrence:<id>`, explicit raw lane;
  no `::` or inferred parent-S3 destination). No parent-S3 guess or legacy
  placement writer was activated by this diff.

The source review found no unused optional factory, credential leak, operation
rediscovery, second automatic-placement outbox, or retirement-order defect.

## Evidence used

Existing bounded evidence was used first, as required:

- The owner report records the five-file nearest run as **149 tests passed**
  and the recovery/projection follow-up as **38 tests passed**, plus scoped
  ESLint and `git diff --check` passes.
- The preceding independent adapter review records **61 tests passed** in the
  operation-host/client-adapter controls and verified the pinned transport,
  exact admission, identity fences, and no-rediscovery properties.

Nearest independent lifecycle/callback controls run on this worktree:

```text
TMPDIR=/tmp/app-m2-auto-owner-binding-independent-review-cache \
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs \
node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
--configLoader=runner --no-cache --maxWorkers=1 \
src/tools/video-editor/commands/commitSession.test.ts \
src/tools/video-editor/components/EditorImageGeneration.test.tsx
```

**PASS: 2 files / 84 tests, exit 0.** This covers close-time claim/retirement
and exact recovery behavior plus visible unavailable/available placement UI.

```text
git diff --check 25e828af6
```

**PASS, exit 0.** No product files were modified by this review. No full suite,
project typecheck, build, browser, localhost/socket, install, or central test
service run was performed.

## Exact real browser gate still required

The required gate must use the real App candidate with the current normal pair:

- Agent/provider: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`
- Runtime/server: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- App: the final harness snapshot tree containing this three-file change

Use the existing Vite/Playwright setup, not a fake operation host:

- Vite production operation route: `"/runtime-config/v1/operation"` in
  `config/vite/vite.config.ts:93`, backed by
  `createRuntimeOperationProxyOptions()` in `config/vite/runtimeProxy.ts:47-72`.
- The actual admission handler is
  `createRuntimeOperationAdmissionPlugin()` in
  `config/vite/runtimeProxy.ts:74-94`; it applies origin/host/fetch-metadata
  checks and strips credentials before the proxy. The lower-level real proxy
  handler is `createRuntimeProxyServer()` in
  `scripts/runtime-discovery-proxy.mjs:324-385`, with control path
  `/runtime-config/v1/operation` and bound data prefix
  `/runtime-config/v1/operation/runtime/v1/`.
- The automatic-placement traffic to observe through that operation prefix is:
  `POST /v1/tasks` (exact task bytes/key), `GET /v1/tasks/{taskId}`,
  `GET /v1/tasks/{taskId}/managed-outputs`,
  `GET /v1/projects/{projectId}/media-selection/verified`, and
  `POST /v1/projects/{projectId}/timelines/{timelineId}/commit`. No direct
  `/api/runtime` fallback is acceptable for this owner path.
- Run the existing central `test:e2e:three-products` configuration and its
  `tests/e2e/local/three-products.spec.ts` journey with the real local Runtime,
  Chromium setup, and the matched d874/2c4 source guards. The automatic
  placement case must retain the real S2 occurrence image flow, reconnect and
  reload, durable outbox recovery, lost admission/commit acknowledgement with
  exact retry on an equal actor/realm fresh binding, guarded undo/redo including
  strict ABA, retirement/late-callback races, and zero legacy automatic-
  placement traffic. Hosted/remote negotiation must remain visibly unavailable.

This exact browser/Runtime acceptance was not run here and remains the
activation gate. The source approval must not be relabeled as completion of
automatic placement.

## Recommended next step

Have the orchestrator run one centrally registered, immutable App-tree +
d874/2c4 pair gate through the actual proxy route/handler above. Activate only
if all required acceptance/reconnect/reload/undo/retry/zero-legacy assertions
pass; otherwise retain the unavailable/refuse-draft behavior and report the
concrete failure.
