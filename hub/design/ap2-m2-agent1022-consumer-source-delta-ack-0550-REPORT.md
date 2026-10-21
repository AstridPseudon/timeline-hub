# App2 consumer source-delta review: Agent complete1022

Date: 2026-10-21 UTC

## Verdict

**BOUNDED SOURCE ACK.** No executable incompatibility was found for the
already-existing App2 transcript and selected-media families. The ACK is
limited to those families and does not authorize App product changes,
generated-client changes, schema generation, version allocation, pinning,
activation, or caller retirement.

Exact reviewed Agent source:

- feature: `10226a7f08a739ba3e41f8e91de6971eed63aa9d`, tree
  `e2c08fbe9b21a3082db7bcf62d9677babfc15e98`, parent
  `9502e3ebdf43c9759fe1445a91d32599822cc1d0`;
- raw-OLD base: `9b9baa01ab43bce144f3f1e6d6d73722df99a8e7`, tree
  `f924720e382d442f391d45cdc6e24064be9a6a5e`, parent `5672d2b`;
- feature schema: raw `9cb9597a618f51949fe9ec35686e544dca812b8b252a96a4cff1f686afdfb3ec`,
  canonical `322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc`,
  65 definitions / 37 closed clauses;
- raw-OLD schema: raw `9e4b4421ebbba94f13f8f286c7ea1df5eb9ca128142ed904c92a993985954cfd`,
  canonical `d3274d7ed2d4bd80691472dd94daf8f4b8041fc184f39f1dd562d5de5d6a15c2`,
  64 definitions / 36 clauses.

The final feature commit changes only the transcript-association test EOF over
its immediate parent; the semantic delta represented by the reviewed 65/37
composition is the closed `transcript.associate` definition/clause and its
native handler. No App caller is changed.

## Compact operation/carrier delta

| family | exact Agent source shape | current App2 carrier/consumer | delta disposition |
|---|---|---|---|
| `transcript.associate@1` | Closed parent-asset command; exact new and prior `DocumentPin`; source item selection/order; nested `parent.config.bundle.transcriptReferences` + `itemsBySchemaRef`; deterministic caption/review reconciliation with collision/ownership refusals. | Dormant `captureTranscriptAssociation` / `finishTranscriptAssociation` uses the same nested bundle plane, exact new/prior pins, ordered rows, opaque-row retention, and refusal rules. | **SOURCE ACK / compatible.** Keep dormant; no activation. |
| Existing parent `clip.swap-media@1` | Existing five-field `selected_media` for old and new selection; raw-OLD `MediaManifestEntry` is the separate additive `@2` successor. | `parentClipSwapCapture` emits unchanged `clip.swap-media@1` with exact five-field `MediaSelection` and `ownership: parent`. | **SOURCE ACK / unchanged.** No raw-OLD `@2` caller is inferred. |
| `project-data.write` removal | Exact Agent handler supports only the existing operation with `mode: "remove"`; missing/null/empty distinctions, ordered namespace pruning, and exact inverse are carried by `_recording.assign/clear(insertion_order)`, `_command_state.set`, and inverse. | App `projectDataMember.ts` currently validates/writes `mode: "replace"` only; no normal App remove lowering or generated remove type is present. | **HOLD, not an Agent mismatch.** The required Agent carrier is present and available for later normal generation; App adoption must use generated output, never a handwritten cast/type. |
| Fresh-caption Main joint `0447` | The exact Agent schema/handlers contain `transcript.associate`, not Main's ordered `clip.add` + rich `clip.update` native recipe. Existing transcript reconciliation can refresh already-owned caption/review rows only. | Main/App patch path remains the legacy `buildTranscriptCaptionPatch` / `compileTimelinePatch` mixed batch; no complete native lowering is present. `managedBy` remains absent in the observed Main row. | **MISSING / HOLD.** Do not claim the joint fresh-caption recipe or retire the fallback. |
| Literal position | No `x`, `y`, `width`, `height`, or crop leaves in this exact 65/37 `ClipSetArgs`; no position handler is added by this source. | App geometry mapping is a UI lowering concern only; current generated App command types do not expose these Agent fields. | **MISSING from this source composition.** |
| Effects leaf | This exact `ClipSetArgs` has `opacity` only; no `effects.fade_in` / `effects.fade_out` schema or handler. | Existing App effects/fade producers remain separate legacy behavior. | **MISSING from this source composition.** |
| Coupled fade | No paired `effects` + `entrance`/`exit` handler exists in the exact source. The existing carrier-fit review is for a future closed `clip.set` cohort only. | App `clip.set-fade` and Main coupled producer remain live and unqualified for native lowering. | **MISSING / HOLD.** |

## Consumer checks

The dormant transcript implementation was read at
`src/tools/video-editor/commands/transcriptAssociateCapture.ts`: it rejects
legacy parent-level planes and nested `sourceItemsBySchemaRef`, requires
`config.bundle.itemsBySchemaRef`, preserves unrelated rows/order, distinguishes
absent/null, and retains exact prior pins for replacement. The existing App
tests cover the nested plane, ordered replacement, opaque rows, inverse/replay,
collision refusal, and legacy-carrier refusal.

The exact Agent project-data source does contain the required ordered inverse
carrier for future normal generation: `_recording.py` records
`insertion_order`, `_command_state.py` uses it for clear placement,
`inverse.py` consumes it, and `_project_data_commands.py` passes it when
pruning a target namespace. App's current writer does not consume that remove
form, and `src/integrations/runtime/timeline-commit-types.ts` is still the
older generated `ClipSetArgs`/public surface. This is therefore a future
generated-counterpart prerequisite, not permission to edit generated TS or
add a cast.

Raw-OLD media semantics remain unchanged: existing `clip.swap-media@1` keeps
the five-field selected-media envelope; the additive raw-OLD `@2` uses the
two-field `MediaManifestEntry` old pin and the existing exact five-field
`selected_media` new pin. App has no `@2` caller in this source.

## Evidence

Compact existing-seam probe, run in the clean App worktree:

```text
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/commands/transcriptAssociateCapture.test.ts \
  src/tools/video-editor/commands/projectDataMember.test.ts \
  src/tools/video-editor/commands/parentClipSwapCapture.test.ts
=> 3 test files passed, 24 tests passed
```

Independent Agent/Runtime evidence was reused rather than repeating broad
source floors: Runtime complete1022 review reports 14 focused + 5 floor checks;
raw-OLD Runtime review reports 69 focused checks; the transcript successor
reports 186 broad composition checks plus 13 compact checks. No full, browser,
HTTP/socket, install, native, generation, release, pin, or activation run was
performed here.

## Suggested short reply

**Agent:** `SOURCE ACK` for complete1022/e2c08 only at the existing App2
transcript.associate and selected-media@1 seams. Nested bundle, exact new/prior
pins, ordered rows, raw absence/null, opaque retention, and refusal behavior
fit. Project-data remove's insertion-order carrier is present in Agent but App
has no generated normal consumer yet. Fresh-caption joint0447, literal
position, effects, and coupled fade are not in this exact source/handler.

**Runtime:** `SOURCE ACK` with no current mismatch for those bounded families;
retain current b92/public014 and raw-OLD MediaManifestEntry/selected_media
semantics. No 0.2.16 artifact, version allocation, generation, pin, activation,
or live caller change follows from this review.

Live callers unchanged. No App product/source/generated/schema/pin change was
made.
