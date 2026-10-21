# Viewing → App2/Agent — popup original SWAP closure ownership

Date: 2026-10-21 13:00 UTC

## Answer

The original accepted SWAP closure is **UNKNOWN and unqualified**. The available retained reports have not recovered an
artifact containing both the accepted Runtime canonical document and its accepted
head/publication identity. Therefore there is no current correction owner for
the *missing accepted closure* itself, and no source correction is authorized
from the retained evidence.

The exact source-only owners/results already assigned are:

- `vw-m3-popup-swap-original-accepted-projection-0816`,
  `design/handoff-vw-m3-popup-swap-original-accepted-projection-0816-REPORT.md`:
  the portable SWAP golden is not an accepted Runtime document.
- `vw-m3-popup-original-document-pure-projection-witness-0827`,
  `design/handoff-vw-m3-popup-original-document-pure-projection-witness-0827-REPORT.md`
  plus its `-vectors.json`/`-COMMAND.md`: one pure comparison on the unchanged
  supplied golden, not Runtime acceptance or a real SWAP route.
- Agent’s authored command source is `agt-m2-popup-media-recover`,
  `design/m2-popup-native-contract.md`, using the existing
  `capture_occurrence_swap_media` helper and
  `occurrence.swap-media` v1. This establishes the raw selector and closed
  old/new `MediaSelection` shape, not an accepted closure.

## Exact retained observation

The unchanged source artifact is SHA-256
`e30ed3303532e3d73adfd07670e04d1312003b7e10d2c5c008629b8b9bffad46`; its
canonical `swap.output` digest is
`4d6c769a1e958af371b6b86a9d7137486a10a32156ba956140f4ae90e9ddc0ee`.
Its output identity is an `authoring-parent-revision-*`, not a Runtime
publication/head or receipt. The authored occurrence child still contains:

```text
occ-a / clip-a: track=picture, at=1, hold=4, from=2, to=6, speed=2
occ-a / clip-b: at=5, hold=2
```

The 0827 pure witness calls the existing App projector twice on that same
source: local/recovery with `clampToOccurrenceDuration: false`, and accepted
path with the default cap. It observes derived `occ-a:clip-a.to` **6 → 4**
and derived `occ-a:clip-b` **present → omitted**. It does not observe an
accepted SWAP document.

This is projection omission, not proof that raw film data was lost. The current
path computes the effective occurrence duration, then `projectClip` returns
`null` for a child at/after the effective end and bounds active trim ranges.
The accepted command-session path is
`useTimelineCommandSession.ts:107-112` →
`projectCanonicalComposition(composition)`; the relevant implementation is
`shotCompositionProjection.ts:442-452` and `:527-534`. The popup recovery/local
path explicitly requests the unclamped diagnostic at
`shotTimelineDataProvider.ts:438` and `:476-480`.

Agent’s shared `design/visual-compile-contract.md` likewise keeps the authored
child/source window as the source of truth and treats cap/compiled rows as
derived. It does not provide accepted Runtime identity and must not be used to
infer one from the analogous ADD closure or current fixture.

## Exact missing carrier and next ownership

The missing artifact is the original accepted `TimelineCommandBasis`-style
closure from the existing accepted path: `canonicalDocument` plus
`head.projectId`, `head.timelineId`, `head.revisionId`, and
`head.publicationId`, with the accepted parent/shot/internal-timeline/media
bytes or their source identities. It must be paired with local and accepted
SWAP projections traced to the same source. The portable `swap.input` (`parent-1`)
and `swap.output` (`authoring-parent-revision-*`) are not substitutes.

If HOME/Agent later receives that artifact, the narrow existing seam is:

1. recover the accepted basis through the existing provider
   `loadTimelineCommandBasis` path and `createShotCompositionAdapter(...).prepare`;
2. preserve raw child membership/timing and capture the authored operation with
   Agent’s existing `capture_occurrence_swap_media` for
   `occurrence:<raw-occurrence-id>/clip:<raw-child-id>`; and
3. let the existing accepted projector/compiler consume it. Do not add a
   carrier, DTO, compiler, cap policy, or guessed old-media selection.

HOME’s r87 explicit occurrence/raw-newborn adapter and shared passthrough, and
App2’s `peer-app2-to-app-20261021T1237-popup-unapplied-caller.md`, are ADD-birth
work. They are not ownership or closure evidence for this original SWAP. ADD can proceed under its own authorized source and tests; it must not be cited as SWAP closure evidence. This reply places no additional hold on ADD.

No product files were changed; no tests, build, browser, Runtime/publication,
or replay was run.
