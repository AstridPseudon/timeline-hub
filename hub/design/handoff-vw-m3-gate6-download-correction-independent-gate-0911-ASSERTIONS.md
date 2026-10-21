# Retained Gate6 assertion mapping

## New hunk review

| Location | Proposed change | Review |
| --- | --- | --- |
| `tests/e2e/timeline/viewing-parity/cases.ts:91` | `authoredOutput.file` → ``timeline-${fixture.timelineId}.mp4`` for admitted `output_policy.filename` | **Retain after correction**. This is the Runtime/App managed-output identity selected by `renderRouter.ts:741-743,879,963-969`, and matches the retained physical request. `format: mp4` and `destination: download` remain asserted. |
| `tests/e2e/timeline/viewing-parity/cases.ts:159` | `authoredOutput.file` → ``timeline-${fixture.timelineId}.mp4`` for `download.suggestedFilename()` | **Reject.** The normal UI result filename comes from `renderConfig.output.file` in `useRenderState.ts:785-788`; the picker and blob download both consume that value in `TimelineRenderControls.tsx:194-236`. This fixture's value is `frame-parity.mp4`. |

## Assertions retained one-for-one

The proposed patch leaves the following assertion groups unchanged:

- admission status, project, capability ID/digest, empty browser input IDs,
  timeline selector, canonical project/document/head/occurrence identity, and
  absent legacy `spec.inputs`;
- admitted task identity and Runtime task/snapshot authority, snapshot digest,
  media registry membership/order-to-digest comparison, task polling, and
  zero legacy writes;
- completed spec identity, exactly one MP4 managed output, task/project/media
  association, exactly one provenance sidecar, provenance canonical authority,
  renderer, composition ID, project directory, and provenance digest;
- result-dialog/player object URL, revision summary, direct download transfer
  observer, project scope, object identity, null download failure, nontrivial
  size, managed-output size, MP4 `ftyp`, and downloaded-byte digest;
- ffprobe video codec/size/fps/frame-count and audio codec/sample-rate/channel
  assertions;
- evidence recording, post-download fixture pinning, browser/toolchain source
  versions, and the physical negative/guard assertions elsewhere in the case.

Changing the browser filename to the managed admission filename would not be
assertion-preserving: it would replace the genuine UI naming contract with the
upstream admission contract without a browser observation proving that the UI
uses the latter.

## Grant/source/package/browser/physical comparison

- **Grant:** the retained 0856 grant/marker authorized exactly frozen d00; the
  proposed test-only patch was not in that source identity, so it cannot reuse
  that grant for a future edited physical run.
- **Source:** the relevant frozen d00 and current HOME `renderRouter.ts`
  naming path agrees. Frozen d00 and current HOME `useRenderState.ts` agree on
  the result filename source; current HOME `TimelineRenderControls.tsx` also
  retains the same picker/blob naming behavior.
- **Package:** no package, lockfile, capability, media, or output identity
  code is changed by the packet.
- **Browser:** the second hunk is contradicted by the source path used by the
  normal UI download. It was not reached in physical run 18439.
- **Physical:** 18439 is valid evidence only for the first admission mismatch;
  cancellation began before a valid download body, browser filename, frame,
  audio, parity, or negative-control result. The second case's cancellation
  errors are not independent evidence.

## Pure-regression evidence

The diagnosis worker recorded the frozen expectation as red (exit 1: received
`timeline-timeline-physical18439.mp4`, expected `frame-parity.mp4`) and the
proposed timeline-id pure expectation as green (exit 0). That pure regression
proves the admission-name correction only; it does not prove the proposed
browser-download hunk.

