# Automatic production submission binding: source question

Status: **BLOCKED on ingress/session ownership; no production binding delivered.**

Worker: `app-m2-auto-production-submit-binding`. Read PLAN first. Base remains App
`171a259acbeb3ced855ca8f72fed0943a2f5a5cb`, tree
`f33b5268678efe390a5732022d81b53f35ccf509` (normal013/public12/root171a).
No product, tests, generated client, dependency pin, root, renderer, Auth or player
source changed. No approved source paths were copied speculatively. This is the
brief's permitted stop with an exact product/source question, not completed work.

## Exact question for the orchestrator

**Should the editor host own an invocation of the existing ImageGenerationModal,
with a new explicit add-to-timeline option and explicit raw occurrence target,
and supply that invocation with its existing accepted command session/outbox?**
If another production binding already supplies this, name its source ref and
callsite. The current image page and shared modal do not receive an accepted
command session or claimed outbox. Reusing the global image page instead requires
an explicit target/session bridge; please choose that product/source location
rather than deriving authority from the active editor or associated shot.

Recommendation: an editor-owned invocation of the existing modal, initially one
image/output only. Keep ordinary gallery generation available when the opt-in is
unchecked or cannot be prepared. Explicit checked approval must either persist
successfully before admission or fail visibly; no automatic fallback to an
unreserved promise. The chosen owner needs the existing session's validated
accepted basis and clean-dependency check. This does not require a new journal.

The question was submitted through the user-input tool during this worker turn.
No answer has been received as of this report. No source ambiguity was resolved
by guessing a raw owner, approval, accepted base or operation host.

## Real ingress traced on the exact base

| Source | What it actually owns / missing binding |
| --- | --- |
| `src/tools/image-generation/pages/ImageGenerationToolPage.tsx:112,192` | Supplies project IDs to `useImageGenSubmit`; passes its handler to the real image form. Associated-shot selection updates gallery filters. It is not canonical occurrence approval. |
| `src/tools/image-generation/hooks/useImageGenSubmit.ts:11,34,46` | The hook accepts only `projectId` / `effectiveProjectId`; its real submission calls `createImageGenerationTasks(projectId, taskParams)`. It has no accepted basis, raw occurrence, explicit automatic policy, or outbox owner. |
| `src/shared/components/modals/ImageGenerationModal.tsx:24,46,62` | Another real caller of the same producer. Props are open/close/initialShotId; it uses selected project and task placeholders. No accepted-session input or explicit add-to-timeline option. Current callers are gallery/shot/image-upload surfaces, not an editor-owned invocation carrying a command session. |
| `src/shared/lib/taskCreation/imageGeneration.ts:264` | Real producer validates the typed one-prompt request, obtains the live capability, composes the canonical admission, and calls `createTask`. No placement approval or pre-POST reservation port. Multi-image output selection must also be explicit; choosing the first output is not an approval. |
| `src/shared/lib/taskCreation/createTask.ts:323,327,338,346` | Options are unused. Validates capability/input authority, allocates one in-memory UUID, then posts through the bridge with that key. There is no durable-before-submit hook; reopening the producer would compose again and allocate another key. |
| `src/integrations/astrid/taskRoutes.ts:73` | Rebuilds the closed admission envelope and serializes the task POST. A future reservation must freeze the exact final serialization, not merely save pre-normalized params or compose a second request. The returned projection includes run_id, but createTask currently returns only task IDs/status. |
| `src/tools/video-editor/hooks/useTimelineCommandSession.ts:59,114,239` and `commands/commitSession.ts:42,417` | Existing editor owns the validated accepted closure, authenticated scope and claimed durable outbox. Its exposed surface currently has move/label/history/retry operations; no image submission/placement approval bridge. Recovery only discovers ordinary intents/pending on this base. Adding a global active-timeline lookup would not establish explicit approval or original clean dependencies. |
| `src/shared/contexts/AgentChatContext.tsx:8` | Its editor context contains display/scope facts and element/live-scene adapters, not an accepted basis or placement authority. Task refs after admission cannot repair pre-admission approval. |

These are source findings, not a reproduced durability implementation. No current
passing behavior test was rewritten to expect lost/refused behavior.

## Reviewed sources and settled fence disposition

Read the requester continuation design in `app-automatic-placement-gap.md`,
`app-requester-synchronous-fence-review.md`, `app-requester-real-host-binding.md`,
`app-auto-native-port-independent-review.md`, the runtime media fence ACK,
`app-media-fence-ack-disposition.md`, and the latest callback independent review.

- Latest approved callback branch
  `tl/app-m2-auto-media-fence-ack-capture-enable-source`, exact App
  `47250bdf82ee49dcf212fe56e92ad5d79989ba24`, tree
  `fc390a827c56d8dcc943a09b6c9cebae79b9161f`.
  The independent review approves the two-file callback change only. The callback
  returns the original native commands after lifecycle checks. It delegates the
  original readClosure codec to its injected host; no production caller is supplied.
- Corrected native capture is App
  `ca51f422597adea38e5f5bd981b7f12fab38fff4`, native Agent
  `80f5149631bb2b08c0569a2a53192e14442991e7`.
- Requester synchronous-boundary repair independently approved at App
  `a103f3ca2e8e66f2837a85c0ddd007962eca66ac`.
  Its literal synchronous live-host and claim checks cannot be replaced with
  cached handshake equality or ad hoc clients.
- Runtime ACK is against published
  `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.
  Exact five-field selected-media capture plus transactional acceptance recheck
  is sufficient for normal completed media. **There is no missing-media-guard
  blocker here.** Do not add producer.guard, guessed proposal/provenance/epoch
  fields, new DTOs or a pin refresh.
- Existing inactive browser operation-host source is
  `tl/app-m2-proxy-operation-browser-host` /
  `be27b45066947e920cda8da67991976b432ccb33`. It is not production-bound in this
  base and was not copied/activated. Source-only host review is not a reason to
  turn on automatic dispatch or bind the ambient global bridge as that host.

After the ingress ownership answer, port only the required approved requester,
placement outbox and native capture paths; manually preserve the base's current
root/renderer/pins. Do not import the callback branch's older entire cohort or
whole bootstrap/render outbox changes just to obtain its placement methods.
No settled PLAN decision was contradicted or changed.

## Exact executed tests

Working directory:
`/home/user/work/wt/app-m2-auto-production-submit-binding`.
The worker's ignored node_modules symlink was temporarily pointed to the existing
read-only `/tmp/app-coherent-deps12/node_modules`; no contents in that or any
shared dependency/runtime/venv were changed. A private runner only establishes
the config's __dirname; runner config loading and --no-cache avoid shared caches.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-auto-production-submit-binding/notes/runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/shared/lib/taskCreation/createTask.test.ts src/shared/lib/taskCreation/imageGeneration.test.ts src/shared/lib/taskCreation/imageGeneration.hosted.test.ts src/tools/image-generation/hooks/__tests__/useImageGenSubmit.test.ts src/tools/image-generation/hooks/__tests__/useImageGenSubmit.hosted.test.ts src/shared/components/modals/ImageGenerationModal.hosted.test.tsx
```

**PASS: 6 files / 45 tests, exit 0, 8.33 seconds, start 2026-10-20 12:20:37 UTC.**
Log: `workers/app-m2-auto-production-submit-binding/notes/producer-baseline.log`.
These are unchanged baseline tests. createTask exercises its actual admission
logic with a mocked bridge; image producer tests mock createTask; UI hook tests
mock the producer. They do **not** prove a composed durable submission binding.

```sh
git diff --exit-code
git diff --check
git status --porcelain=v1 --untracked-files=all
```

All passed, exit 0, empty output before report publication. No build/temp output
in the worktree. No full, build, tsc/compiler-API, browser, socket, install or
central test-service request; no git commit/merge/rebase/checkout/push/ref change.

## Concrete unrun delivery and activation gates

All of the brief's new binding acceptance cases remain **UNIMPLEMENTED / UNRUN**:
actual producer plus injected durable reservation failure/delay must produce zero
task POST until transaction complete; reopen must reuse exact request/key/IDs;
identity/project changes must refuse the old continuation without rewriting it;
unchecked/anonymous requests must not acquire approval. Original accepted
readClosure, raw owner/anchor/lane/fallback and native policy must survive reload.
Dirty/unacknowledged dependencies must remain retained and visibly refused.

A production host must bind completion/reconnect, original immutable reads and
verified media to the same authenticated operation lifetime and validated commit
adapter. If unavailable, persist the real prepared approval and show pending/
unavailable while keeping asset/manual use, with no Placed label or silent switch.

Before activation: matched Agent905 / normal013 tuple, actual gate approval,
real native acceptance and canonical reload, guarded undo/redo and strict ABA,
lost admission/commit ACK and restart/exact retry, actual task/output/media
invalidations, duplicate completion, and zero legacy writer traffic. Browser/
socket proof belongs to a separately authorized central test-service run. No
retrospective anonymous placement, pin refresh or writer retirement was performed.

BLOCKED and KEEP are written for the orchestrator's answer; DONE is deliberately
absent. This report is the only deliverable; the requested production binding is
not claimed complete.
