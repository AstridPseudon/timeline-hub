# Queued seek completion: stopped at the ownership boundary

Disposition: BLOCKED. No repository source or tests changed. This is the task's
explicit missing-completion-identity stop condition, not a request for generic
permission. Viewing owns the completion producer. No corrected seek candidate
is available for merge or mounted qualification.

## Exact source

Worker: /home/user/work/wt/app-m2-split-queued-active-completion-cause-fix-r39

- Inspected HOME base: `33b4a86cfdc2ac2ee63b069c225ae465d1f35656`.
- HOME tree: `fd345b29c30460d934c096e51ba01447bbb6e4d4`.
- Finished pending r38: `ab938b4beacc02419de7293dfa09190956b9d0ba`.
- r38 tree: `c3722bfb0f29fb1770512de1c00d4df3d74c5431`.
- RemotionPreview.tsx is byte-identical in HOME and r38: SHA-256
  `3bd5cddce54f10e0b75c28aab7ddcea9b4f1c860508ad24bec4b7c0679a5a902`.
- useTimelinePlayback.ts is also identical between those refs.

The r38 branch was read with git show/diff only. Its rejected hook was not
ported onto HOME: doing that would knowingly add the already-rejected latch
clear. The relevant completion seam is the same on either allowed source.

Read PLAN.md and both requested Viewing rejection reports. Their counterexample
is confirmed by the current producer source, not inferred solely from reports.

## Why the hook alone cannot implement this

`RemotionPreview.tsx:23-24`: `PreviewHandle.seek(time)` returns void. It has no
completion callback, promise, request identity, or status accessor.

`RemotionPreview.tsx:109` and `useTimelinePlayback.ts:13`: the existing
onTimeUpdate/onPreviewTimeUpdate callback receives only a number. Nothing in
that number identifies active A versus queued B, completion, supersession, or
a config-deferred request. The hook does not receive the delivered fps or the
mailbox state either.

`RemotionPreview.tsx:302-304`: every public Player frameupdate is forwarded as
frame / fps. This discards the event's frame and supplies no seek lifecycle
information. Public Player frameupdate itself has only a frame, not a seek ID.

`RemotionPreview.tsx:331-375`: one active frame and one replaceable pending
request; the RAF clears active A and dispatches B. This is a command pacing
window, not an observed-frame completion boundary. Merely reading these refs
in the frame listener would also be insufficient: the RAF may clear the active
ref before that request's frame effect runs.

Installed read-only packages: React/React DOM 18.3.1, Remotion and
@remotion/player 4.0.509. `use-player-methods.js:44-60` schedules a frame state
change then synchronously emits seeked. `use-playback.js:300-302` emits
frameupdate from an effect dependent on frame. Same-frame seeks retain the
same state object; therefore a new frameupdate is not guaranteed. Synchronous
seeked is not observed React frame completion.

The original split fps is 30000/1001, not an integer 30. Authored B=1 maps to
frame 30 and feedback 30/(30000/1001)=1.001. Do not fix this by rounding authored
input, adding a tolerance, substituting fps, or counting requests: pending
requests coalesce and a same-frame request can produce no new frame effect.

## Exact minimal UNAPPLIED Viewing contract hunk

Absolute artifact:
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-split-queued-active-completion-cause-fix-r39/notes/viewing-completion-contract.UNAPPLIED.patch

The patch proposes one optional completion indication on the EXISTING internal
onTimeUpdate callback. No new callback channel, DTO, clock, store, request
counter, package API, or public Remotion Player change. It applies cleanly to
the exact current producer source. It is deliberately a CONTRACT-ONLY hunk:
it does not emit the indication and MUST NOT be merged as a working fix.
No executable producer implementation is claimed or qualified here.

Viewing must implement the producer in its owned mailbox before App can consume
this proposed indication. Required meaning: true on the callback carrying the
last timeline seek's consumed frame feedback (or an explicit no-frame-change
completion), false/absent while an active/latest queued request remains. The
hook will suppress that final callback's time first, then release its EXISTING
isSyncingFromTimeline carrier. A frame number/time match in the hook is not the
completion producer. This defines causal completion, not browser decode or
pixel readiness.

Required owner lifecycle details, which the current callback cannot supply:

1. A feedback with B queued is not completion; keep the timeline carrier held.
2. Mailbox dispatch B is not completion. Preserve B's outstanding completion
   state beyond RAF cleanup until its feedback is consumed.
3. B feedback with no newer request completes; suppress its quantized time,
   then release. Ordinary later preview feedback is accepted immediately.
4. If A and B are batched into a single committed frame, only the surviving
   latest seek completes. Do not wait for a nonexistent A event.
5. Same-frame and clamped no-op seeks must complete without waiting for a new
   frame effect. Replacing/cancelling a pending target, config deferral or
   invalidation, and unmount must not leave the carrier permanently held.
6. An old drag RAF must not release a newer final-release click's guard.
   App's existing drag guard clears by RAF, so click-only changes cannot claim
   preservation of final release in that interleaving.

App continuation after owner implementation: thread the optional indication
through useTimelinePlayback's existing callback type; retain exact authored
setCurrentTime(time); consume completion only after suppressing its echo; remove
RAF expiry as a completion assumption. Keep final-release click unconditional.
No consumer patch is applied before the producer contract exists.

## Required regression for the future executable candidate

Use the real preview mailbox and a Player boundary whose seekTo schedules
React frame state and whose frameupdate is emitted from a React effect; no
synchronous callback-as-completion substitute. Keep fps=30000/1001:

| Step | Required observation | Existing carrier |
| --- | --- | --- |
| Click A=0.5, then final release B=1 before mailbox RAF | Only A dispatched, B pending | held |
| Commit A's frame effect BEFORE mailbox dispatch B | frameupdate(15), time=0.5005 | held; no timeline write |
| Flush mailbox RAF | B dispatched as frame 30 | held |
| Commit B's frame effect | frameupdate(30), time=1.001 | suppress, then release |
| Later ordinary preview frame 45 | time=1.5015 | accepted |

Assert actual observed event order A-frameupdate < B-dispatch < B-frameupdate,
not merely that A/B seek calls occurred. Also retain authored currentTime=1
exactly, final-release dispatch, the alternate B-effect-after-RAF order,
coalesced same-frame/no-op completion, and drag-to-final-release sequencing.
No new regression was authored/run at this blocked stage; the existing single
hook test is a baseline, not evidence of a corrected ordering.

## Original split preservation

No split file was written, copied, edited or executed. HOME does not contain
the pending r38 split packet. Its original body read directly from r38 retains
SHA-256 `48938cfeffed2f3d6180206a4e7744c00979b31a14021f61c66ff98638f1f574`.
The packet remains in r38 unchanged; no replacement split body was introduced.

## Commands and results

PASS (exit 0), 1 file / 1 existing test:

```sh
TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-split-queued-active-completion-cause-fix-r39 ./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useTimelineSync.test.ts
```

`node_modules` realpath checked before running: /home/user/work/app/node_modules.
No dependency or default Vite cache was written; --no-cache was used. No install.

PASS (exit 0), applicability only, no patch applied:

```sh
git apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-split-queued-active-completion-cause-fix-r39/notes/viewing-completion-contract.UNAPPLIED.patch
```

PASS: git diff --check. git status --short: empty; repository remains unchanged.

Not run: corrected event-order regression (no executable correction), preview
component suites, browser/actual mounted split, build, full/central, tsc, install,
graph, live sockets or native/physical playback. No commit/merge/checkout/push.

## Next step

Viewing reviews the proposed internal completion contract and implements the
owner mailbox producer on the named source. Then App can implement and test its
hook consumer against that exact producer; return both source patches for NEW
code review. r38 is still rejected/held. Do not activate the split packet.
