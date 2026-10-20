# Native automatic capture after Runtime ACK: independent review

**APPROVE the bounded source change. No blocking finding. Production binding and activation remain unqualified.**

Reviewed App `47250bdf82ee49dcf212fe56e92ad5d79989ba24` (tree `fc390a827c56d8dcc943a09b6c9cebae79b9161f`) against `b6a3632c15bb8f5c71946f683fa0b185892c4296`, 2026-10-20. PLAN was read first. Adopted the existing Runtime ACK in `runtime-media-completion-fence.md` and independent APPROVE in `runtime-media-fence-independent-review.md`; read `app-auto-media-fence-ack-capture-source.md`. No settled decision changed, product edit, new authority, or contract repair was needed.

## Diff and preserved behavior

Exactly two files differ: `nativePlacementCapture.ts` (+4/-7) and its test (+106/-23). The callback now returns only `{ commands }` after the existing original native read/capture and final synchronous `context.assertCurrent()`. It does not rebuild, filter, or translate any command claim. Complete native command golden hash remains `69f80c68b553835f2a689db01ef7c22759960e0585b178100e1ed1f1a0da7341`.

Exactly two obsolete missing-guard expectation groups become success:

| Previous expectation | Replacement checked |
| --- | --- |
| Successful native capture throws `task/attempt guard is unavailable` | Commands-only payload, unchanged native command hash and original continuation, one verified read |
| Successful requester capture persists missing-guard conflict, never builds/sends | Image/video durable intent and linkage at original head; exact pending request before send; lost fixture ACK, reopen and identical retry; fixture acceptance and duplicate recovery |

The entire `readNativePlacementCapture` stage is byte-identical to base. All pre-existing read-stage assertions before the first replaced test are byte-identical. The final pre-existing requester identity-interruption test changes only storage-factory plumbing. `placementRequester.ts`, `commitOutbox.ts`, `autoCapture.ts`, requester/outbox tests, generated client/types, package and lock files are byte-identical to base. Independent byte comparisons are retained in worker `notes/audit.log`.

Original explicit approval/policy, autoApprove, owner, anchor, lane, literal fallback and allocated IDs still match the saved requester input. The original locator/project, exact five-field pin, original head revision/publication, canonical scope and raw parent revision checks remain. Frozen/detached original inputs and the injected original-read closure are preserved. The adapter still delegates decoding/binding of `readClosure` to the host's `OriginalPlacementRead`; these trusted fixtures do not establish a production closure codec or authentication of arbitrary caller data.

All awaited reads retain before/after identity and claim checks, including rejecting reads; the callback retains its final synchronous check. The requester still checks its authenticated synchronous lifecycle and live claim, and the outbox checks persisted owner generation and lifecycle at mutations. Existing refusal cases remain passing; no skip, xfail, deletion, or weakened lost-behavior expectation was introduced.

## Actual schema and durable recovery trace

- `OutboxPlacementCapture` returns finite JSON. `{ commands: EditCommand[] }` fits it directly; `resolved`, `expect`, `authorship`, `reads`, `selections`, `bindings`, and `created` stay in each command. Capture records/after-bundle are not wire fields or extra commit authority. The requester does not require the session's separate preview/before/after payload fields.
- `capturePlacement` first commits the original media pin with strict IndexedDB durability. After capture it rechecks identity/claim, then atomically appends `{ basis: { head: original.input.head }, readyBase: original.input.head, payload }` and links the continuation's `placement.intentId`. No capture payload is sent before this transaction completes.
- `dispatch` uses the original intent and base, serializes the built request once and allocates one retry key inside another strict transaction. `transaction` resolves on `complete`; only afterward may transmit run. Reopen takes `pending.request` directly, without build/capture/read/selection refresh. Source tests compare the full request, including method/path/body/key, both before send and after reopen.
- Actual requester/outbox outcomes are `{ kind: 'accepted', head, value }`, `{ kind: 'rejected', error }`, or `{ kind: 'retry', error }`. Acceptance atomically stores head/value, marks the linked placement accepted and removes only its acknowledged prefix/pending request. Capture refusal retains a continuation conflict; commit rejection retains the intent conflict plus rejected exact pending request. Recovery returns conflict before recapturing or retransmitting. The new capture/commit refusal tests alter metadata/pin and reopen twice, requiring complete record equality apart from claim generation.
- The fixture accepted `value: {}` is valid local JSON, **not** a Runtime acceptance envelope. Production `RuntimeDataProvider.commitTimeline` validates the real `CommitAcceptedMutation` and canonical closure, derives `accepted.revisionId` from `data.accepted_revision_id` and `accepted.publicationId` from `receipt.receipt_id`, and returns `TimelineCommitResult` with response/canonicalDocument/graph/receipt. The existing session shows the accepted-outcome mapping. This callback diff does not bind that transport or prove receipt/reload/undo behavior.

The Runtime `2c4ac180` source was read with `git show`: `RequestCommitPort.selected_media` requires a declared selection, retains the exact value, and `validate` re-reads it; `MediaReads.selected` requires all five fields. Store acceptance revalidates under its mutex/transaction. The reviewed ACK establishes the normal-API lifecycle authority argument; no Runtime suites were repeated here. No `producer.guard`, proposal pin, task/attempt epoch, new authority hash, DTO, endpoint, or journal was added. Existing content/catalog digests remain unchanged.

Whole-repository source search finds no non-test caller of either native capture export beyond its own definition/internal call. `createPlacementRequester` likewise has no production invocation. UI/task submission stays inactive.

## Exact independent tests

Working directory: `/home/user/work/wt/app-m2-auto-media-fence-ack-independent-review`.

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-auto-media-fence-ack-independent-review
D=/tmp/app-coherent-deps12/node_modules
node --require "$W/notes/runner.cjs" "$D/vitest/vitest.mjs" run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/nativePlacementCapture.test.ts src/tools/video-editor/commands/placementRequester.test.ts src/tools/video-editor/commands/commitOutbox.test.ts
```

**PASS: 3 files / 189 tests (43 adapter, 93 requester, 53 outbox), exit 0, 4.21s.** Log: `$W/notes/targeted.log`. This is the requested narrow rerun, not the earlier nine-file/642-test run.

```sh
node --require "$W/notes/runner.cjs" "$D/vitest/vitest.mjs" run --config "$W/notes/review.config.ts" --configLoader=runner --no-cache --maxWorkers=1 "$W/notes/interruptions.test.ts"
```

**PASS: 1 file / 5 independent private probes, exit 0, 1.51s.** Final log: `$W/notes/interruptions-final.log`. An initial run also passed all five; only an irrelevant fixture assertion/import was subsequently removed from the private probes. Private fixtures copy the reviewed test helpers and import this worktree's actual product code; no repository tests or product code were edited. The probes cover:

- Identity and claim interruption in the microtask between the native read stage finishing and callback return: final synchronous assertion refuses both.
- Successful native capture and late refusal followed by identity invalidation before storage consumes them: neither intent nor semantic conflict is persisted; no build/send; restoring authorization recovers the original approval/pin/IDs.
- Native capture held across release of its claim: late payload cannot append; authorized recovery uses the original bindings and sends once.

These are trusted in-process fixture probes, not browser crash, server acceptance, or security qualification. Authorized recapture after an interrupted, unlinked capture is intentional; genuine persisted capture/commit conflicts are not recaptured.

```sh
git diff --check b6a3632c HEAD
git status --short
```

**PASS, exit 0; worktree clean.** No repository changes or build/temp output. Private12 dependencies and shared node_modules/venvs/runtimes were read-only; runner config loader and `--no-cache` avoided shared caches; the private config additionally points cacheDir into this worker's notes. No full/642-test repeat, central request, socket, browser, build, tsc/compiler API check, install, git mutation or KEEP marker.

## Next production binding and limits

Proceed to a separately scoped production host/ingress task: bind same authenticated host verified-media reads and synchronous lifecycle invalidation; decode the explicitly authorized saved approval/readClosure and inject its original document or exact immutable raw reads, without resolving a newer head. Connect the original commands/base/exact retry identity to the existing validated commit adapter and its actual outcome schema. No second authority mechanism is needed.

Then qualify a coordinated Agent/schema/Runtime/App tuple with real native image/video acceptance, acceptance-time media invalidations, canonical reload, undo/redo/strict ABA, zero legacy writer traffic, lost ACK/process restart and visible refusal/draft retention. Socket/browser work belongs in the central test service under a separately authorized brief. Pool promotion, parent births/extent growth, owner short-video/style requirements and the independently reported Runtime repeat-generation publication defect remain inherited follow-ups, not proven by this source change.

No blocker to this independent source review. Approval does not activate production or close those gates. Report and private notes are outside the repository; commit message and DONE are in the assigned worker directory, with no KEEP.
