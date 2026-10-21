# Gate6 download-correction independent verdict

## Verdict

**REQUEST CHANGES — the proposed packet is not approved.**

The first hunk is source-backed: the managed admission filename is selected by
`defaultOutputFilename(fixture.timelineId)` and the retained physical 18439
request received `timeline-6c0e5aa0-99af-408a-af71-11a9e2e337de.mp4`, not the
fixture's authored `frame-parity.mp4`.

The second hunk is not source-backed. In frozen d00 and current HOME App,
`useRenderState.ts:785-788` stores the completed result filename from
`renderConfig.output.file`; `TimelineRenderControls.tsx:194-236` uses that
value for both the native picker `suggestedName` and the blob anchor's
`download` attribute. For this fixture the normal UI download contract is
therefore still `frame-parity.mp4`. The retained physical run stopped at the
admission assertion and never reached a valid browser-download observation.

The smallest correction is to change only `cases.ts:91` to
``timeline-${fixture.timelineId}.mp4`` and retain `cases.ts:159` as
`authoredOutput.file`. Do not create a competing patch in this review.

## Identity and custody

- Proposed patch: `handoff-vw-m3-gate6-download-name-source-diagnosis-0910-PATCH.patch`
- Exact patch SHA-256:
  `679aade875b0131225ec8afbbfbbcf6c0918087ef8cb27e5f851b5f19605afef`
- Frozen physical source: App d00a66134f330672ea7471dc69db38c1566d94cf,
  tree a8bf53d5d5e865aa88825bbc20f6f530bfbaa7ba.
- Current HOME source checked read-only: `/home/user/work/app`, branch
  `tl/integration`, HEAD 33b4a86cfdc2ac2ee63b069c225ae465d1f35656.
- Relevant frozen d00/current HOME naming functions agree on the managed
  admission default `timeline-${timelineId}.mp4`.
- The proposed patch remains unapplied. No d00 or 0845 source identity was
  reused with edited files by this review.

## Future physical-run source selection

Materialize a new private App leaf from frozen d00, apply only the approved
one-line admission-assertion correction, recompute the full App source and
graph fingerprints, and obtain a fresh manager grant/tuple for that new
identity. Keep Agent, Runtime, Composition, browser, package, and custody
identities from the approved packet only where the manager explicitly carries
them forward. Never reuse d00 or 0845 source hashes, grants, markers, or
physical evidence after editing the App source. No physical launch is
authorized by this verdict.

