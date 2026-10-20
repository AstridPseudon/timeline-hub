# App2 currentroot element port review

Date: 2026-10-20
Base: `05b6b488d..d4850f997` (`tl/ap2-m2-element-currentroot-port`)

## Verdict

**REQUEST CHANGES — source. HOLD — consumer/row.**

The two-file port contains no deleted dependency, old cohort, old pin/root,
shared-session, door, outbox, serializer, package, generated, or fixture
change. The element-revision helper is native-parity correct on the actual
currentroot TypeScript output. The literal PARAM helper is not: its submitted
read sequence is rejected by Agent 310e. Therefore the source is not approved.

This is not an old-positive-behaviour-loss claim. The bounded local tests pass;
the finding is that this new currentroot recording implementation does not yet
produce the native PARAM record.

## Source findings

### Element revision

`captureClipElement`/`finishClipElement` preserves the repaired behavior:

- target identity and occurrence ownership are recorded;
- both `elementRef` and `element_ref` are read, in that order, even when the
  first alias is present;
- existing element identity/kind/selected-pack ownership is guarded;
- the write is to canonical `elementRef`, with the old alias cleared when it
  exists;
- selected project-pack capture remains visibly unsupported until the
  authenticated Agent schema/realm seam exists.

The actual TS-produced element command was accepted by Agent 310e and matched
Agent execution exactly: command, record, and after-bundle all matched.

### Literal PARAM recording defect

For an asset-backed occurrence clip, the currentroot TS command reads, in
order:

```text
id, occurrence.occurrence_id, occurrence/shot.shot_id,
elementRef, element_ref, clipType, clip_type, asset, asset_id, media_id,
object_id, params
```

Agent's authoritative `clip.set-params` capture reads:

```text
id, occurrence.occurrence_id, occurrence/shot.shot_id,
clipType, clip_type, asset, asset_id, media_id, object_id,
elementRef, element_ref,
occurrence/registry.assets.old-picture.{media_id, object_id, digest, content_digest},
params
```

The current helper checks the aliases before the scalar identity loop, so the
recorder deduplicates them in the wrong position. It also never records the
asset-registry media reads. Sending this actual TS-produced command to Agent
310e fails with:

```text
submitted reads does not match authoritative capture
```

The local implementation does preserve explicit clears, unknown literal
values, unchanged-value writes, and opaque JSON in the exercised bundle, but
those semantics do not compensate for the rejected native record. Repair the
PARAM recorder from the native identity/read order and registry-read behavior,
then rerun exact command/record/bundle parity for both element and PARAM.

### Selected-pack boundary

Selected project-pack element and PARAM capture correctly fail closed with
`selected project pack capture requires authoritative Agent schema capture` and
retain the draft. No local schema synthesis or retained-JSON authority is
approved. This remains unsupported until authenticated realm identity,
`schema_inputs`, admitted snapshot, descriptor validation, and the native
`params.schema`/`params.snapshot` dependencies and `params.element` binding are
available through the provider seam.

## Consumer HOLD

The helper is unwired. A repository scan found no consumer import; the current
`ElementsLibraryPanel` still calls the legacy `elementOperationAdapter` for
`timeline.apply_element` and `timeline.apply_transition`. Do not call this row
done, remove the adapter, or claim zero legacy traffic.

The proposed shared artifact in the port handoff is prose/pseudocode, not an
applicable patch. Source review does not approve it. Exact missing wiring is:

1. Add a currentroot `elementPort` to the existing command session: capture a
   stable authored bundle/clip basis, finish against that original basis, and
   submit only the prepared command through the existing outbox/Runtime door.
2. Expose that port through `useTimelineCommandSession` and
   `VideoEditorProvider` with the existing legacy-clean barrier; preserve the
   selected-pack refusal until authenticated Agent inputs are forwarded.
3. Change `ElementsLibraryPanel` only for qualified existing-clip element
   revision and literal PARAM edits; preserve the raw basis through preview and
   submit, and never recapture from the ACK/display projection.
4. Qualify complete operation families before deleting the old adapter/route:
   element clip placement/animation, overlay creation, element update and
   removal, fade/entrance/exit, transition apply/update/removal, and creation or
   full-panel apply. These are not translations of `clip.set-element`; each
   needs an explicit native operation or a visible unsupported-operation
   refusal with the draft untouched.

No consumer or writer deletion is included in this review.

## Verification

- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/elementCapture.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/runtime/element-adapter.test.ts` — **3 files, 97 tests passed**.
- Temporary minimal closure config plus `./node_modules/.bin/tsc -p review-tsconfig.json --pretty false` — **passed**; the temporary config was removed.
- Actual TS element probe, piped to Agent 310e read-only using `/home/user/work/venv-app2-native/bin/python` and the private Agent source — **validate accepted; execute accepted; command/record/bundle exact**.
- Actual TS PARAM probe, same read-only Agent environment — **rejected** with `submitted reads does not match authoritative capture`; the native expected sequence is recorded above.
- Prior native repair evidence: `test_recipe_clip_set_element.py` **30 passed** and repaired literal element parity passed; this review did not rerun a full Agent lane.

No full, browser, live-socket, Runtime, package, pin, generated, or shared-file
suite was run.
