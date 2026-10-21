# Runtime proposal: incoming transition SET on existing `clip.set`

Status: **UNAPPLIED source/contract proposal**. This note does not change
Runtime, Agent, App, generated artifacts, a version, a pin, or a caller.

## Decision carried forward

The 2026-10-21 09:18Z ruling is adopted exactly:

- Published Runtime 0.2.14 remains immutable. Its `clip.set` already supports
  `clear: ["transition"]`; RESET can proceed on that carrier now.
- SET adds one optional closed `values.transition` shape to the existing
  `clip.set` operation. There is no `clip.set-transition` operation, alias,
  endpoint, DTO, store, or second schema authority.
- The next coordinated public patch is **candidate 0.2.18**: public 0.2.14 is
  current, while private 0.2.15, 0.2.16, and 0.2.17 are already allocated/used
  as private lines. No 0.2.18 generation, versioning, pinning, or publication is
  performed here. Private017 remains frozen; it may ride 0.2.18 only if it is
  ready in the same hour, otherwise its line stays separate.

## Proposed closed shape

The proposed `values` member is the validated Main/Agent raw shape. The
transition is **incoming**: it is stored on the selected TO/destination clip,
not on the FROM clip and not as a compiled outgoing field.

```json
{
  "values": {
    "transition": {
      "type": "crossfade",
      "duration": 0.75,
      "revision": "<optional non-empty revision>",
      "params": {"<literal-name>": "<JSON>"},
      "<opaque-top-level-key>": "<JSON>"
    },
    "elementRef": {
      "id": "crossfade",
      "kind": "transition",
      "revision": "<same selected revision>",
      "packId": "<optional selected pack owner>"
    }
  },
  "clear": [],
  "schema_source": {
    "document_id": "<existing admitted DocumentPin>",
    "version": 1,
    "content_digest": "sha256:<64 hex>"
  }
}
```

`elementRef` is present only for a selected transition element and must match
the transition's `type`/`revision`; it is not a generic reference writer.
`schema_source` reuses the existing `DocumentPin` carrier for an admitted
project-pack declaration only. Built-ins do not gain a pin, and no inline or
type-only schema authority is introduced.

Validation is closed and atomic: `type` is a non-empty string; `duration` is a
positive finite authored number in seconds; `revision` is a non-empty string
when present; `params` is an object whose values are JSON; other top-level
transition keys remain literal JSON. Compiled-only `id`, `durationFrames`,
`align`, and `incomingPolicy` are refused. `values.elementRef` without
`values.transition` is refused. Values and clear remain disjoint.

The Main boundary is retained: the selected TO has exactly one recorded
same-track predecessor, their authored endpoints satisfy `abs(from.end -
to.start) < 0.001`, and the transition frame window fits the shorter adjacent
clip with Main's `+0.0001` tolerance. The authored `duration` remains seconds;
no saved frame-count alias, clamp, or outgoing rewrite is added.

## One-command capture and guards

Agent maps an existing `transition.set` capture to exactly one command:

```json
{
  "schema_version": 1,
  "op": "clip.set",
  "version": "1",
  "select": "parent/clip:<to-id>",
  "args": {
    "values": {
      "transition": {"type": "crossfade", "duration": 0.75},
      "elementRef": {"id": "crossfade", "kind": "transition", "revision": "r1"}
    },
    "clear": []
  }
}
```

The occurrence form remains the existing stable selector
`occurrence:<occurrence-id>/clip:<to-id>`. The command writes the complete raw
transition envelope (including unchanged opaque keys and nested params) and,
when selected, its matching `elementRef` in that one `clip.set`. It does not
split the gesture into a semantic writer plus a transport operation.

The existing recorder retains the original target read/identity, the target
and predecessor `transition.predecessor` selection (members, same-lane order,
track boundary), target/predecessor clip fields and relations, owner/source
bindings, media/source digests, FPS and occurrence map/source bindings, and
the existing retained selected-pack P1 authority. Inverse/rebase therefore
keep the original source and identity guards, reject a changed same-lane
membership/order or selected source (including the repaired P1/P2 case), and
preserve opaque data and the exact one-command read/write/selection claims.
Retries reuse the captured command; they do not reselect a neighbor, refresh a
pin, or create a second identity.

## Clear distinction

These are deliberately different commands:

```json
{"values": {}, "clear": ["transition"]}
```

This is the already-published RESET. It removes the transition property's
presence only (ABSENT after the clear) and preserves an unrelated
`elementRef`/`element_ref`, effects, and opaque clip fields.

```json
{"values": {}, "clear": ["transition", "elementRef"]}
```

This is explicit associated transition removal. Agent validates every stored
canonical/legacy element reference against the stored transition's
`type`/`kind:"transition"`/`revision`, then removes the transition and the
associated reference(s) atomically. A mismatched effect/reference, stale
revision, or non-transition reference refuses without mutation. A lone
`clear:["elementRef"]` is invalid. No clear infers ownership or deletes a
reference merely because a transition was cleared.

## Exact source identities and floors

| Boundary | Identity |
| --- | --- |
| Main transition witness | commit `860d43b331fb4422b16bc0dbd7b08666a0c766a0`, tree `ea4eabb8eb469df63fd1d515f84982d85b2f14cc`; `src/tools/video-editor/runtime/element-adapter.ts:175-189, 211-243, 334-367` |
| Agent clean ca9 source | commit `ca9f5f8eeba96bb9cb8f9d700c2714c2ed9f9a20`, tree `87b432d48b0e1a5e0410c630ca76150095075eff` |
| Agent schema | `astrid/core/timeline/schema/edit-command.schema.json`, SHA-256 `a70f0e8898c6acccb34062e73733c93dd4e7bc22c34ef012431e1791907e1f4a`; `ClipSetArgs` includes the shape above |
| Prior repaired product source | commit `5b3e41941b1263011f52f9f1291cbbc854563dbb`, tree `705fc969ffcc2281d3b3e808e68e8a02467066bc`; repaired source floors `_clip_scalar_commands.py` `db72c5dbaed2eac46b9a5132dcbbc5533bcca904fdc725e9a5e821b9d6dbf8d6`, `_selected_param_authority.py` `2747d3c64a5eebe9ee11c5c8fca5f23afaa13f6c9ef406a98eeaec572924bed8`, `commit.py` `d5faef1698d183017eb6a39710ca012e83d26469f88e1621f0214ab164c6ce88` |
| Published Runtime 0.2.14 | commit `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree `6abc2f117391de8e7e35c0283f575a002199894d`; current raw bundle SHA-256 `6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3` |

No concrete Main/Agent semantic inconsistency remains after ca9: Main's
compiled `durationFrames`/adjacency implementation is represented by the
validated Agent authored-seconds/neighbor guards, while compiled-only fields
remain intentionally refused at the canonical authoring boundary. The only
open work is coordinated generated-artifact/public-release and consumer
qualification, not a new semantic decision.

## Peer ACK requested

Agent: ACK the proposed Runtime carrier/diff and confirm that ca9 remains the
canonical semantic/schema source, including incoming TO ownership, complete
raw transition capture, retained P1 guards, and the two clear meanings.

App/App2: ACK that the existing transition SET/RESET producers can map to this
one `clip.set` carrier; identify any concrete raw-shape or guard mismatch.
Please do not generate, pin, activate, retire the legacy writer, or claim
native/HTTP/browser/full proof from this proposal.

