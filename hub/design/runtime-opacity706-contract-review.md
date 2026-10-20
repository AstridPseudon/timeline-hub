# Runtime review: Agent bounded clip opacity source

Status: **BOUNDED SOURCE ACK**.

I reviewed the requested proposal and independent review against Agent
70652d26567797f1df5b14e3f2480249aef743e7, whose tree is
63229ef26d7b44faf765f074ff2029a1598a8d79, and whose canonical schema is
110165ab9f7e4be3e9766d06b5ceacab8c5e8c7cc12e7180929005b67bcc82d6.
No concrete mismatch was found in the bounded source contract. This ACK is
for the source candidate only; it does not pin or activate a Runtime/App
consumer.

## Contract verification

- Main's current ClipPanelBody reads clip.opacity ?? 1, constrains the
  control to 0..1, and emits the raw slider value. The candidate maps this
  to clip.set@1.args.values.opacity, not params.opacity.
- ClipSetArgs.values is closed and admits only top-level hold and opacity;
  opacity is JSON number with inclusive minimum 0 and maximum 1. clear is
  closed to the existing fields plus "opacity".
- Boolean, null, string, out-of-range, and non-finite opacity values are
  refused. Finite JSON is checked before schema validation; there is no
  numeric coercion. The handler writes/clears the literal clip["opacity"]
  leaf and does not manufacture a selected-pack schema or an opacity alias.
- The schema is closed for keys and value types. The cross-field
  values/clear overlap relation remains an existing handler rule:
  _changes() refuses an intersection before any write. Thus
  values={"opacity": x}, clear=["opacity"] is refused, even though the
  independent closed-shape schema clauses do not encode that relation.
- ClipSetParamsArgs remains a separate operation with separate generic
  parameter semantics. A params.opacity key is not accepted by clip.set;
  the candidate's source tests cover the hostile bypass.
- Parent and occurrence selectors remain the existing scoped identities.
  Both clip.set schema branches retain the same selector and args guard for
  versions 1 and 2; source-bound capture still selects version 2 only for
  the existing verified source-closure case. _target() retains the
  parent/occurrence identity, owner, source, dependency, and binding reads.
  The opacity addition does not alter those guards.
- Set records the exact prior leaf presence, including absent, null, 0, and
  an existing value; clear removes presence. Existing inverse/redo, strict
  A-to-B-to-A refusal, direct-neighbor preservation, occurrence isolation,
  and disjoint-params rebase behavior remain on the generic recorder path.

## Historical source floors

The candidate's test-only without_opacity() helper removes only the new
opacity property, clear token, and description wording from an in-memory
schema copy. It reconstructs the unchanged historical hashes:

- ordinary: 6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
- private carrier: 613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3
- private project-data: 39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d

No frozen fixture, counterpart, public artifact, pin, or source file was
mutated.

## Runtime boundary

The installed Runtime contract remains the pre-opacity floor: its bundled and
public ClipSetArgs definitions admit only hold, asset, and transition, and
its current provider digest is unchanged. Therefore current Runtime
validation will refuse an opacity command until a later coordinated schema
and provider-digest update. That is expected for this SOURCE ONLY proposal,
not a contract mismatch or a reason to mutate the frozen 392/613/6ba sources.

## Evidence

Direct pure probe against the exact Agent tree (in-memory only):

PASS exact Agent schema boundary/type/closedness probe
PASS handler-level set/clear overlap guard
PASS in-memory source floors: 392/613/6ba

The proposal reports its focused Agent conformance as 111 passed, 2 warnings
and its inventory controls as 52 passing checks. I did not rerun the Agent
suite, Runtime full/quick suite, native pair, browser journey, or any
generation/pin/activation flow for this bounded read-only review.

