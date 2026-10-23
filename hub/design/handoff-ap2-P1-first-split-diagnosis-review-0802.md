# Handoff: independent P1 first-split diagnosis review

## Result

Independent review confirms both source-derived causes in `handoff-ap2-P1-first-split-conflict-sol-0747.md`. Agent and App findings each **PASS as causal diagnoses**; the requested P1 behavior remains **H3 NO-GO**.

## Agent finding — confirmed

Current Agent `e49a6e76b3ab363e312c55b313714af1f845f54b` and pinned Agent `f894c3c9dda25ab03527eeb7f52da5da31d627c1` retain identical causal methods:

```text
astrid/sdk/timeline/_doc_patch.py: normalized_path, value_at, validate_payload,
patch, Closure.native_sites, Closure.install
astrid/sdk/timeline/_recording.py: Recording.compile_mirrors
```

`Closure.native_sites` maps an id-addressed parent clip leaf to only `parent/clip:<id>` (`_doc_patch.py:184-187`). `Closure.install` writes only that site (`:222-237`). `Recording.compile_mirrors` updates `config.clips` only when `commands.py:243-250` calls it at command completion. Consequently, after insert/hold/label changes, the primary row is changed while the config mirror is stale. The later output-file change in the same `doc.patch` reaches `_doc_patch.py:415`, where `validate_payload` (`:261-264`) rejects `identity_conflict: contradictory parent mirrors`, path `['clips']`.

The independent provider witness preserved 13 reads, exact `order_before=[p1-chain-source]`, and exact previous operands. With base equal to current and no intervening edit:

| mode | pinned f894/Runtime34e | current e49/Runtimea5d |
|---|---|---|
| original order | exit 2, `identity_conflict`, `contradictory parent mirrors`, `['clips']` | same |
| output-first control | exit 0, accepted, 13 reads | same |
| bad previous | exit 2, `previous_value_mismatch` | same |
| bad order | exit 2, `original collection order changed` | same |
| bad declared read | exit 2, declared hold read mismatch | same |

The output-first result is a causal control, not a workaround or recommendation.

One precision correction: `_doc_patch.py` as a whole is not byte/AST-identical between f894 and e49 because current `Closure.__init__` accepts `source_bundles=()` and passes it to `document_from_bundle`. The causal methods listed above are equal, and this unrelated staging change does not affect the diagnosis.

## App finding — confirmed

The production caller remains:

```text
useClipSplitting
  -> useClipEditing.applyConfigEdit
  -> useTimelineCommit
  -> serializeForDisk / buildDataFromCurrentRegistry
  -> timelineLocalSaveHandoff.capture
  -> documentPatchIntent
  -> localSaveSession persisted outbox
```

`editor-utils.ts:283-345` split semantics only change the source hold and new row ID/position. But `useTimelineCommit.ts:529-539` serializes the resolved config. `serialize.ts:146-190` uses resolved clips and removes output from persisted data. `timeline-data.ts:450-475` then restores missing output defaults and applies `deriveTimelineClipDisplayNames`. `timelineLocalSaveHandoff.ts:187-195` and `documentPatchIntent.ts:150-168` treat those rebuilt differences as authored intent.

The independent real-module App probe used raw source label absent, output file `out.mp4`, and registry `p1-video.mp4`. It observed serialized/rebuilt source label `p1-video.mp4`, serialized output absent, and rebuilt output `output.mp4`. Its Vitest control passed: 1 test file / 1 test.

## Evidence boundary and ownership

This is source-derived causal evidence. The original exact request, realm, and trace were deleted; no byte-exact replay claim is made. The full-v2 request/reply contract remains retained. No guard weakening, fixture change, output-first workaround, fabricated reads, new executor, publication waiver, or production edit was made.

Agent owner: repair per-change authoritative mirror synchronization while retaining contradictory-mirror validation, previous-value/order/read guards, bindings, authentication, and final Runtime checks.

App owner: preserve authored/absent label provenance and raw output through the existing serialization/rebuild seam; do not turn derived display/default values into patch intent.

The original accepted/merged/refused mixed chain, new-ID trim, Agent intervention, lost ACK/restart, exact retry, history and undo remain unverified. H3 stays NO-GO until separately authored corrections and manager-owned integrated P1 evidence pass.

Durable worker detail and exact command paths are in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P1-first-split-diagnosis-review-0802/WORKERreport.md`
