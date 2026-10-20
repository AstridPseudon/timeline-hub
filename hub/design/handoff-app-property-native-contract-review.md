# App native property contract review

**KEEP — read-only review complete. Opacity is ready for the next bounded capture implementation after owner qualification; no native App wire/UI or writer deletion is qualified by this report.** No repository files, pins, generated clients, Runtime source, tests or expectations were changed. Current root/pin/full gates continue independently.

Manager review requested before exporting this report to `design/handoff-app-property-native-contract-review.md`. This worker has left the proposed content here rather than exporting before that review. The next single worker brief is `notes/next-opacity-worker.md`.

## Fixed sources and decisions

| Source | Exact commit / tree |
| --- | --- |
| Actual App task base | `cc4dff86b845432acc38dd9407ccb079a6a5a677` / `0bf2dba9590097e703bf5775f6a7fa4363184449` |
| Reviewed Agent property union, `hub/tl/agt-m2-property-review-compose-b` | `062cf1afc324b885d05ab61e49a2e5f15cbe82d9` / `6c6015cce3876e7abbceddd021bb4a3c7c9b481d` |
| Newer reviewed transition windows, `hub/tl/agt-m2-transition-set-c` | `48b17eb4550abc23826bb7687a01378753ec84cc` / `3d3dbbfde2120e1e52227bbce793f336e0152aea` |
| Existing Runtime 0.2.8 read release, inspected only for published schema boundary | `1ad39f5c4bf834736bb2ee04b031eebbcdb11ce0` |

Read PLAN first; the 02:54 ordinary-writer queue and 03:31 retained-read owner decisions in `managers/app/INBOX.md:602,660`; flat `m2-opacity-contract.md`, `m2-effects-contract.md`, `m2-transition-set.md`, `app-transition-set-seam.md`, `app-scalar-ingresses.md`, `app-retained-param-read-review.md`, `handoff-app-retained-document028-review.md`, and the ratified addendum in `viewing-incoming-policy.md`. No frozen R4 implementation or unreviewed Agent property candidate was used.

The transition-c branch is **not** the union: its schema does not include opacity/position/effects. Its `_transition_set` AST is identical to property-b, and `recipe_m2_app_transition_set.json` is byte-identical. Its new ten-window fixture is useful evidence to carry into the next owner-composed union, not a reason to substitute its narrower schema for property-b.

## App-ready versus blocked

“Capture-ready” below means the current input has a faithful mapping to reviewed native semantics, subject to a new official union and owned Agent pin. It does not mean a TS implementation, accepted write, reload/retry/undo or browser journey exists at cc4.

| Consumer | Exact current ingress → native mapping | Verdict / remaining blocker |
| --- | --- | --- |
| Single/bulk opacity | `ClipPanelBody.tsx:400` / `BulkClipPanelBody.tsx:717` → shared Slider → `{opacity: number}`; native `clip.set` values `{opacity: v}`, clear `[]` | **Capture-ready first slice.** Shared Slider really scalarizes `[v]`; no percent conversion. Capture must read original raw presence, never inspector fallback `1`. No live migration yet. |
| Programmatic opacity | `useTimelineCommandsService.ts:604` `updateClip({clipId, patch:{opacity:v}})` → currently merges resolved config and `applyValidatedMutation(type:'config')` | **Capture-ready for finite 0..1 numbers.** Future own `opacity:undefined` maps to clear, not JSON null; do not broaden other updateClip keys. |
| Flat position and reset | `ClipPanelBody.tsx:380`, bulk `:274`, `useClipPositioning.ts:16,45` → `{x,y,width,height}` / own undefined geometry keys | **Capture-ready subset.** Native flat pixel/fraction leaves and explicit clear match. Reset clears exactly eight position/crop fields; opacity survives. No rotation/scale/fit/flip/position-object command exists here. |
| Named effect type/duration/intensity and whole-slot removal | `ClipEffectsTab` delegates to `ClipEntranceEffectField`, `ClipExitEffectField`, `ClipContinuousEffectField`; native values named slot patches, clear slot name | **Partial only.** Same-type edits preserve untouched members. Type switch replaces whole slot. Current controls often include params/defaults, so the entire inspector cannot be admitted as this subset. |
| Named-slot params/default/reset, creator auto-application | Same fields and `ClipEffectsTab.tsx:195` produce `custom:<resourceId>` and `params` | **BLOCKED.** No durable selected immutable descriptor per named slot. Only exact unchanged params echo is allowed. Positive strict xfails remain requirements; do not delete/refuse away existing behavior. |
| Numeric fades | `element-adapter.ts:331` `timeline.set_clip_fade` → `effects.fade_in/fade_out` plus entrance/exit fade slot updates | **Partial capture mapping.** Seconds remain seconds. Native merges supplied fade leaves and retains unknown siblings. Existing adapter silently converts an effects array to a map; native correctly refuses that conversion. Preserve old arrays and their ordering/duplicates. |
| Ordered custom instances | No inspector producer/declared stable identity established; canonical array is fade entries without IDs | **BLOCKED.** No invented `{id,type,params}` list, index selector, alias or migration. Ordered custom-instance positive xfail remains. |
| Unselected incoming transition type/duration | `ClipTransitionSection.tsx:133,243` → complete `transition:{type,duration,params?,...opaque}` on target TO clip | **Partial capture mapping.** Duration callback preserves whole object. Type selector omits any paired elementRef; existing nonmatching selected ref therefore refuses. Do not silently clear/replace selected identity to force success. |
| Transition parameter edit/reset and bulk duration | Same component `:274,301` and `BulkClipPanelBody.tsx:633-651` reconstruct `{type,duration,params}` | **BLOCKED lossless ingress.** Source probe confirms revision and opaque outer members disappear, including on bulk duration; reset also drops unknown nested params. Native SET replaces the entire transition, so passing these patches through unchanged encodes that loss. Needs a bounded App preservation fix before migration. |
| Elements library transition apply/update/remove | Library calls `timeline.apply_transition`; adapter `:345,368,408` uses exact transition ref, converts frames/fps, writes TO clip | **Mapping known, migration held.** Existing adjacent-pair/fit checks are stricter than ratified incoming policy. Native allows first/gap/overlap/oversized windows. Remove currently drops transition and elementRef; native transition clear drops only transition. These are explicit consumer mismatches, not permission to change native policy. |
| Selected pack transition SET | Exact ref + `schema_source` + retained document/object inputs | **BLOCKED for live App.** Existing App client is 0.2.1, admitted UI descriptors do not contain DocumentPin. 0.2.8 supplies read shapes but not future SET fields. Owned union/pin, exact capture adapter, retained native qualification and first-use exact DocumentPin inverse remain. |

Actual inspector path is `PropertiesPanel.tsx:542` → `useClipEditing.ts:235` `handleSelectedClipChange` → `applyRowsEdit`, not solely `updateClip`. Bulk uses `handleUpdateClips` / `handleUpdateClipsDeep`. Programmatic updateClip is a separate ingress; both must migrate before claiming all opacity producers. Elements uses `AstridElementOperationAdapter` → `createElementTimelineRoutes` → `saveTimelineAtHead`/`saveTimeline` (`element-adapter.ts:66-106`), another current snapshot producer. All current writers/drafts remain intact here.

Current named-slot field components have selector/remove/reset/parameter callbacks, with duration/intensity carried or defaulted in their objects; they do not expose dedicated NumberInput/Slider duration/intensity controls. Bulk named slots use the same per-clip default-carrying selection pattern (`BulkClipPanelBody.tsx:369,427,485`). This narrows the flat effects document's UI description: native duration/intensity support is not proof that such standalone inspector controls exist on cc4.

## Exact native args, units, presence and owner

At property-b, existing export `astrid/sdk/timeline/_clip_scalar_commands.py:215` is:

```python
capture_clip_set(bundle, select, *, values=None, clear=(),
                 schema_source=None, schema_inputs=(), realm_id=None)
```

It calls the existing `_capture` → native `execute`, returning the fully recorded command. Envelope is `schema_version:1, op:'clip.set', version:'1', select:<raw ref>, args:{values,clear,schema_source?}`. Both values and clear are required on wire; capture fills their empty containers. At least one write/clear, no duplicate clear, no set/clear overlap. Exact supplied captures and their original claims must survive outbox/retry/rebase; do not recapture at ACK/restart.

| Field(s) | SET value | Clear / meaning |
| --- | --- | --- |
| opacity | Finite JSON number 0..1 inclusive | `clear:['opacity']` removes leaf. Null, boolean, string, array, nonfinite or outside range refused; no clamp/default/percent parse. |
| x/y/width/height | Finite raw canvas pixels | Clear individual leaves. Native permits zero/negative dimensions; do not add UI bounds to raw semantics. |
| cropTop/Bottom/Left/Right | Finite raw edge fractions | Clear individual leaves. No percent conversion, clamp or normalization. Current reset supplies these keys, even though the position tab does not expose individual crop inputs. |
| entrance/exit | `{type:nonempty string,duration?:number,intensity?:number,params?:JSON object}` | Whole-slot clear; no nested clear syntax. Durations are seconds, intensity raw scalar. Candidate schema imposes no positivity/range bound on these numbers. |
| continuous | `{type:nonempty string,intensity?:number,params?:JSON object}` | Whole-slot clear. No duration field. |
| effects | Nonempty object containing only numeric fade_in/fade_out | Whole-field clear supported, not individual fade-leaf clear. No array SET. |
| transition | `{type:nonempty string,duration:positive seconds,revision?:string,params?:JSON object,...opaqueJSON}` | `clear:['transition']` removes only transition. Native refuses compiled-only top-level id/durationFrames/align/incomingPolicy. `params.durationFrames` is ordinary schema-controlled nested data, not that forbidden top-level field. |
| elementRef | `{id,kind:'transition',revision,packId?}` closed exact ref | Only paired with matching transition SET; no standalone reference writer/clear. All four identity fields matter for selected built-ins. |

There is no argument named `selectedDocumentPin`; the selected declaration's exact DocumentPin is carried as existing **`args.schema_source`**. Hold and asset-clear remain existing behaviors; asset assignment is not admitted by these property changes.

Stable selectors are only `parent/clip:<raw-id>` and `occurrence:<occurrence-id>/clip:<raw-id>`. No shot selector, displayed/prefixed clip ID, shared-shot row or whole-root selector. Native `_target` rejects `/` in components and `::`. Parent clips use the nonempty direct `bundle.parent.clips` collection, otherwise the existing `parent.config.clips` fallback (`_command_state.py:157-184`). Occurrence clips use `bundle.shots[bundle.placements[occurrence].shot_id].internal_timeline.clips`. Parent tracks/config/fps and scoped registry remain in their existing codec locations; preserve mirror/provenance handling rather than flattening them.

App `authoringBundleFromDocument` clones exact parent/shot/internal payloads and maps shared occurrences to their independent authoring owners (`commands/authoringBundle.ts:103-228`). `shotCompositionProjection.ts:334-347` supplies `app.canonical.clipRef`/rawClipId/ownerRef; duplicates or missing/bad raw IDs are unaddressable. Current commitSession captures moves against that mapping and verifies displayed head (`:199-212`). A future property capture must use the same raw basis/head fencing. Do not split a display string at `:`: raw IDs can themselves contain colons.

App `config-utils.ts:182-269` normally spreads authored clip fields unchanged while attaching assetEntry. Inspector defaults (`opacity ?? 1`, defaultBox) are display values. In contrast, child `shotCompositionProjection.ts:350-421` filters geometry through finite-number checks, offsets timing, supplies hold and gain defaults, and changes display IDs. Thus even current resolved child fields cannot recover absent/null/dynamic raw values. Neither resolvedConfig, ClipMeta, `sanitizeTimelineClipSnapshot`, nor a strict disk serializer is an admissible native before-state.

Historical strict Agent `timeline-config.schema.json` is also distinct from EditCommand: its TimelineClip is closed, requires id/at/track, has numeric flat position/opacity, closed named slots, numeric-map/ordered-fade-array effects, and legacy transition object/string alternatives. It does **not** declare elementRef, and rejects some opaque/revision-bearing transition examples accepted by native authored commands. This is source-schema divergence to keep explicit, not evidence to filter opaque raw rows through that legacy schema or to claim new Runtime acceptance. Current App TS types do declare elementRef and revision-bearing transition (`types/index.ts:89-129,360-399`).

## Capture/read/write guards and preservation

All property captures use `_scalar_commands.py:14-64` `_target` + `_clip_basis`: exact clip id; occurrence id and original source shot identity; `scalar.images` with base parent/source mapping and scalar target/owner bindings; clipType/clip_type, asset/asset_id/media_id/object_id, elementRef/element_ref tagged reads; selected asset's media_id/object_id/digest/content_digest. `clip_set` additionally reads source asset content_sha256. Same-value writes still record authorship and exact before/after. These base/source pins are provenance, not a reason to refresh original leaf guards after unrelated acceptance.

Opacity/position add only their authored leaf writes/clears. They do not read geometry neighbors, timing, params or rewrite containers. Absent, historical present-null, zero and dynamic/opaque old values stay distinct in expect/reads/record/inverse. Opaque namespaces and own JSON keys `__proto__`, `constructor`, `prototype` must remain data; reuse own-property-safe current primitives, never introduce an allowlist or assignment merge that changes their meaning. Ordered arrays retain order and duplicate entries.

Effects `_clip_scalar_commands.py:154-182`: same slot type is a read guard; same-type duration/intensity writes touch only supplied leaves. Params can only echo the exact whole stored params object, then read that container and record supplied leaves. Type change reads/replaces the entire old slot and refuses changed/new params. Object-container creation distinguishes absent/null and records exact before-state; nonobject/array map conversion refuses. Clear retains an exact whole-slot/whole-effects before image, including otherwise unsupported historical data. The UI's reconstructed slot objects must not be mistaken for commands to erase unmentioned opaque members.

Transition `_clip_scalar_commands.py:91-151`: reads original transition and selected identity, target track + owning track id, parent config.output.fps, occurrence MAP_FIELDS, and target plus immediate predecessor identity/media/CLIP_FIELDS and timing RELATIONS at root/app/app.astrid. `transition.predecessor` (`_recording.py:20-33`) has target owner, empty or immediate-predecessor members, **all same-lane clips in stable authored start order**, track boundary and guard-membership policy. Equal starts preserve collection order. Other lanes are independent. Collection membership/order and inverse intervening writes, including same-lane A→B→A, remain guarded (`_collections.py:108-118`). SET writes only the target transition and optional paired elementRef; no predecessor write or neighbor fit requirement.

Positive seconds must quantize to a positive safe whole-frame window: duration*retained rational-fps must be >=0.5 and <2**53-0.5. This is not an integer-seconds*fps requirement, nor permission for App to round authored seconds. Exact half frame is accepted; smaller refused. Canonical owner is always incoming. First/gap/overlap/oversized authoring stays legal; one Agent canonical→compiled conversion owns clamping and half-open ends. Do not reuse element-adapter's adjacent-pair or shortest-clip checks as native capture guards, nor add a policy flag or second App compiler.

Native transition SET replaces the complete raw transition object, including params; missing keys are removed. Changed known parameter values validate without coercion/defaults; unknown JSON is literal. Duration edits must preserve raw opaque members and params. Parameter reset is not authority to drop unknown nested data. Our source probe demonstrates where current callbacks fail this preservation requirement; fixing those remains a separate bounded task.

## Selected schema/read and publication blockers

Exact selected transition ref must match type and any supplied authored revision. A selected shipped built-in requires exact id/kind/revision/packId catalog match and does not use schema_source. Unselected registered built-ins use the existing native catalog schema; unregistered unselected transitions remain opaque, with no renderability claim. Other selected refs without an admitted declaration refuse. Existing unrelated effect elementRef is not silently ignored when SETting a transition; effect-layer targets are refused.

Project-pack changes use `_scalar_commands.py:98-128`: exact `{document_id,version,content_digest}` schema_source, authenticated realm_id, exactly matching `(VerifiedDocument, {objectId:VerifiedDocumentObject})` schema input. The existing native resolver validates owner/project/admission/revision/resource closure/object bytes/build identity; records params.schema, params.snapshot, params.element and retains pinned_documents. A same-type unchanged-params transition can avoid schema resolution unless schema_source is explicitly supplied; changing params/selection needs the exact source. No UI schema/type string/current descriptor substitutes for it.

The previously reviewed official Runtime 0.2.8 supplies `getProjectVerifiedDocument(projectId,pin)` and `getProjectVerifiedDocumentObject(projectId,pin,objectId)`. The approved exact original pin selects the document; its unique matching admission supplies objectId; forward unmodified responses to native capture. A live V2, descriptor label, element revision hash or caller-computed document digest is not original pin authority. Current `runtime/admitted-elements.ts:12-21` selection includes realm/descriptors/authoring paths but no DocumentPin.

**0.2.8 is not the future property union.** At `1ad39f5:contract/schemas/edit-command.json` (SHA-256 `472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9`), ClipSetArgs.values permits only hold; clear is hold/asset/transition. Property-b source schema SHA-256 is `58c3f994fbbd9a3350d35373856513c567b3e231ad7123cf4a9b01feefedfaeb`. A new normal officially generated union, owned Agent pin and reviewed matching cohort are required. Do not edit App generated DTOs, widen a local union or bless 0.2.8 as SET acceptance. App cc4 still declares Runtime contract 0.2.1 (`src/integrations/runtime/generated-contract-metadata.ts`).

Explicit remaining positive requirements, source-inspected and **not rerun**:

- property-b `tests/editing_conformance/test_recipe_effect_fields.py:250-278`: strict xfails for named-slot param edit, param reset/clear, ordered custom-instance add. They stay blocked requirements, not refused features or deleted tests.
- both reviewed branches `tests/sdk/test_timeline_transition_schema.py:54-71`: `test_first_selected_transition_exact_document_inverse` remains strict xfail. Authored transition/ref undo can be exact while manifest still retains a newly introduced DocumentPin. Whole-document inverse is not qualified. Do not bless a selected transition writer cut on payload-only undo.

## Exact golden handoff

Paths below are relative to the Agent repo, under `tests/editing_conformance/fixtures/`, at the fixed candidate SHA named. Existing command/record claims are the reference; no App vector was regenerated or altered here.

| Fixture | Candidate / SHA-256 | Actual coverage |
| --- | --- | --- |
| `recipe_m2_app_clip_scalar_fields.json` | property-b / `8bb75e23c10c9677635d85f33f219b7f1b2d89baf481e3b7ed21f425b76f0c06` | Original 3 commands: child hold, asset clear, parent transition clear. **No opacity command** in this file. |
| `recipe_m2_app_clip_position.json` | property-b / `36707dfbe4bcc7d4ccc770b0be51c5ec005b6184cda8a83310a0ec8cef84ef15` | 3 commands: parent x=-120.5/y=64/1280x720; occurrence cropTop=.125/cropRight=.25; parent eight-field reset. Bundle, commands, records, after_bundle. |
| `recipe_m2_app_effect_fields.json` | property-b / `541866ba55ee3d5cf41c2bfacb21d44fcc1450423ef4f490b36c53174f239cc0` | 4 commands on occurrence:f2-occurrence/clip:f2-agent-clip: fades+entrance/exit, continuous, entrance duration, entrance/continuous clear. Also literal requests and full records/bundle images. |
| `recipe_m2_app_transition_set.json` | both candidates, byte-identical / `ce250ab38b5c7a681bddf618ad2fb55d5fba57290a337d474d1b6b5134e8d747` | Parent f2-transition-clip crossfade .75s, opaque params/outer data, immediate predecessor f2-app-clip; full bundle/command/record/after image. |
| `recipe_m2_app_transition_windows.json` | transition-c / `9152d3d90dc85d511cf3bb142fe26fb15e1316aa6c101418af2f415ac9cb8dc5` | 10 commands/records cases: first, tie/order, gap, adjacent half-open, overlap, oversized, rational 30000/1001 first/adjacent/oversized/exact-half-frame. This file contains commands+records, not full before/after bundles. Reconstruct via `windows_case` in same-SHA test module. |

Opacity has executable native assertions rather than a dedicated portable golden: property-b `tests/editing_conformance/test_recipe_clip_scalar_fields.py:132-196`, especially `test_actual_app_update_clip_opacity_uses_the_clip_set_golden_shape`. Literal SET is parent/clip:f2-app-clip, values opacity .4, clear [], exact expect present(.9), authored leaf/resolved identity. Next capture work needs full native command/record/before/after parity vectors, including absent/null/zero and occurrence isolation; do not pretend the unchanged scalar-fields fixture already contains them.

## Executed checks and limits

From the assigned App cwd:

```sh
node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-property-native-contract-review/notes/app-input-probe.cjs
```

Exit 0, **9 bounded source-level checks passed**. Extracts exact App AST expressions/read functions and runs them in isolation: actual shared Slider scalar→single/bulk opacity; single duration transition preservation; actual PARAM/reset and bulk-duration omission; own-undefined None intent; ordinary config resolver preserving raw opacity/pixels/ordered duplicate fades/own __proto__/unknown params and absent/null/zero. Reset's schema-default function is a deterministic stub to isolate the actual callback's replacement behavior; this is not selected schema validation. No Agent execution, Runtime, React mounting, live UI, network or acceptance claim.

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx src/tools/video-editor/lib/config-utils.test.ts src/tools/video-editor/commands/authoringBundle.sharedOpaqueRemap.test.ts > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-property-native-contract-review/notes/app-targeted.log 2>&1
```

Exit 0; **4 files / 41 tests passed**, 5.53s. Existing App unit tests only; their mocks do not qualify native property ingress. No tests weakened, skipped, rewritten or added to the repo. Additional read-only `git show`/JSON/AST comparisons confirmed exact SHA/tree/fixture hashes, 0.2.8 schema's bounded SET and identical transition recipe/golden across the two reviewed sources. `git status --short --untracked-files=all` is clean after tests.

Not run/requested: Agent suites (avoided duplicating candidate-green proof), Runtime suites, full suites, central test requests, browser/live sockets, build/install/project tsc, renderer, real public retained reads, native App captures, accepted reload/retry/inverse, audiovisual parity or zero-legacy-traffic tests. Those remain release/migration evidence, not conclusions of this source review.

## Next step

Manager: review this KEEP report, then export it to the requested flat handoff path. Owners first qualify the new official property union plus owned Agent pin. Then dispatch **one opacity capture-only worker** using `notes/next-opacity-worker.md`. Keep transition/effects/position, selected-Pack inverse fixes, root/pin adoption and independent full gates outside that worker. Existing writers stay until each actual migrated ingress proves reload/undo/retry and zero legacy traffic, with its own deletion-ledger row.
