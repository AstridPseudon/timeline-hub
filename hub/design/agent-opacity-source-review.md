# Independent review: bounded clip opacity source

## APPROVE

Reviewed source tree `a53606703997434f8d9390a9f76fbe913bdd06e4` against base
`e010e6a3868e963471244491bb6672c3e4a5135e` and the proposal in
`agent-opacity-private-source-proposal.md`.

The proposal is bounded to the existing `clip.set@1` operation. The canonical
schema is SHA-256
`110165ab9f7e4be3e9766d06b5ceacab8c5e8c7cc12e7180929005b67bcc82d6`, with 56
definitions and 30 existing operation clauses. It adds no operation, pin,
generation, activation, selected-pack manufacture, or public artifact.

The contract matches Main’s producer in
`/home/user/work/app/src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.tsx`:
the slider reads `clip.opacity ?? 1` and emits `{ opacity: value }`. Agent
captures this as top-level `clip.set` `args.values.opacity`, not
`params.opacity`.

The focused conformance covers exact presence for absent/null/zero/existing
values, clear-as-removal, inclusive raw `0..1` validation, invalid/null/
non-number and out-of-range refusal, hostile `params.opacity` bypass refusal,
occurrence isolation, direct-neighbor preservation, inverse/redo, strict
A→B→A inverse refusal, and disjoint-parameter rebase. Existing capture guards
and v2/source identity machinery remain in the generic capture path.

The seven inventory failures were caused only by comparing the new candidate
bytes with frozen 613/392/6ba sources. The bounded test-only helper now strips
only the opacity schema property, clear enum member, and description wording
before reconstructing those historical bytes. No frozen fixture, hash, closure,
typed-carrier, v2, old-schema refusal, or assertion was weakened.

No counterexample found. Runtime/App ACK and any later generation or native
consumer activation remain correctly outside this source-only proposal.
