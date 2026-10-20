# M2 effects: Agent contract candidate (integration held)

Owner: agt-m2-effects-set. Base Agent 027bd16d96010544331c953c0e1014e161786e71.
This is an early source contract, not a release or Runtime/App acceptance claim.

## Actual producer and canonical shapes

App `/home/user/work/app/src/tools/video-editor/components/PropertiesPanel/ClipEffectsTab.tsx`
delegates to ClipEntranceEffectField, ClipExitEffectField and
ClipContinuousEffectField. These set/remove singleton **named slots**
`entrance`, `exit`, `continuous` through `onChange` -> `updateClip` (hooks/
useTimelineCommandsService.ts:604). Type strings are selectors (including
`custom:${resource.id}`), not instance IDs or immutable descriptor references.
The fields edit duration/intensity and merge params. None/Remove means ABSENT.
`runtime/element-adapter.ts` timeline.set_clip_fade additionally merges
`effects.fade_in/fade_out` and sets entrance/exit. The panel is ClipEffectsTab,
not an EffectsPanel file, on the available App tree.

Agent `astrid/core/timeline/schema/timeline-config.schema.json`:
- named slots are objects with type/duration/intensity/params (continuous has
  no duration); no descriptor ref or instance ID is declared there;
- `effects` is a numeric map OR an ordered array of `{fade_in?,fade_out?}`;
  the array records declare NO stable ID, effect type, or params.

Consequently an ordered `{id,type,params}` custom-instance command cannot be
claimed to match this canonical schema or this inspector. Other App graph
fixtures preserve such opaque arrays, but do not establish an inspector
producer or a canonical instance identity contract. No inferred identities,
array-index args, inline schemas, local-disk schema reads, or migration are
introduced by this slice.

## Smallest faithful native subset

Reuse `clip.set` v1, stable select `parent/clip:<id>` or
`occurrence:<id>/clip:<id>`, unchanged values/clear envelope and normal capture.
Add closed values fields:
- entrance/exit: `{type: string, duration?: number, intensity?: number,
  params?: object}`;
- continuous: `{type: string, intensity?: number, params?: object}`;
- effects: `{fade_in?: number, fade_out?: number}` (nonempty).
Add clear fields entrance/exit/continuous/effects. Existing hold/asset/transition
semantics stay intact. `values` and `clear` remain disjoint.

Same-type slot edits merge only supplied duration/intensity leaves and preserve
all unmentioned opaque members/params, including null versus ABSENT. Omitted
params do not mean clear. Replacing a slot type or removing a slot records the
exact old whole slot; same-type edits guard declared slot type and write only
touched leaves. Numeric map edits write only supplied fade leaves, preserving
opaque siblings. Conversion from an array or nonobject slot refuses explicitly;
removing the entire effects field is allowed with its exact original guard.
Old ordered arrays otherwise remain byte-for-byte unchanged.

Params may be echoed unchanged. Adding/changing params in a named slot refuses
explicitly: no stable selected immutable descriptor is stored there. Existing
exact pack **clip** params remain `clip.set-params` with its existing
schema_source/DocumentPin/resolver/retention path; this is not a substitute for
named-slot params. No new endpoint, DTO, manifest, schema-source alias, Runtime
generation, or pin adoption is requested.

## Remaining positive behaviors / coordination required

Named-slot custom parameter add/edit/reset/clear and ordered custom-instance
add/remove/params remain OPEN, with positive requirement tests marked strict
xfail rather than rewritten to expect refusal. App must keep the writer/draft
for these consumers. Needed before further generation: the actual App producer
for ordered instances, its raw stored identity shape, and a reviewed recorded
migration/selection binding for exact descriptor identity on named slots. The
existing resource type string alone cannot select V1 versus V2 or pack owner.
Any future multiple-declaration input refs must be agreed here with Runtime
before generation; this candidate adds none.

Writer retirement still requires actual App accepted reload, retry, inverse,
and zero legacy traffic. No full-suite, browser, socket, Runtime acceptance,
all-effects coverage, or M2 integration claim is made.
