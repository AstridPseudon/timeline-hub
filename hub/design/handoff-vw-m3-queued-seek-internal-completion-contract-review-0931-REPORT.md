# Queued-seek internal completion seam review — APPROVE

## Verdict

APPROVE the exact r39 contract-only hunk. It is the smallest adequate internal
shape: add one optional `seekComplete` indication to the existing
`RemotionPreview` `onTimeUpdate(time)` callback. Do not add a callback channel,
request identity/counter, clock, public Player API, wire/DTO/store field,
tolerance, or source-window/fps change. The proposal remains UNAPPLIED and no
product source was changed.

The bit is unambiguous only with the following producer meaning, which is the
required Viewing implementation contract:

- `true` is emitted only on the callback that consumes the latest surviving
  mailbox seek's frame feedback, or on an explicit callback for a same-frame,
  clamped, or otherwise no-frame-change completion.
- A feedback for active A is non-completion when newer B is queued. Mailbox RAF
  dispatch of B is also non-completion. B's frame-30 feedback is the completion
  in the required A→B witness.
- No newer request may remain when `true` is emitted. Coalesced/superseded
  requests complete through the surviving latest request; config-deferred
  requests remain held until the matching config is applied; invalidation and
  unmount clear/cancel the producer's outstanding completion state without
  leaving the consumer held.
- The callback's `time` remains the producer's existing feedback/authored value;
  the App hook must retain authored values and must not normalize them to frame
  time. For a no-frame-change completion the consumer suppresses the callback's
  time before releasing the guard.

The App consumer must use `seekComplete`, not callback arrival, to release the
existing timeline-origin carrier. It must not retain the old RAF-expiry
assumption, and a prior drag RAF must not clear a guard established by a newer
click/final release. Final release remains unconditional. Ordinary later
preview feedback is accepted after the one `true` completion.

## Required witness

At fps `30000/1001`, authored A=`0.5` then queued/final B=`1` must observe:

1. A is dispatched; B is pending; carrier held.
2. A frame effect occurs before B dispatch: frame 15 feedback is `0.5005…`,
   non-completion; carrier remains held.
3. Mailbox RAF dispatches B as frame 30; still non-completion.
4. B frame-30 feedback is `1.001`; callback carries `seekComplete=true`, its
   time is suppressed, then carrier releases.
5. Later ordinary frame 45 feedback (`1.5015…`) is accepted.

The same producer contract must cover coalescence, same-frame/no-op completion
without a new `frameupdate`, deferred config, unmount, and drag-RAF versus newer
final-click ordering. These are implementation acceptance criteria, not changes
to the proposed seam.

## Ownership and exact sources

- Producer owner: Viewing, in App's Viewing-owned preview/player surface:
  `src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx`,
  current HOME line 109 callback and lines 302–304 frame forwarding, mailbox
  lines 319–379, unmount cleanup lines 435–440.
- Consumer owner: App editing, through the existing
  `useTimelineSync`/`useTimelinePlayback` callback carrier. The public
  `PreviewHandle.seek(time): void` and Player event contract remain unchanged.
- HOME: commit `33b4a86cfdc2ac2ee63b069c225ae465d1f35656`, tree
  `fd345b29c30460d934c096e51ba01447bbb6e4d4`.
- Pending r38: commit `ab938b4beacc02419de7293dfa09190956b9d0ba`, tree
  `c3722bfb0f29fb1770512de1c00d4df3d74c5431`.
- `RemotionPreview.tsx` blob is identical on both refs:
  `557003fcaa020b9f475784e583f7d1b0225a5374`.
- `useTimelinePlayback.ts` blob is identical on both refs:
  `ebe95977fbd0c000c86da4fb2f083580eadb54be`.
- Proposal:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-app-split-viewing-completion-contract-r39-UNAPPLIED.patch`, SHA-256
  `00be197d79a8405b3533390b8ec0bc511bd704cd231f5e2eae3a570a5a27308d`.
- r39 report SHA-256:
  `840a948667f81e3d91952d722f1badb10a8f644ed3f5e7a5f690ba2a2c27242f`.
- 0817 counterexample report SHA-256:
  `c7758a97f8a0f8728384a5560232fd27609c1035fe0e7b3f1075dec458f8870d`.

## Evidence and limits

PASS, run in this review:

```sh
git apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-app-split-viewing-completion-contract-r39-UNAPPLIED.patch
git status --porcelain=v1
```

The patch applicability check passed and the assigned worktree remained clean.
The existing 0817 scheduler witness and targeted run were reused unchanged as
requested: the report records the real React/Remotion ordering witness and
`vitest` result of 2 files / 127 tests passed. No new scheduler witness was
needed because r39 changes the causal producer contract rather than replaying
the already-established failure.

Not run: product implementation, browser/mounted split, physical playback,
full/central suites, broad replay, install, build, live sockets, or native
tests. Approval is for the internal seam only; the producer and consumer still
require a new executable candidate and its focused regression before merge or
activation.
