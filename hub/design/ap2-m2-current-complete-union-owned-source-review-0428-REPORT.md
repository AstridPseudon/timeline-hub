# App2 M2 complete-union source review

## Disposition

**BOUNDED SOURCE ACK; not a complete App2 union ACK.** The ordinary,
track/order, element/PARAM, transcript-carrier, and serializer source shapes
retain their individually reviewed semantics within the boundaries below.
Two concrete App-side gaps remain: project-data `remove` is not representable
by the current carrier, and the corrected after-anchor source is unavailable
on the assigned App tree. No donor source was substituted for the missing
after-anchor helper.

This is source compatibility only. It is not a freeze, generation, pin,
public-adoption, consumer-activation, or native HTTP claim.

## Exact Agent source identity

The committed Agent handoff and independent union review identify the same
source:

- commit: `5672d2b7deee2bfe2ab375fd6db5fc35a192591d`
- committed tree: `6dd13b552c4f07fff5586b1fa772bdbdf64accba`
- schema: `astrid/core/timeline/schema/edit-command.schema.json`
- raw schema SHA-256: `daec2964bb589d2087409446f99b84cfe9d6fb62b0b3af25e37363a78b170514`
- canonical formatted schema SHA-256:
  `9c05ec496e957548fe4656ca655a67a7b936ff4f220bdedae474a680e6d32eb9`
- inventory: 62 definitions, 36 closed operation clauses
- activated callers: none

The Agent source review is APPROVE source-only. Its compact reconstruction
preserves the frozen floors `84fc0863`, `65bb68ac`, `27f2e3ed`, `39211e63`,
`613123b2`, and `6ba7b51`. The exact Agent conformance evidence recorded in
that review is 25 schema-union, 39 composed-schema, 79 movement, 91 parent
media, and 69 reference/order/timing tests passed. No Agent source was
replaced by an older schema.

The assigned App source was clean at:

- commit: `6e267027137f11288a8e20ee8cf226209be60408`
- tree: `b65cd465f0865c77ceb73d29f105c7d6d2c18b53`

## Carrier findings

### Ordinary / serializer

Bounded ACK for the existing ordinary carrier shapes. The current generic
capture classifies the complete patch before owner resolution, refuses mixed
supported/unsupported batches atomically, executes accepted members against
one copied authored bundle, preserves public operation order, and assigns
sequential record ordinals and derived-write causes. The ordinary helpers
retain the existing guarded `clip.move`, `clip.set`, `clip.trim`, `track.set`,
and bounded structural paths; unsupported families remain visibly refused or
on the existing writer.

`serializeResolvedTimelineEdit` remains a whole-document serializer with
three current production consumers (`runner.ts`, `useTimelineCommit.ts`, and
`timeline-mutation-engine.ts`). Its current source preserves opaque authored
roots and refuses when a verified raw serialization basis is missing. This is
the honest source boundary: no serializer deletion or native-consumer cut is
claimed.

### Project-data

The replace/null/opaque/sibling/guard behavior is source-compatible and
preserves ordered batch recording. The exact mismatch is:

- Agent `ProjectDataWriteArgs` accepts either
  `{target, key, value, mode: "replace"}` or
  `{target, key, mode: "remove"}` with no `value`.
- App `projectDataMember.ts:111-124` only accepts `key,value` with optional
  source mode `merge|replace`; `validateArgs` at lines 126-134 requires
  `target,key,value,mode` and only allows native `replace`.
- The capture at lines 317-326 always emits a native `replace` command with a
  value. There is no closed App carrier for Agent-valid `remove`.

The existing focused source tests intentionally cover replacement and refusal
of unsupported deletion; that refusal must not be re-described as support for
the Agent union's remove clause.

### Track/order

Bounded ACK for `track.reorder@1`: the App helper selects the complete
`parent/collection:track` membership, requires `expected_order` to match the
current complete same-owner permutation, writes only the virtual
`parent::track_order` carrier, and reorders existing raw rows without
rebuilding opaque fields. Lane-bearing input remains refused, so the
data-lane/public trim path is not conflated with this media-only shape.

### Element / PARAM

Bounded ACK for the current v1 `clip.set-element` and `clip.set-params`
carriers. The source retains stable target identity, occurrence/source
bindings, both `elementRef` and retired `element_ref` reads, explicit clears,
unchanged writes, and opaque PARAM siblings. Asset-backed PARAM capture reads
the four guarded registry leaves (`media_id`, `object_id`, `digest`,
`content_digest`). Selected project-pack element/PARAM paths refuse without
authoritative Agent schema capture; no App pin or schema authority is
invented. The existing `elementGesture` caller was not changed.

The selected-PARAM authority helper also remains fail-closed: incomplete,
ambiguous, cyclic, out-of-order, or unavailable accepted history refuses while
preserving the draft, and direct authority is taken from the original
accepted record rather than a latest catalog/display pin. Production wiring,
activation, and restart qualification are outside this source review.

### Transcript association

Bounded ACK for the separate dormant App helper, not as an operation in the
Agent 62-definition union: a direct probe found no `transcript.associate`
clause in the Agent schema. The current App helper bytes match the previously
approved dormant source:

- `transcriptAssociateCapture.ts` SHA-256
  `4d4b289588c5f847ae9d0dea3290e3f6bc19dcba356a8febb6a3a94cc82830bc`
- test SHA-256
  `56c1c0bb0393ec2275caf6f76af07b207c23d873e1551f687de9393364b31516`

It requires the nested `parent.config.bundle` carrier, refuses legacy root
planes and `sourceItemsBySchemaRef`, writes the canonical
`transcriptReferences`/`itemsBySchemaRef` planes, and reconciles generated
captions from provenance/source-item identity rather than a raw clip asset.
Exact new/prior document pins are required. No live caller was found outside
its test; no host, provider, session, serializer, or pin activation is
claimed.

### Parent after-anchor

**Unavailable on the assigned App source tree; no ACK.**
`parentAfterAnchorCapture.ts` and its test are absent from App commit
`6e267027137f11288a8e20ee8cf226209be60408`; only the ordinary
`parentClipAddCapture.ts` support file is present. App2 STATUS records the
corrected after-anchor packet as pending HOME merge and separately records the
Main-compatible missing/null-hold requirement as still open with Agent.

The prior after-anchor report's four Agent parity cases, six refusals, and
strict missing/null refusal are existing evidence for that donor packet only;
they do not make the absent helper present here. The existing `media.ts`
`afterClipId` path is a legacy duplicate/fallback path and was not substituted
for the missing native carrier. Consequently raw recorder ordering and
missing/null-hold refusal are not ACKed for the current assigned tree.

## Status context and scope boundaries

The current Agent handoff is source-only with no activated callers. App2
STATUS is M2 OPEN: ordinary snapshot fallback remains live, the transcript
helper is dormant, after-anchor is pending HOME merge, and missing/null hold
compatibility remains open with Agent. Latest HOME/App handoffs confirm no
dormant SWAP/after-anchor activation and no second full run after the
zero-collection wrapper failure. HOME group/public trim and Runtime DTO
semantics were not reviewed here.

Changed live callers: **none**. No App production source, tests, refs, or
shared dependencies were changed.

## Verification and evidence

No tests, installs, full suites, browser journeys, localhost/live-socket runs,
or generated artifacts were run, per task scope. Read-only probes included:

```text
git -C /home/user/work/agent rev-parse 5672d2b7deee2bfe2ab375fd6db5fc35a192591d^{tree}
=> 6dd13b552c4f07fff5586b1fa772bdbdf64accba

git -C /home/user/work/agent show 5672d2b7deee2bfe2ab375fd6db5fc35a192591d:astrid/core/timeline/schema/edit-command.schema.json | sha256sum
=> daec2964bb589d2087409446f99b84cfe9d6fb62b0b3af25e37363a78b170514

git -C /home/user/work/agent grep -n 'transcript.associate' 5672d2b7deee2bfe2ab375fd6db5fc35a192591d -- astrid/core/timeline/schema/edit-command.schema.json
=> no match

rg -n 'captureTranscriptAssociation|finishTranscriptAssociation|transcriptAssociateCapture' src --excluding the helper and its test
=> no live caller
```

Existing reports were used without replaying unchanged suites: Agent union
review evidence above; App ordinary, track, element/PARAM, transcript, and
serializer focused evidence; and the prior after-anchor donor evidence with
the current-tree availability limitation stated above.

## Recommended next steps

1. Add/review the corrected after-anchor helper on the current HOME/App
   integration, retaining atomic missing/null-hold refusal until Agent closes
   that requirement.
2. Add an App project-data remove carrier or keep the current explicit refusal
   and document the App source boundary before any union adoption decision.
3. Keep the serializer and ordinary fallback routes live until producer,
   preview, outbox/retry, and native consumer qualification are separately
   complete.
