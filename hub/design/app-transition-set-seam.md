# App incoming transition SET: source audit and capture handoff

2026-10-20. Design/source audit only. **A narrow standalone capture is feasible;
the App consumer and writer retirement are not qualified.** Reuse `clip.set@1`,
the existing scalar session and durable outbox after a new official paired
schema includes SET. No product, UI, schema, generated type, pin or configuration
was changed. PLAN remains authoritative; M2 writers remain until actual
capture → acceptance → reload/retry/undo and zero-legacy qualification.

## Exact sources and portable golden

| Source | Exact identity |
| --- | --- |
| App audited worktree | `/home/user/work/wt/app-m2-transition-set-capture-seam`, HEAD `4f79aea853a53852f50456ac295588c19016f1f7`, tree `2658e872d1c99ad9addcd979d8ce78803bfd4312` |
| Agent published SET | `/home/user/work/agent` object store, `refs/remotes/hub/tl/agt-m2-transition-set-c`, commit `686198313f35b4e918ec74af23beb9fcb3af5948`, tree `59c458965e9ea0f24e1339c8c907bf4c711d56af`; `-b` resolves to the same commit |
| Agent golden at that commit | `tests/editing_conformance/fixtures/recipe_m2_app_transition_set.json`, 159283 bytes, Git blob `030c16bae23ab61b1e0dc4d05420513c090bdaf2`, SHA-256 `ce250ab38b5c7a681bddf618ad2fb55d5fba57290a337d474d1b6b5134e8d747` |
| SET command schema bytes | Agent `astrid/core/timeline/schema/edit-command.schema.json` at `6861983`, SHA-256 `4b12260791657ed6bc143992e2acf734c6b833489ca3538d7a8a4f81ec8dd4fc` |
| Frozen pair, unchanged | Agent `027bd16d96010544331c953c0e1014e161786e71`, schema SHA-256 `472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9`; Runtime `4c145dc62192f0e942e3ee3922a11488aefe9b41`, client `0.2.3`, Runtime schema `sha256:a435dde3b552999ea75ff593868ff4d56debdd64bd8f79c134fb470a279a05e6` |

The old `/home/user/work/wt/agt-m2-transition-set` directory cited by
[the Agent design](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-transition-set.md)
is absent. This review reads the immutable published commit with `git show`;
the original `hub/tl/agt-m2-transition-set` ref is **027bd**, without SET. Fetch
the golden from **6861983**, not that original ref or an inferred directory.
It contains `bundle`, complete `commands`, native `records`, and `after_bundle`.
The original App three-products rows feed `app_bundle()`; do not replace them
with synthetic display clips. The golden's command has 137 reads, one whole
transition write, one predecessor selection and one mirror-derived write.

Agent source anchors below mean **6861983**: `_clip_scalar_commands.py:100-197`,
`_scalar_commands.py:99-164`, `_recording.py:15-35`, `_collections.py:107-122`,
`commands.py:73-195`, `commit.py:347-418`, all under `astrid/sdk/timeline/`.
App paths below are under the exact audited App worktree.

## Published input, not a new operation

The export is `astrid.sdk.timeline._clip_scalar_commands.capture_clip_set`:

```python
capture_clip_set(bundle, select, *, values=None, clear=(),
                 schema_source=None, schema_inputs=(), realm_id=None)
```

`select` is a stable `parent/clip:<raw-id>` or
`occurrence:<raw-occurrence-id>/clip:<raw-id>`; never the projected display ID.
The emitted command uses `schema_version: 1`, `op: "clip.set"`, `version: "1"`,
empty intent and the native recorder's complete original claims. Its closed
args are `{values, clear, schema_source?}`. Existing hold SET and
hold/asset/transition clear remain supported. The **transition consumer slice**
needs only the following existing native shapes:

```json
{"values":{"transition":{"type":"crossfade","duration":0.75,"params":{"future":{"literal":[null,false,0,"","ƒ(x)"]}},"future":[null,2.0]}},"clear":[]}
```

For selected Elements, send `values.elementRef` and `values.transition` in the
same command. The published `elementRef` schema requires `id`,
`kind: "transition"`, `revision`, permits optional `packId`, and forbids extra
keys. Its ID must equal `transition.type`; if transition has an authored
`revision`, it must equal the selected revision. `elementRef` alone refuses.
When omitted, native selection uses the existing raw `elementRef` then
`element_ref` (native truthiness/precedence), and leaves both raw fields intact.
Do not reconstruct an existing opaque ref merely to edit duration.

Transition requires a nonempty literal `type` and positive finite seconds
`duration`; optional `revision` is a nonempty string and `params` is a JSON
object. Other transition keys remain literal JSON **except** compiled-only
top-level `id`, `durationFrames`, `align`, `incomingPolicy`, which refuse.
`params.durationFrames` is allowed and may be a declared parameter. Do not alias
`crossfade` to `cross-fade`, convert seconds to a saved frame count, clamp to the
panel's 0.05–10 range, or materialize defaults during capture. At retained parent
rational FPS, native checks `duration * float(fps) >= 0.5` and
`< 2**53 - 0.5` and finite: a positive safely quantized window, not an integer
seconds-times-FPS requirement. It does not rewrite authored seconds.

**Explicit clear:** `{ "values": {}, "clear": ["transition"] }` removes the
field to ABSENT. Null, `""`, `{}`, `params: null`, SET and clear of the same key,
repeated clear keys and unknown args refuse. An own UI `transition: undefined`
is translated to that clear before JSON serialization; a missing patch key
means no intent. The command does **not** remove `elementRef`/`element_ref`.
`clear: ["elementRef"]` is unsupported. Reset params is a whole transition SET,
not a transition clear; absent params and `{}` remain distinct.

## Actual App producer behavior and preservation

| Surface / exact App source | Current behavior and handoff consequence |
| --- | --- |
| `components/PropertiesPanel/ClipTransitionSection.tsx:101-169` | None and Remove already call `submitClipScalarEdit(..., {values:{}, clear:['transition']})` when the host provides capture. Standalone presentation falls back to `onChange({transition: undefined})`. Selector SET still calls `onChange` with a **replacement** `{type, duration: oldDuration ?? 0.5, params: schemaDefaultsOrUndefined}`; it drops the old transition's revision/unknown members but retains the clip's unrelated fields through the shallow update. New capture must distinguish explicit type replacement from editing the existing value, and omit undefined params from JSON. |
| `ClipTransitionSection.tsx:260-276` | Duration calls `onChange({transition:{...clip.transition, duration:value}})`. This preserves all enumerable transition members, params and revision in that callback; separate clip-level `elementRef` is untouched. Future capture must start from the **raw captured** transition, since the displayed clip may be normalized. |
| `ClipTransitionSection.tsx:294-341` | Parameter callback rebuilds only `{type,duration,params:{...oldParams,[literalName]:value}}`: unknown params survive, but transition-level revision/unknown keys are lost. Reset rebuilds `{type,duration,params: materializeTransitionDefaults(...)}`: it deliberately replaces the params object, removing custom/unknown params, and also drops transition-level extras. Future param edits/reset should retain the raw transition envelope (including revision) and replace only the intended params; keep Reset's explicit whole-params replacement meaning. This preservation correction is not implemented here. |
| `components/ParameterControls.tsx`, `components/SchemaForm/SchemaForm.tsx`; `shared/components/ui/number-input.tsx:35-44` | Controls emit literal name/value changes. NumberInput supports `onValueCommitted`, but transition duration currently attaches only `onChange`; every valid callback goes to the old path. Keyboard typing/stepping must enter the same original-basis capture as pointer changes. Use the existing hold draft/commit pattern in `ClipPanelBody.tsx:140-175,389-390` if grouping duration typing into one edit; preserve the first basis and draft on failure. Do not depend on pointerdown alone or assert unimplemented Enter/Escape semantics. |
| `hooks/useKeyboardShortcuts.ts:209-238,298-307` | Editable targets return early. Outside them Cmd/Ctrl-Z and redo call the existing undo/redo; Delete removes selected clips, Escape clears selection. There is no transition-specific reset/remove keybinding. Keep these meanings; keyboard activation of Select/Remove/Reset uses the same callbacks. |
| `components/ElementsLibraryPanel.tsx:46-88` | Requires published entry and at least two selected IDs; passes insertion-order IDs as `from_clip`/`to_clip`, exact `{id,kind,revision,packId?}`, and expected config version to `timeline.apply_transition`. It does not supply duration or params and invalidates the query after the legacy call. A native handoff must bind the requested FROM to the native predecessor of the captured raw TO; never silently retarget to another neighbor or guess ownership by splitting a display ID. |
| `runtime/element-adapter.ts:218-240,345-413` | Apply verifies same track/adjacency/fit, defaults to descriptor `defaults.durationFrames` if integer or 8 frames, and writes the **TO** clip's `elementRef` plus `{type: exact ID,duration: frames/fps,revision,params?}`. Update spreads existing transition/clip and preserves their unknown members; explicit params replace the params object. Remove deletes **both** transition and elementRef. Native panel clear therefore cannot faithfully replace legacy adapter Remove on a selected clip. That adapter operation stays OPEN pending an Agent-owned lossless clear contract; never pretend retaining its ref is equivalent. |
| `runtime/element-adapter.ts:66-112,494-520` | Existing durable route loads config/registry/head, CAS-saves via `saveTimelineAtHead` (numeric `saveTimeline` fallback), then reloads. It is still an old writer, not a native command adapter. `timeline.apply_transition`, `update_transition`, `remove_transition` are local operation names, never wire opnames. |
| `runtime/families/transitionAdapter.ts` / `projectors/transitionProjector.ts` | Descriptor projection placeholder only; it supplies no native mutation capture or acceptance. Reusing it as a writer would add a second path. |
| `lib/timeline-domain.ts:182-186,2314-2402,2467-2471`; `lib/timeline-data.ts:192-193,342-343` | Serialization explicitly carries transition and elementRef, and retains own undefined transition for legacy clear coverage. Repair helpers can clear unresolvable types or materialize defaults. These display/repair results cannot become the raw capture authority. The Agent accepts an unselected unregistered type as opaque JSON, so acceptance/reload qualification must prove it is preserved despite unavailable render metadata. |

The selector's type-only UI record is not enough to switch a clip whose existing
selected ref names another type. Native correctly refuses that mismatch. Resolve
an exact replacement descriptor and send the pair atomically, or retain the draft
and visibly refuse; there is no permitted unpin-by-omission. Existing ref extras
may survive a duration-only SET, but a new `values.elementRef` with extra keys
must refuse rather than strip them to satisfy the closed schema.

## Exact predecessor query and read scope

Golden selection, copied without renaming fields:

```json
{"key":"transition.predecessor","query_version":1,"owner":"parent/clip:f2-transition-clip","members":["parent/clip:f2-app-clip"],"order":["parent/clip:f2-app-clip","parent/clip:f2-transition-clip"],"boundaries":["parent/track:V1"],"policy":"guard-membership"}
```

`_recording.selection` takes all raw clips under the target's owner with the
same literal `track`, sorts by authored `at` (fallback `at_ms / 1000`, default
zero), and keeps collection order for ties. No active/hidden filtering.
`members` is the immediate preceding identity, empty for first; `order` is the
entire same-lane identity vector and boundary is its owning track. No global
cross-occurrence or compiled outgoing search. Gaps, overlaps, first clips and
oversized windows remain authorable under the settled incoming policy. Preserve
legacy Elements adjacency/fit checks at that adapter's boundary while porting
its existing behavior; do not add them to native SET or the single-clip panel.

Native reads target identity, existing transition, owning track ID, parent FPS,
target and predecessor media selectors/selected refs, consumed registry
media/object/digest/content-digest/content-sha fields, `CLIP_FIELDS`, and
`RELATIONS` at raw/app/app.astrid prefixes. Occurrence capture binds its raw
owner, shot identity/source pin and existing `MAP_FIELDS`; source identity is
recorded as `scalar.images`, target/owner bindings use the existing recorder.
It rejects effect-layer incoming transitions. It does not invoke a renderer or
introduce the legacy fit rule. Same-lane membership/order or consumed
source/timing changes refuse; disjoint lanes replay independently. Original
reads, selections, expectations, authorship, bindings and created IDs survive
replay unchanged. Whole transition writes include unchanged writes; inverse
checks accepted intervening history, including writes and membership ABA.

**Source-review caveat for Agent, not a policy change:** query ordering consumes
`at_ms` when `at` is absent, but `_collections.selection_overlap:108-112` only
recognizes existing lane members' root/id/track/**at** writes. An `at_ms`-only ABA
on a third lane member outside the target/predecessor read pair appears able to
escape the historical selection-overlap check once current order returns to the
same vector. Existing tests prove membership ABA via a root insertion and test
at-based ordering, not this case. This is a source inference, not a newly
executed reproduction. Agent should qualify/fix that case before claiming all
authored timing-codec selection ABA coverage; App must not copy the omission.

## Selected pack input and retained PARAM read

Reuse the existing native selected-PARAM context, **not** display schemas:

```text
schema_source = DocumentPin {document_id, version, content_digest}
schema_inputs = [(VerifiedDocument, {selected_snapshot_object_id: VerifiedDocumentObject})]
VerifiedDocument = {pin: schema_source, document: exact_project_document}
VerifiedDocumentObject = {object_id, digest, size, media_type: "application/json", bytes_base64}
realm_id = captured scoped realm
```

Only `schema_source` goes in command args. Detached inputs feed pure capture;
Runtime independently resolves authoritative data during commit. Match admitted
ID/kind/revision/pack ownership, exact pin and selected immutable snapshot;
record existing `params.schema`, `params.snapshot`, `params.element`, retain the
verified document and reuse the provider's existing hydration/resolver (extended
to clip.set in 6861983). Known **changed** params are validated without coercion,
default insertion or schema reconstruction; unknown property names/values stay
literal. Same selected transition with no changed params can use native's
existing no-schema-read path; it is not permission to avoid reads for a changed
selected value or new selection. Exact shipped built-ins match catalog
id/kind/packId/revision; an unavailable selected declaration has no type-only
fallback. Unselected registered types use the native built-in schema;
unregistered unselected types remain opaque, with no renderability claim.

[The retained PARAM read audit](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-params-source-read.md)
identifies the frozen public-read gap. The orchestrator's App INBOX decision
03:31Z approves exposing the existing config_source/document_object read through
the normal generated client, with closure authorization, retention/custody/race
checks, no second object endpoint or invented fields. **Approval is not shipment.**
Consume its official paired release once available; current getDocument, CAS
bytes, Vite admission modules and caller-hashed UI declarations cannot recover
the authorized retained V1. Keep changed selected-pack PARAM refusal until the
actual read is usable. The required retained case remains 4 → 8 under V1 max10;
after live V2 max20, removal and restart, V1 still refuses 16. This review did not
qualify a newer read candidate or change frozen 027/0.2.3.

## Implementable narrow App handoff after official pairing

1. Extend the existing `commands/clipScalarCapture.ts` bounded SET implementation
   to match Agent **6861983**, its closed values/schema rules and exact recorder
   output. Add this one predecessor query to the existing `MoveRecording`
   selection machinery; preserve stable ties, order and boundaries. Use its
   existing compile/mirror/dependency path. No new compiler, generic field
   writer, subprocess endpoint, or local command naming scheme. Compare full
   command/bundle/record to the pinned native golden, including JSON roundtrip
   and opaque own keys such as `""`, `"a.b"`, `"__proto__"`, `"constructor"`,
   `"prototype"` in params/allowed unknown transition fields; these remain
   literal keys, not paths or a ban list. The current golden exercises opaque
   nested values, not all these JS own-key cases; those App cases remain to add.
2. Keep `useClipScalarControl` → `captureClipScalarEdit` →
   `commitSession.clipScalarPort` (`commitSession.ts:365-497`). It already checks
   scope/display head, resolves actual raw parents before opaque app.canonical
   fields, and verifies exact occurrence owner/source/output binding. Capture
   raw bundle/select/localGeneration/localBasis once at the start of the edit;
   keyboard changes use the same path. Construct full transition SET from that
   raw basis for duration/params/reset, preserving the envelope and untouched
   elementRef. Keep intentional selector replacement and Reset params replacement
   explicit. Resolve selected inputs for that original basis before finish;
   async reads must not silently capture a new head.
3. Reuse scalar finish to capture against original bytes, re-execute the original
   command against current raw bytes and register the prepared entry before
   submit/enqueue. Preserve every native claim across ACKs, newer dependent
   edits and restart. Extend generated args only from the official new pair;
   current `timeline-commit-types.ts` only permits hold SET and App metadata is
   still 0.2.3. No local schema/type relaxation against frozen 472622.
4. Fix the **existing** scalar preview boundary narrowly as part of that consumer:
   `clipScalarGesture.ts:21-22` always includes `clear`, even `[]`;
   `lib/timeline-patch.ts:174-182` rejects any non-hold payload when clear exists.
   For transition-only or paired SET, omit the empty local clear member (or an
   equivalently bounded validation adjustment), while wire args retain `clear:[]`.
   Preserve exact supported clear previews. Verify full transition and paired
   elementRef survive local rows/meta/config, recovery and accepted projection;
   the clip.update meta sync at `timeline-patch.ts:1296-1315` does not explicitly
   list elementRef when it is absent from existing meta. Existing domain
   serialization supports elementRef, but that alone is not paired preview proof.
5. Keep prepared-command/preview equality checks and existing enqueue/outbox
   `OutboxBasis` (head pair or after prior intent). Use the existing
   `RuntimeDataProvider.commitTimeline` door and exact persisted request body/key.
   A dependent B stays unsent until A is acknowledged, then uses A's accepted
   base with B's ORIGINAL guards. Retry never reselects a predecessor, refreshes
   guards, changes pack revision or allocates another identity. Accepted undo is
   the existing `timeline.inverse` over accepted publication, never a snapshot
   rewrite or preview rollback presented as accepted undo.

**Atomic refusal:** the standalone adapter accepts one whole transition SET,
optionally its matching elementRef, or explicit transition clear. Reject a
mixed patch such as `{transition: next, speed: 3}` (likewise effects, opacity,
asset assignment, clip params, at/track, ref deletion or unsupported registry
work) before preview, prepared registration, outbox append or network traffic.
Never filter to the supported key and save it separately, translate SET to
clear, or fall through to `onChange`/snapshot save after capture fails. Native
clip.set can combine its own supported hold/clear fields, but that does not
authorize a general App patch writer. Retain the entire failed draft and show
the existing visible error. The current permanent mixed test
`ClipPanel.scalar.test.tsx:340` (`hold:8,speed:3` plus transition clear) remains
unchanged; add transition-specific positives/refusals when implementing.

## Acceptance dependencies and verification limits

- Official new Agent/Runtime schema/client pair containing SET; frozen 027 and
  0.2.3 remain untouched. Pairing, local capture parity, selected retained reads
  and consumer conversion are separate dependencies.
- Mounted selector/duration/params/reset/keyboard captures, first/gap/overlap/
  oversized and parent/occurrence isolation, opaque own keys, exact selected
  identity and literal clear behavior; no lost passing behavior expectations.
- Real command acceptance/reload; lost ACK + newer edit + exact retry + restart;
  conflict/refusal retains the whole draft; guarded inverse/redo; zero legacy
  save/publish traffic for each actual consumer. Existing Elements Remove's
  elementRef deletion requires its own Agent-owned contract before replacement.
- **First-use DocumentPin inverse remains OPEN.** Agent
  `tests/sdk/test_timeline_transition_schema.py::test_first_selected_transition_exact_document_inverse`
  is still strict xfail: authored transition/ref restoration passes, but the
  newly introduced manifest pin remains. Do not claim exact document undo from
  authored-only equality. Guarded pin removal with retained historical redo
  custody is an Agent/Runtime acceptance dependency, not an App cleanup trick.
- Agent at_ms selection-history caveat above and the reproduced App scalar
  outbox failure below need qualification. No product fix was made by this audit.

Bounded existing probes only: six App unit files **117 passed / 1 failed**;
the same failure reproduced in isolation. Agent's two transition files at exact
6861983 **37 passed / 1 existing strict xfailed**. Exact commands, logs and the
failure location are in
[the worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-transition-set-capture-seam/notes/report.md).
No install/build/tsc/browser/full/test-service or live-socket suite ran. These
probes do not prove actual App SET acceptance, runtime read shipment, rendering,
retry/reload/undo, or writer retirement.
