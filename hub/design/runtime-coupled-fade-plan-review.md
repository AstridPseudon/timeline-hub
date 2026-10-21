# Runtime coupled fade plan review

Date: 2026-10-21 UTC

## Verdict

**ACK — existing-carrier FIT for a future source cohort.** The proposed
coupled `effects.fade_in` + `entrance` and `effects.fade_out` + `exit` values
fit the existing `clip.set` command, commit request, provider context, and
recording envelopes. No Runtime DTO field, ABI change, endpoint, or second
writer is required.

This is a source-contract ACK only. It does not claim that the current Runtime
bundle, current provider installation, App callers, native clients, or public
support already accept or emit the pair.

## Sources checked

- Ordinary carrier: Agent `ba21beffd177e7d80a5b839bde5a9e25b97235c2`, the
  ordinary `clip.set` source staged on Main-current.
- Reviewed standalone effect leaves: Agent
  `097c68a9fe3641183372657b5f71cbdcb0a5b326`, tree
  `55da544815c3ef9cc33942b549e097d77294d3a0`, especially
  `astrid/core/timeline/schema/edit-command.schema.json:2687-2759`,
  `astrid/sdk/timeline/_clip_scalar_commands.py:90-151`, and
  `tests/editing_conformance/test_recipe_clip_scalar_fields.py:212-363`.
- Main visible producer reference: App/Main source at Main commit
  `860d43b331fb4422b16bc0dbd7b08666a0c766a0`, tree
  `ea4eabb8eb469df63fd1d515f84982d85b2f14cc`,
  `src/tools/video-editor/runtime/element-adapter.ts:334-344`.
- App semantic producer reference: App commit
  `f6e3fa14c4e95090f10735b2163aced88e77bb2d`, tree
  `58113372d9e028aa71731fb0fd645ce6b241b554`,
  `src/tools/video-editor/commands/semanticGestures.ts:159-205` and
  `src/tools/video-editor/runtime/element-adapter.ts:550-563`.

## Carrier fit

The Runtime contract puts `CommitRequest.commands` through the existing
`AgentCommandBatch`/`CommandBatch` array and `EditCommand` envelope
(`contract/schemas/timeline-commit.json:122-168, 45-46`,
`contract/schemas/edit-command.json:827-928, 1877-1903`). `EditCommand.args`
is finite JSON and the registered operation closes its own keys; the proposed
objects and paired clear strings therefore need no transport-level field.
The request remains the ordinary `/v1/projects/{project}/timelines/{timeline}/commit`
path (`runtime_protocol/timeline_commit_port.py:56-76`,
`service.py:2435-2480`).

The provider seam is unchanged: startup validates the existing
`astrid-v1`/interface-version-1 provider signature and contract digest, then
the coordinator invokes `provider.commit(provider_context, port)` with the
detached request context (`timeline_commit_provider.py:16-18, 55-93`,
`timeline_commit_execution.py:69-89`). Nothing in that seam enumerates fade
fields. A future cohort only needs its normal registered `clip.set` operation
schema and Agent handler to agree on the new closed shape.

The current Runtime installed schema is intentionally not evidence of current
support: `runtime_protocol/schemas/timeline-commit-bundle.json:659-707` still
closes `ClipSetArgs` to ordinary `hold`/`asset`/`transition`, and the current
typed aliases in `runtime_protocol/timeline_commit_types.py:118-129` are the
same ordinary floor. That is a future source-cohort admission item, not a
carrier/ABI mismatch in this review.

## Shape and clear rules

The plan is unambiguous if the existing `values`/`clear` envelope is extended
as stated:

- numeric fade-in set: `values.effects.fade_in` plus
  `values.entrance={type:"fade",duration:<same seconds>}`;
- numeric fade-out set: `values.effects.fade_out` plus
  `values.exit={type:"fade-out",duration:<same seconds>}`;
- standalone `effects.fade_in`/`effects.fade_out` set and clear retain the
  already reviewed effects-only behavior;
- a coupled clear is the two clear entries together:
  `effects.fade_in` + `entrance`, or `effects.fade_out` + `exit`;
  `entrance` or `exit` alone is refused, while an effects-only clear remains
  standalone;
- set/clear overlap is refused before mutation. The two independent pairs may
  be present in one command when each pair is complete.

This uses ordinary JSON objects and arrays only. It creates no IDs, introduces
no operation, and does not require a second provider or writer.

## State, order, inverse, and rebase

The reviewed `097` source already proves that an effects object is a bounded
numeric leaf patch, refuses ordered effects arrays/non-object parents, retains
opaque effects siblings and insertion order, and records exact nested tagged
states. Its focused tests cover absent, present-null, empty, opaque sibling,
clear, inverse, strict ABA, and disjoint-leaf rebase cases
(`test_recipe_clip_scalar_fields.py:212-363`). The same recorder can carry the
two coupled writes: one top-level `entrance`/`exit` write and one nested
`effects` leaf write, with reads for the original `entrance`, `effects`, and
`exit` states. Exact absent/null/present values remain representable in the
existing `AgentState` envelope; inverse can restore both prior containers and
their order, and the existing guarded intervening-write checks cover both
touched addresses.

Forward coupled set should be understood as replacing the selected
`entrance`/`exit` value with the closed Main pair while preserving unrelated
effects siblings. Exact prior `entrance`/`exit` content is an inverse concern;
the plan must not imply that opaque fields inside those replaced slots are
preserved by the forward Main-shaped set.

## Main/App semantic boundaries

Main’s cited adapter writes the numeric effects leaf and the matching
`entrance`/`exit` object, uses seconds, and leaves an omitted side unchanged
(`element-adapter.ts:334-344`). The App semantic producer captures all three
original states, rejects an effects array, and currently emits `clip.set-fade`
(`semanticGestures.ts:159-205`); its adapter preserves that coupled command
before save (`element-adapter.ts:550-563`). Thus the future `clip.set` pair is
the right producer-to-provider translation target, but the cited current App
producer is not evidence that it already emits it.

Two qualifications are required:

1. Main’s typed fade action validates finite non-negative numbers only. The
   App semantic producer separately admits `null` as a present-null state and
   uses `clear` for absence. If the future source cohort preserves that
   present-null behavior, it is a separate App/semantic-consumer requirement;
   it must not be certified as Main typed-action parity. The pair must carry
   null on both corresponding fields, or clear both, so null and absent do not
   collapse.
2. The Main adapter’s raw spread normalizes an existing effects array to an
   object, whereas the reviewed Agent/App semantic carrier refuses arrays and
   leaves the legacy fallback in place. Array refusal is therefore not a Main
   raw-action claim; it is the explicit carrier/producer compatibility rule in
   the plan.

## Non-claims

No plan code, Runtime schema, DTO, provider, App caller, public/native client,
activation, pin, generation, or release was changed or certified. No full,
socket, browser, renderer, or generation suite was run. The source evidence is
sufficient for this carrier verdict; no scratch compatibility check was needed.

