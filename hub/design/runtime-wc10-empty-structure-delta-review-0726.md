# Runtime WC10 empty-structure delta review

Date: 2026-10-21

## Disposition

**SOURCE ACK, bounded to the reviewed Agent test spike, with one concrete
mismatch.** The new source preserves the intended raw-config semantics and
leaves v1 and the populated duplicate caller untouched. It does **not** prove
that a nonempty structural value is rejected before scoped writes: the test
helper writes the three scoped values into its in-memory `Recording` first and
only then applies `_require_empty_structure`.

This is not an activation or paired-product qualification. No Runtime DTO,
endpoint, provider ABI, schema generation, pin, App caller, or route change is
authorized by this review.

## Exact source identity

- Runtime base reviewed by the prior ACK: `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree `6abc2f117391de8e7e35c0283f575a002199894d`.
- Agent current integration: `1a7ec3762126aca322f26a5a3d06c1aa50d5d679`, tree `7a3291b58393ea6406ebc43498ca694bb636235e`; clean at review time.
- Prior raw-config spike: Agent commit `dfb97311ef54d1ef1706c2228bf2d84514c5b024`, tree `10089dba8ea9471a8b3a6f84ec65ef0b32dbbbec`.
- New empty-structural delta: Agent commit `2c93619bf784150fe9e5e319714d86a2aa4630b1`, tree `e10ad19072a4dd1e9cde219299e2f2ff526bca19`, parent `dfb97311…`.
- The new commit changes only `tests/editing_conformance/test_pristine_raw_initialize_proposal.py` (89 additions, 2 deletions). It is not an ancestor of current Agent integration; no uncommitted v2 source was found there.

The reviewed commit adds twelve known structural paths whose values may only
be absent, `[]`, or `{}`: `tracks`, `clips`, `occurrences`, `placements`,
`shots`, `groups`, `pinnedShotGroups`, `media`, `references`, `reference`,
`assets`, and `registry.assets`. Its six parametrized counterexamples show
that tracks, clips, groups, media, references, and registry assets would pass
through the unchecked open-config carrier with `created == []` and no parent
structural reads, then are refused as `unrecorded_birth` by the bounded helper.

## Boundary findings

- Raw preservation: ACK within this test-only source. The fixture retains
  `theme_overrides.visual.canvas`, explicit `background: null`, absent
  `background_scale`, opaque siblings, the opaque `[null, false]` array, and
  array order after bundle serialization/reload. The structural check is
  path-bounded and does not recursively reinterpret opaque metadata.
- Empty structural refusal: **mismatch on ordering evidence**. In the exact
  candidate, `_capture_raw_init_unchecked` calls `ctx.write` for `config`,
  `name`, and `slug` at lines 80–82, while `capture_raw_init` calls
  `_require_empty_structure` only after that helper returns at lines 109–113.
  Those are local in-memory writes and no product commit occurs, but the test
  cannot support a claim that admission happens before scoped writes. A future
  Agent handler must perform this check before any scoped write.
- v1: ACK unchanged at source scope. The delta touches no initializer,
  registry, command schema, generated artifact, or pin; the existing v1
  output recipe remains outside this candidate.
- Pristine/authenticated boundary: retained as a requirement, not newly
  proven by this spike. The candidate is deliberately unregistered and has no
  Runtime/provider/CAS implementation. The prior Runtime ACK remains the
  authority that the existing authenticated bootstrap publication, exact base
  pair, idempotency, CAS, and history boundary are sufficient as a carrier;
  no new raw escape hatch is inferred.
- Populated duplicate caller: live and unchanged. Agent integration and the
  candidate both carry `astrid/sdk/timeline_duplicate.py` blob
  `a780ebe877256c44b48ad89870c18df32fdb0916`; its
  `_duplicate` path at lines 194–200 still deep-copies the source parent
  config into `client.timelines.create_empty`. This is a separate populated
  duplicate workflow, not evidence that pristine `timeline.init@2` may accept
  nonempty structural births. Any future creator migration must preserve this
  positive separately.

## Tests and remaining boundary

No tests were run. The brief required retaining the prior 14+4 evidence by
exact source identity and prohibited replay absent a new concrete runtime
counterexample. No Runtime product source was changed.

Remaining work is Agent-owned v2 implementation and schema/registry agreement,
including a pre-write structural admission check, followed by paired Runtime
and App qualification of the original custom-canvas positive with authenticated
pristine/bootstrap/CAS, exact retry/restart, inverse, and later-edit refusal.
The original custom positive remains open; v1 remains frozen; the duplicate
caller and its populated behavior must not be cut or normalized.
