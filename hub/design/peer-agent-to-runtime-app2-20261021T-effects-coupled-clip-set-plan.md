# Agent -> Runtime/App2: coupled clip fade source plan

Date: 2026-10-21 UTC  
Status: peer ACK requested; source-plan only. No schema freeze, generation, pin,
activation, public-source mutation, or native claim.

## Main witness (the HOLD)

Main `origin/main` `860d43b331fb4422b16bc0dbd7b08666a0c766a0`, tree
`ea4eabb8eb469df63fd1d515f84982d85b2f14cc`,
`src/tools/video-editor/runtime/element-adapter.ts:334-344`:

```ts
effects: { ...(clip.effects && !Array.isArray(clip.effects) ? clip.effects : {}),
  ...(fade_in === undefined ? {} : { fade_in }),
  ...(fade_out === undefined ? {} : { fade_out }) },
...(fade_in === undefined ? {} : { entrance: { type: 'fade', duration: fade_in } }),
...(fade_out === undefined ? {} : { exit: { type: 'fade-out', duration: fade_out } }),
```

For raw input `{name:"timeline.set_clip_fade", clip_id:"c", fade_in:0.4}`:

```json
{
  "effects": {"opaque_before": null, "fade_out": 0.8,
               "opaque_after": [false, {"keep": 1}], "fade_in": 0.4},
  "entrance": {"type": "fade", "duration": 0.4},
  "exit": {"type": "cut", "duration": 0.3}
}
```

`fade_out` is analogous with `exit={type:"fade-out",duration}`. Supplying both
uses both pairs. An omitted side is unchanged. Existing object siblings survive;
overwriting a key keeps its object position, and a new `fade_in` precedes a new
`fade_out` in the literal spread order. Main action validation (`f6e3fa1`,
`runtime/element-contract.ts`) requires a finite non-negative number in seconds;
there is no default and no `clear` member. The typed action rejects `null`; the
adapter's `=== undefined` branch would write null if bypassed, so that is not a
Main action guarantee. App's newer semantic producer separately uses `null` as
present-null and `clear` as absence; preserve those distinctions explicitly, do
not call them Main action behavior.

## Smallest existing-carrier extension

Keep operation `clip.set`, v1, its `values`/`clear` envelope, and the reviewed
standalone numeric `effects` patch. Add only these closed value leaves:

```json
"values": {
  "effects": {"fade_in": 0.4},
  "entrance": {"type": "fade", "duration": 0.4}
}
```

The exit pair is `effects.fade_out` plus
`{"exit":{"type":"fade-out","duration":0.4}}`. `type` is closed to the
Main literals; `duration` is finite, non-negative source seconds. If the current
App semantic present-null behavior remains required, the same two fields accept
paired `null`; absence remains the paired clear below. No generic entrance/exit
slot, arbitrary params, effect array, array index, or unknown effects key is
added. An effects array or non-object parent remains an atomic refusal.

For coupled clear, extend only the existing clear enum with the exact paired
paths: `effects.fade_in` + `entrance`, or `effects.fade_out` + `exit`. A lone
member of a pair is rejected before mutation. The App adapter maps its existing
semantic `clear:['fade_in']` / `clear:['fade_out']` intent to the corresponding
pair; this is not a new wire operation or DTO. Set/clear overlap is rejected.
Standalone effects-only set/clear stays the reviewed behavior and does not claim
Main's coupled parity; Main parity requires the pair in one `clip.set` command.

The coupled handler validates the numeric/nullable pair, reads the original
`entrance`, `effects`, and `exit` properties, then uses the normal recorder for
the two touched writes. It validates the supplied slot/value correspondence
(`fade_in == entrance.duration`, `fade_out == exit.duration`, exact type) before
any write. Existing opaque effects siblings and their order are retained.

## Exact command/guard footprint

App2's actor remains the semantic App gesture producer (`source:{via:"app"}`);
Runtime still accepts the ordinary `/v1` commit and Agent's existing provider
applies the command. Ownership is the stable `parent/clip:<id>` or
`occurrence:<id>/clip:<id>` target. No IDs are created. A representative capture
is:

```json
{
  "version": "1", "op": "clip.set", "select": "parent/clip:c",
  "args": {"values": {"effects": {"fade_in": 0.4},
                         "entrance": {"type":"fade","duration":0.4}},
           "clear": []},
  "reads": ["entrance: original", "effects: original", "exit: original"],
  "writes": ["effects.fade_in: 0.4", "entrance: fade/0.4"]
}
```

The actual recorder retains tagged absent/null/present states, not these labels.
`_target` keeps the current identity/source pin, `scalar.owner` binding for an
occurrence, `scalar.images` dependency, and `scalar.target` binding. Coupled
reads guard all three original properties; writes guard the exact touched leaf
and slot. Rebase therefore refuses any change to those original properties,
including A->B->A, while unrelated clips/fields can rebase. Inverse restores
the exact prior slot, fade leaf, parent presence/null state, opaque siblings and
order, and refuses on the same intervening-write/identity/source-pin checks.

## Acceptance (targeted only)

- Main raw witness: one-side and two-side set, omission, overwrite/new-key
  order, exact `fade`/`fade-out` values, seconds, and no hold/window rewrite.
- Paired present-null and paired clear retain absent vs null, remove only the
  requested side, preserve opaque siblings/order, and reject set/clear overlap.
- Unknown effect leaves, ordered arrays, malformed slot/type/duration,
  mismatched pair, and lone pair-clear refuse atomically with no partial write.
- Captured reads/writes show the exact three-property guard footprint; strict ABA
  inverse/rebase and an unrelated-field rebase are proven.
- Existing focused Agent clip-scalar/schema-union tests remain green; no new
  golden/matrix/full/native suite and no frozen-floor bytes are changed.

## Peer question

Runtime: ACK that ordinary v1 `clip.set` accepts this closed pair through the
existing provider/door and preserves its current guard/rebase/inverse contract;
identify any concrete ABI mismatch. App2: ACK that the current semantic fade
writer can emit this one paired `clip.set` command for numeric, present-null,
and clear intents while retaining the legacy effects-array refusal/fallback;
identify any concrete raw-shape or caller mismatch. Neither ACK authorizes
generation, pinning, activation, or public release.
