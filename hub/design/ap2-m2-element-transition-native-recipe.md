# M2 element transition native recipe

Date: 2026-10-20

Verdict: native recipe is executable on the reviewed Agent transition candidate, but apply/update are not live on the current Agent integration pin. Removal is already expressible by the current Agent operation and App's live scalar-clear seam. This is a recipe and seam handoff only; no product writer or row is retired.

## Sources and boundary

- App element-row handoff: `handoff-app-to-app2-element-routes.md`, source branch `timeline/app/tl/app-m2-ordinary028-current-safety-compose` at `55e7e217b4adc2c57315e22ce0bebfc36a436ffa`.
- App live None seam: App commit `90f39e080ded099a0c73893f26c91b51b2abcc74` (`fix(timeline): retain native transition clears in atomic bulk edits`). This is App-owned D01-app-transition-none-serialization; reuse it, do not duplicate or edit it in this row.
- Current App element ingress is `src/tools/video-editor/components/ElementsLibraryPanel.tsx` -> `runtime/element-adapter.ts`. It currently performs a whole-config CAS save.
- Current integrated Agent is `/home/user/work/agent` at `f133a87986d839d7716d3efac2c2ba25fe036098`.
- Native SET evidence uses a private extraction of reviewed Agent ref `tl/agt-m2-transition-set-c` at `48b17eb4550abc23826bb7687a01378753ec84cc`, not the current integration pin.

## Exact recipe

The adapter ingress remains the semantic front door, but its mutation must become a thin producer through the existing App scalar capture/session seam. It must not call `saveTimeline`, `saveTimelineAtHead`, a resolved-document serializer, or a second transition store.

1. Resolve authority from the current selected catalog entry. `ElementsLibraryPanel` already supplies `{id, kind, revision, packId?}` from `editorContext.elementContext.catalog`; use that exact descriptor after the existing `refreshAdmittedElementRef`/admitted-catalog refresh. Do not construct a descriptor from an ID, a type-only cache, an authored `app.elements` record, or a stale panel snapshot.

2. Capture the raw target through the existing `clipScalarPort.capture({clipId, ownerRef, current})`. Use the returned stable `select` and original `localBasis`; never infer `parent/clip:<display-id>` when the projection binding identifies an occurrence. The current App session verifies scope/head, one displayed identity, and matching raw owner before it returns the basis.

3. Preserve the existing adapter's placement and duration policy at the producer boundary. `from_clip` is the predecessor; `to_clip` is the incoming target. Keep the current same-track adjacency check and visible-duration calculation for this ingress. Default duration is `entry.defaults.durationFrames ?? 8`, converted to authored seconds as `frames / retained_fps`; an explicit `duration_frames` uses the same conversion. No outgoing conversion, successor fit, or direction inversion is allowed. The canonical `clip.transition` field is INCOMING and belongs to the TO clip.

4. For `timeline.apply_transition`, finish one native `clip.set` against the TO clip:

   ```json
   {
     "values": {
       "transition": {
         "type": "<descriptor.id>",
         "duration": "<frames / retained fps>",
         "revision": "<descriptor.revision>",
         "params": "<complete authored params when present>",
         "<opaque transition keys>": "<unchanged values>"
       },
       "elementRef": {
         "id": "<descriptor.id>",
         "kind": "transition",
         "revision": "<descriptor.revision>",
         "packId": "<descriptor.packId when present>"
       }
     },
     "clear": []
   }
   ```

   `elementRef.id` must match `transition.type`; kind/revision/pack owner must match. For a selected project-pack transition, `schema_source`, `realm_id`, and verified immutable `schema_inputs` come only from the existing Agent/provider authority. If that capture is not available, refuse before preview/prepared registration/outbox/network; do not synthesize a pin or cache.

5. For `timeline.update_transition`, capture the original target transition and element reference, then replace only the requested known fields in a complete raw transition object. Preserve all unmentioned own keys, nested params, null/absent distinctions, and existing revision/pack identity. If a new descriptor is supplied, it must be the refreshed exact authority and must match the resulting transition. If no descriptor is supplied, the existing raw ref must resolve uniquely in the current verified catalog; the old adapter's synthetic `legacy` fallback is not an authority and must not be used by the native producer.

6. For `timeline.remove_transition`, reuse App's existing scalar clear capture exactly:

   ```text
   args = { values: {}, clear: ['transition'] }
   ```

   Single remove uses `captureClipScalarEdit` + `submitClipScalarEdit`. Bulk remove/None uses `submitClipTransitionClears`, which calls the existing `finishBatch`/`submitBatch` and enqueues one command group. The native clear removes only `transition`; it deliberately leaves `elementRef` and every opaque sibling field untouched. Do not use the current local adapter branch that destructures both `transition` and `elementRef`.

7. Preview is the existing leaf-only `clipScalarPreview`: one `clip.update` per target with `payload` containing the complete transition SET or `clear: ['transition']`. `finish` re-executes the original command claims on current raw bytes, registers the prepared entry, and submits through the existing outbox/Runtime `/v1` path. A lost ACK/restart retries the exact command body/key; it does not reselect the descriptor, predecessor, fps, params, or pack revision.

8. Native Agent records and guards the target identity/source, owning track, retained fps, and `transition.predecessor` selection (members, stable same-lane order, and track boundary). Inverse is the existing guarded inverse over the accepted publication. Replay uses the original captured body. An intervening same-lane write or A→B→A transition write refuses; disjoint-lane replay remains allowed.

## Representative native command

Using the existing App three-products fixture (`PARENT = parent/clip:f2-transition-clip`, stable predecessor `parent/clip:f2-app-clip`, fps 30), the reviewed Agent candidate emits this SET body:

```json
{
  "op": "clip.set",
  "version": "1",
  "select": "parent/clip:f2-transition-clip",
  "args": {
    "values": {
      "transition": {
        "type": "crossfade",
        "duration": 0.75,
        "params": {"future": {"literal": [null, false, 0, "", "ƒ(x)"]}},
        "future": [null, 2.0]
      }
    },
    "clear": []
  },
  "intent": {},
  "resolved": ["parent/clip:f2-transition-clip"],
  "selections": [{
    "key": "transition.predecessor",
    "owner": "parent/clip:f2-transition-clip",
    "members": ["parent/clip:f2-app-clip"],
    "order": ["parent/clip:f2-app-clip", "parent/clip:f2-transition-clip"],
    "boundaries": ["parent/track:V1"],
    "policy": "guard-membership",
    "query_version": 1
  }],
  "bindings": {"scalar.target": "parent/clip:f2-transition-clip"},
  "created": []
}
```

The complete native command additionally contains the exact raw reads and `expect` guard for the original `{type: crossfade, duration: 0.5}` transition. The recorded write is exactly one leaf:

```text
parent/clip:f2-transition-clip.transition:
  present({type: crossfade, duration: 0.5})
  -> present({type: crossfade, duration: 0.75, params: {future: {literal: [...] }}, future: [null, 2.0]})
```

For apply, add the matching `elementRef` in the same `clip.set` values object. For remove, use the clear body above; its `expect` is the original transition value and its write is transition -> absent.

## Evidence

Private, read-only runs; no shared dependency or repo source was changed.

- App live-None source `90f39e080ded099a0c73893f26c91b51b2abcc74`: focused Vitest on `TransitionPreservation.test.tsx`, `clipScalarCapture.test.ts`, `clipScalarGesture.test.ts`, `commitSession.clipScalar.test.ts`, and `runtime/element-adapter.test.ts`: **5 files, 113 passed**. This includes single/bulk None removal, one atomic bulk command group, refusal before mutation, exact retry/recovery retention, and opaque transition preservation.
- App handoff source `55e7e217b4adc2c57315e22ce0bebfc36a436ffa`: focused Vitest on element adapter/panel plus scalar capture/gesture/session neighbors: **5 files, 87 passed**.
- Current integrated Agent `f133a87986d839d7716d3efac2c2ba25fe036098`: existing App scalar fixture lanes: **18 passed, 80 deselected**. The clear fixture proves exact raw transition removal, inverse/redo, replay, stable IDs, and unchanged sibling/opaque data.
- Current integrated Agent exact SET refusal, using the same fixture and `capture_clip_set(... values={'transition': ...})`:

  ```text
  CommandError: Additional properties are not allowed ('transition' was unexpected); kind=invalid_edit_command
  ```

- Current integrated Agent exact `clip.set-element` refusal for applying to the fixture target with no prior element reference:

  ```text
  CommandError: clip.set-element requires an existing element ref; kind=invalid_edit_command
  ```

- Reviewed Agent candidate `48b17eb4550abc23826bb7687a01378753ec84cc`: `test_recipe_transition_set.py`: **41 passed in 12.44s**. This proves the representative App fixture SET, opaque values, canonical incoming predecessor selection, first/gap/overlap/oversized windows, rational fps, explicit clear, inverse/redo, replay, same-lane guard refusal including A→B→A, and selected builtin/project-pack authority cases.

Not run: full suites, browser, localhost, sockets, Runtime-door acceptance, or live authenticated App. The candidate result is not a qualification of the current integration pair.

## Exact Agent contract request

Current Agent has the needed clear operation (`clip.set` with `clear: ['transition']`) but not incoming transition SET or paired first-use `elementRef` application. Request the smallest existing-operation extension from Agent: reconcile the reviewed `48b17eb4` transition-set-c implementation into the current canonical Agent schema/registry without adding an operation, DTO, endpoint, pin, store, or cache. It must retain current definitions and current INCOMING meaning, then publish the normal generated pair before App consumes it. The native contract must admit the existing `clip.set` values `{transition, elementRef}` and optional existing `schema_source` only for verified selected project-pack inputs, with the candidate's predecessor/track/fps/source guards and opaque-field recording.

Until that pair is integrated and frozen, `timeline.apply_transition` and transition SET/update remain visibly unsupported at the native producer boundary. Do not fall back to the existing adapter whole-document save.

## Peer seam request to App

Please expose the already-owned `clipScalarPort` path to the element-adapter producer after the Agent pair is published:

- keep `captureClipScalarEdit`, `submitClipScalarEdit`, `submitClipTransitionClears`, `finishBatch`, `submitBatch`, and the existing `OutboxBasis`/preview checks;
- extend the existing `clipScalarCapture` argument typing/finish path only to pass the official native transition SET and paired `elementRef` body, preserving the full raw transition object and verified schema inputs;
- route adapter apply/update/remove through that port, with apply/update one command group and bulk remove one command group;
- leave App's D01 None serialization implementation as the owner and do not copy it into element-adapter;
- make the native remove result clear transition only, preserving elementRef and opaque fields;
- keep unsupported selected project-pack authority visibly refused with the draft intact.

Qualify the actual consumer with accepted commit, reload, guarded undo, exact retry/restart, and zero legacy element-adapter save traffic before any deletion-ledger or row-retirement claim.

## Next worker brief

On a current-root App/Agent pair with the normal generated transition SET contract frozen, replace only the element-adapter mutation producer seam. Use the existing catalog refresh and scalar capture/session/outbox code. Prove one apply, one update preserving opaque keys, one remove preserving `elementRef`, and one bulk remove group against the current element fixtures; submit the exact TS-produced commands to Agent validation/execution, then run the bounded accepted/reload/undo/retry/refusal tests. Refuse selected project-pack writes without authenticated verified inputs. Do not edit D01 None code, add a parallel op/schema/DTO/store/API, or claim row retirement until the legacy traffic and end-to-end gates pass.

