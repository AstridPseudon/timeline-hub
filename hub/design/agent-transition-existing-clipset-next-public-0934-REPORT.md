# Agent bounded source ACK: Runtime incoming transition SET

Date: 2026-10-21 UTC

## Disposition

**BOUNDED Agent SOURCE ACK for the existing `clip.set` carrier and the
unapplied Runtime schema diff, with three literal contract clarifications
called out below.** The source semantics at the requested Agent floor are otherwise
compatible. This is not generation, pinning, activation, publication,
consumer qualification, or proof of Runtime/App behavior.

## Source identities reviewed

- Agent clean ca9 source: commit
  `ca9f5f8eeba96bb9cb8f9d700c2714c2ed9f9a20`, tree
  `87b432d48b0e1a5e0410c630ca76150095075eff`.
- Agent schema:
  `astrid/core/timeline/schema/edit-command.schema.json`, SHA-256
  `a70f0e8898c6acccb34062e73733c93dd4e7bc22c34ef012431e1791907e1f4a`.
- Agent repaired source floors reviewed: `_clip_scalar_commands.py`
  `db72c5dbaed2eac46b9a5132dcbbc5533bcca904fdc725e9a5e821b9d6dbf8d6`,
  `_selected_param_authority.py`
  `2747d3c64a5eebe9ee11c5c8fca5f23afaa13f6c9ef406a98eeaec572924bed8`, and
  `commit.py`
  `d5faef1698d183017eb6a39710ca012e83d26469f88e1621f0214ab164c6ce88`.
- Main witness: commit
  `860d43b331fb4422b16bc0dbd7b08666a0c766a0`, tree
  `ea4eabb8eb469df63fd1d515f84982d85b2f14cc`; `element-adapter.ts`
  transition admission and apply/update sections at the cited source lines.
- Runtime public floor from the proposal: 0.2.14 commit
  `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
  `6abc2f117391de8e7e35c0283f575a002199894d`.
- The private017 Agent line was inspected read-only at
  `b8bbb5cf1d7f64b6a51e762ef394c4278b3e5492`; it has no transition carrier
  change relevant to this ACK. No private017 artifact was changed.

## ACK: reviewed shape and semantics

The proposed Runtime shape is the right existing operation boundary:

```json
{
  "schema_version": 1,
  "op": "clip.set",
  "version": "1",
  "select": "parent/clip:<to-id>",
  "args": {
    "values": {
      "transition": {
        "type": "<selected transition id>",
        "duration": "positive authored seconds",
        "revision": "same selected revision",
        "params": "optional complete literal JSON object",
        "<opaque top-level key>": "literal JSON"
      },
      "elementRef": {
        "id": "same transition id",
        "kind": "transition",
        "revision": "same selected revision",
        "packId": "optional selected pack owner"
      }
    },
    "clear": []
  }
}
```

The Agent schema at `ClipSetArgs` has exactly the proposed additive fields:
closed transition properties, JSON-valued `params` and opaque top-level
transition keys, `elementRef`, `schema_source`, and the additional
`elementRef` clear token. Compiled-only `id`, `durationFrames`, `align`, and
`incomingPolicy` are refused. No new operation, DTO, store, endpoint, or
second schema authority is needed.

The Agent handler at `_clip_scalar_commands.py:91-176,205-246` confirms:

- SET owns the incoming transition on the selected destination/TO clip.
- `duration` is authored seconds and is checked for positive finite numeric
  input; no frame-count field is saved, clamped, or rewritten.
- `transition.type == elementRef.id` and the transition/reference revisions
  must match; `elementRef.kind` must be `transition`.
- Built-in declarations use the Agent catalog directly. Project-pack
  declarations use the existing exact `DocumentPin` path; no inline or
  type-only authority is introduced.
- The handler reads the target and predecessor clip fields/relations and
  media digest, retains parent/occurrence ownership/source bindings and FPS,
  and writes the raw transition envelope plus the matching ref in one
  `clip.set`.

The existing reset remains exactly distinct:

```json
{"values": {}, "clear": ["transition"]}
```

It removes only transition presence and preserves unrelated canonical or
legacy `elementRef`/`element_ref` data. The explicit associated removal is:

```json
{"values": {}, "clear": ["transition", "elementRef"]}
```

At `_transition_clear_pair` and `clip_set`, this validates every present
canonical/legacy reference against stored transition type/kind/revision and
clears the transition and both reference spellings atomically. A lone
`elementRef` clear is refused. Inverse restores the exact prior presence.

## Guards and authority

The `transition.predecessor` selection at `_recording.py:20-28` and its
overlap handling at `_collections.py:108-122` record the immediate same-track
predecessor, the same-lane order/membership, and the owning track boundary.
The SET then enforces Main’s adjacency rule
`abs(predecessor.end - destination.start) < 0.001` and the shorter-adjacent
clip frame-fit tolerance `+0.0001`. It refuses gaps, cross-track neighbors,
and oversized windows; it does not select a successor or invent a second
transition writer.

For a selected project-pack transition, `_selected_param_authority.py:9-49`
and `commit.py:513-590` retain the accepted P1 source/snapshot association
for same-reference generic `clip.set`, require the exact `schema_source`,
and refuse a later P2 authority for the same stable selected identity. The
requested element ID/kind/pack owner/revision must remain the selected
identity. Built-ins do not require a pin. This is the existing authority
chain, not a new receipt or proof mechanism.

## Concrete mismatches to carry to Runtime/App2

1. **The proposal’s literal `crossfade` sample is not the Agent ca9
   canonical built-in identity.** Agent’s descriptor and transition tests use
   `cross-fade`; `crossfade` is an authoring/browser alias in surrounding
   code. The source handler matches catalog descriptor IDs exactly. Main’s
   adapter preserves the supplied operation element ID. Therefore the hub
   must export the selected descriptor’s exact ID and enforce
   `transition.type == elementRef.id`; it must not treat the proposal’s
   `crossfade` sample as an Agent canonical token or silently normalize it at
   the Runtime carrier. If `crossfade` is intentionally retained as the
   cross-product canonical ID, that is a new semantic decision and requires a
   source repair/compatibility test; it is not covered by this ACK.

2. **Main and Agent differ on frame integrality at the authored boundary.**
   Main’s `transitionDurationFrames` requires an integer frame count. Agent
   ca9 stores authored seconds and only checks safe positive/fit frames; its
   existing transition test uses `0.75` seconds at 30 fps (22.5 frames).
   The proposal’s claim that there is no remaining Main/Agent semantic
   inconsistency is therefore too strong. The settled carrier can remain
   authored seconds, but Runtime/App2 must either explicitly accept the
   Agent authored-seconds contract as the canonical boundary (and not claim
   Main’s integer-frame admission), or obtain a future Agent decision/source
   change to require integral `duration * fps`. This worker made no such
   change.

3. **Revision is effectively required for SET despite the prose saying it is
   optional.** `ElementRef.revision` is required by the existing schema, and
   the Agent SET requires it to equal `transition.revision`; consequently a
   valid paired SET always carries a non-empty transition revision. Keep
   `revision` optional only for an unpaired raw transition shape that Agent
   will not accept, or clarify the schema prose to say required for SET.

## Exact existing capture entrypoint and future composition

The exact Agent capture entrypoint is:

`astrid/sdk/timeline/_clip_scalar_commands.py:capture_clip_set`

It delegates to the existing `_scalar_commands._capture` and produces one
`clip.set` command. There is no separate native Agent transition capture API
to preserve or replace. A future App/CLI composition should read the target
clip’s current raw transition and selected ref, deep-copy the complete
transition envelope (including opaque keys and nested params), apply the
requested changes, then call `capture_clip_set` once with the paired
`values.transition`/`values.elementRef` and the exact `schema_source` only
when the selected descriptor is a project-pack element. RESET continues to
call the same entrypoint with `clear=["transition"]`; paired removal uses
`clear=["transition", "elementRef"]`.

No `clip.set-transition`, `clip.set-params`, transport carrier, or new DTO is
needed for this composition. The command is a source ACK, not proof of a
Runtime commit or consumer qualification.

## Evidence and scope

No product files, Runtime/App artifacts, branches, refs, pins, or source
were modified. No generation, publication, activation, native/HTTP/body,
renderer, browser, live socket, install, or full suite was run.

Prior bounded ca9 review evidence (not rerun in this read-only review) records
the following targeted results:

- `tests/editing_conformance/test_recipe_clip_scalar_fields.py -k 'private_transition or transition_only_clear or explicit_transition or transition_set_enforces'` plus `tests/sdk/test_timeline_transition_schema.py`: 7 passed, 136 deselected.
- Selected-authority focused lane in `tests/sdk/test_timeline_selected_param_authority.py`: 7 passed, 20 deselected.
- Transition/schema lane: 29 passed, 87 deselected.

Recommended next step: Runtime/App2 should ACK the corrected canonical-ID
wording and explicitly record the authored-seconds versus integer-frame
boundary before any 0.2.18 artifact generation or pinning. 
