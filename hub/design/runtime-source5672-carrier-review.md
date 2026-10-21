# Runtime bounded source/carrier ACK — Agent 5672 union

Date: 2026-10-21 UTC

## Verdict

**SOURCE ACK, bounded to the composed Agent source contract.**

No new Runtime semantic incompatibility was found in the complete Agent union
when it is paired with the existing generic commit carrier and the approved
raw-reference counterpart pieces. This is not a generation, version, pin,
freeze, public-artifact, native-provider, App, or activation approval.

The exact Agent source reviewed is commit
`5672d2b7deee2bfe2ab375fd6db5fc35a192591d`, tree
`6dd13b552c4f07fff5586b1fa772bdbdf64accba`.

- Raw schema SHA-256: `daec2964bb589d2087409446f99b84cfe9d6fb62b0b3af25e37363a78b170514`.
- Canonical formatted schema SHA-256:
  `9c05ec496e957548fe4656ca655a67a7b936ff4f220bdedae474a680e6d32eb9`.
- Inventory: 62 definitions and 36 closed operation clauses.
- Scope: ordered project-data remove, mute, opacity, free `clip.move-set`,
  parent `afterClip` birth, raw parent reference, and parent track order over
  the reviewed `84fc` floor. Raw OLD swap and other named future units are not
  included.

## Carrier review

The Runtime generic envelope is sufficient for the new source claims once the
Agent-owned operation schema is supplied by the future counterpart:

- `EditCommand` keeps the operation version, stable selection, opaque `args`,
  reads, writes, bindings, created IDs, and intent without a Runtime-owned
  operation-specific DTO. `AgentSelection` already carries complete `members`
  and `order` claims.
- `Recorder`/`CommandRecord` already retain the complete command record,
  selections, virtual writes, dependencies, and derived writes as canonical
  JSON. `parent::track_order` is therefore a valid guard address; Runtime does
  not need, and must not invent, a persisted `track_order` leaf or second
  authored store.
- Accepted history already stores the recorder and canonical document behind
  the normal idempotency receipt/publication chain. The existing canonical
  digest and revision-identity checks preserve exact JSON bytes; unknown
  authored siblings remain in the parent payload rather than being rebuilt
  from the relational projection.
- The closure gate requires canonical parent `clips` and `config.clips` to be
  lists and rejects disagreement, while preserving the rest of the parent,
  clip, track, project-data, mute, opacity, and after-anchor authored fields.
  The future Agent provider must continue emitting those synchronized lists.
- Existing project/timeline membership, immutable revision/content-digest
  checks, occurrence ownership, publication ancestry, history verification,
  and accepted-retry ledger checks remain the relevant Runtime custody and
  owner guarantees. Nothing in this union requires a new owner namespace or
  timing store.

The earlier rational-FPS carrier concern is resolved by Runtime commit
`60a919a22f42f0b5b0a246ce84cb43e9f46c2106` (tree
`4fc4c0fdbe1a2d78061a4b83d480d758a6a69d13`): the visual seam accepts the
approved mapping and two-item list forms for local frame calculation while
retaining the authored spelling. The source union's timing dependency is
therefore compatible at this bounded source boundary.

## Raw reference and projection dependency

`timeline.reference@1` is compatible only with the approved narrow Runtime
counterpart, not with a generic media selection or caller metadata:

- `f53bf588bf70b090ce8e0bed5ccb7d91157771b6`, tree
  `d82f37052847949e77c12e1704c3f27c6dd56a46`, provides the private,
  request-scoped `raw_media_info(MediaManifestEntry)` read. It verifies the
  exact two-field digest pin against the managed project CAS association,
  captures the verified descriptor identity under the request, and rechecks the
  capture at acceptance. No duration, generation, catalog, or latest-head
  authority may be invented by the carrier.
- `449d13d291cc3b62ebbdd780d38d8c58732e4e1b`, tree
  `47d5f06df25618b45a95293c5217e6454f6ae69c`, derives the existing unplaced
  reference read model after closure and raw custody validation. It preserves
  unrelated rows, globally refuses occupied identities unless the previous
  accepted carrier proves ownership, removes only exact owned rows, and writes
  the legacy snapshot atomically with acceptance/history.

These are explicit future-counterpart dependencies. The current Runtime
integration head `b92d3e7a05eec65c142294ef4873edd059e9b31d` does not contain
those two source pieces, and its checked-in Agent schema resource remains the
55-definition/29-clause carrier. It must not be described as already accepting
the raw-reference operation. Frozen C3d and ordinary014 likewise do not gain
raw-reference support by this ACK. A complete counterpart must compose the
approved helper and projection onto the current Runtime source, then perform
normal schema/artifact work in its own later task.

Same-ID ordinary asset/reference collisions remain visible refusals at the
Agent operation/projection boundary. Runtime must not infer namespace
authority from a media digest or turn the refusal into an overwrite.

## Exact current-boundary discriminator

One read-only discriminator compared the frozen union schema with the current
Runtime bundled Agent resource:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python - <<'PY'
  # load Agent tree 6dd13... and runtime_protocol/schemas/timeline-commit-bundle.json
  # compare EditCommand operation conditionals and carrier definitions
PY
```

Result:

```text
Agent:   62 definitions / 36 clauses
Runtime: 55 definitions / 29 clauses
Runtime-missing union operations:
clip.move-set, occurrence.move, occurrence.resize, project-data.write,
timeline.migrate-groups, timeline.reference, track.reorder
```

This is the expected not-yet-generated counterpart boundary, not a defect in
the source union and not permission to mutate the current public resource.

## Reused evidence and limits

I reused the prior bounded schema, movement, media, reference, and carrier
evidence rather than repeating matrices:

- the final Agent bounded report and contract review establish exact source
  containment and the 239 conformance cases plus schema reconstruction lanes;
- the Runtime movement review establishes closure/recorder compatibility and
  the rational-FPS issue now fixed by `60a919a`;
- the Runtime raw-capture review establishes the `f53` custody/recheck seam;
- the Runtime unplaced-projection review establishes the `449` ownership,
  occupancy, rollback, and history projection seam;
- the Runtime track-order review establishes virtual-order carrier semantics;
- the Runtime project-data review establishes ordered remove/opaque-value
  inverse semantics.

No Runtime source, DTO, store, generated artifact, schema, App, or Agent file
was changed. No full, browser, socket, generation, freeze, pin, activation, or
native qualification run was performed or inferred.

## Counterpart dependencies for Agent/App2

1. Agent supplies the exact frozen 62/36 schema and provider handler/recorder
   semantics; Runtime only carries and durably verifies them.
2. Runtime's complete counterpart composes `f53` raw capture and `449`
   projection onto current Runtime, preserving current CAS, closure, history,
   idempotency, and owner checks.
3. App2 keeps raw-reference and track-order producers dormant until that
   counterpart is generated/pinned and a normal paired qualification proves
   capture, accepted retry, reload/history, inverse, and occupied-ID refusal.
4. No caller may substitute `MediaSelection`, latest catalog state, caller
   duration/metadata, or same-ID namespace authority.

