# App M2 producer host-field source mapping

Status: mapping complete, with the Runtime empty-owner HOLD retained. There is no ACK or activation recommendation. No App product files or live callers changed.

## Immutable source identities

- New Agent producer source: commit `57af3fffe192ad369c4282d9ab3a67efd57dc51c`, tree `319013e799d244497deac26719282595c213b658`. The source schema hash is `0b747d87c763a8f0ba0dcc5027390ab04d6296cfddfffa8c049020334ca3ec92`.
- App origin/main baseline used for the upstream trace: commit `860d43b331fb4422b16bc0dbd7b08666a0c766a0`, tree `ea4eabb8eb469df63fd1d515f84982d85b2f14cc`.
- App transcript witness: commit `1557c312b999ddc0a21c1728acbc64052ef6491f`, tree `cf94daef960fe1426f6f50e4000b00c0fc42867e`.
- Current App integration worktree: commit `6e267027137f11288a8e20ee8cf226209be60408`, tree `b65cd465f0865c77ceb73d29f105c7d6d2c18b53`.
- The separate App position-source witness is Agent commit `f2a2cfbb58926b7c9d47d206ae294acf376b0c2e`, tree `8c5674a5e329ab8dc5dcb4711251268a61b81847`. It is relevant only for the flat geometry/crop leaves, not for producer ownership.

The requested App2 STATUS and INBOX were read from `scratchpad/orch/managers/app2/STATUS.md` and `scratchpad/orch/managers/app2/INBOX.md`. The requested separate HOME STATUS file was not present in the available scratchpad or repo paths; no decision from it was inferred.

## What the App currently authors

The current transcript regeneration path in `src/tools/video-editor/dev/transcript-lane/extension.ts` is the clearest existing producer witness:

- `288-305` computes the caption box and source item values.
- `394-402` constructs the raw output fingerprint: `track`, `at`, `duration`, `clipType: "text"`, `label`, `text`, and flat `x`, `y`, `width`, `height`.
- `403-420` constructs `app.__generated__` with the extension id, contribution id, source schema, source item/revision/value, output value, and conflict policy.
- `421-433` preserves an existing generated caption in preserve mode; fresh creation is only `clip.add` with `track`, `at`, and `clipType: "text"`.
- `435-449` refreshes an existing caption with `hold`, flat geometry, `text`, `label`, and `app.__generated__` using the existing direct patch shape.
- `452-463` removes stale outputs only when track, generated extension id, contribution id, and source-schema provenance all match. This is owned stale removal, not general deletion.

The raw authored field inventory is in `src/tools/video-editor/lib/timeline-data.ts:44-76` and copied into the next clip at `170-204` and `320-355`: root `track`, `at`/timing, `hold`, `label`, flat geometry, crop fields, `text`, `params`, and `app`. The transcript path writes the root timing, label, text, and geometry fields plus `app.__generated__`; it does not write `params`. The real association fixture at `src/tools/video-editor/commands/transcriptAssociateCapture.test.ts:82-108` contains `hold: 2.3`, `text.content`, `text.color`, `text.fontSize`, an opaque root sibling, an opaque app sibling, and generated provenance. Its assertions at `162-223` require those values and siblings to survive. That fixture has generated metadata but no `app.managedBy`, so it is field/opaque-value evidence, not proof of new producer ownership.

The current scene-phase marker path provides the timing positive. In `src/tools/video-editor/dev/scene-phase-markers/extension.ts:660-728`, same-track alignments become one `clip.move` with `at` and one `clip.update` with `hold` per member; cross-track and mixed cases retain the guarded legacy shape. Fresh shot creation at `539-583` and `614-657` is `clip.add` followed by a hold/label update. The real positive fixture `src/tools/video-editor/commands/fixtures/ordinary_real_batch.json` and `src/tools/video-editor/commands/ordinaryRealBatch.test.ts:9-50` cover five members, each with move then hold, including parent and occurrence clips. The scene tests at `src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts:749-850` assert exact move/hold values and the cross-track fallback.

## Mapping by behavior

### Fresh creation

The current App fresh transcript carrier is incomplete for the Agent producer source: `extension.ts:421-433` creates a minimal `clip.add` with no `hold`, `app.managedBy`, `app.__generated__`, `label`, `text`, or geometry, then relies on the legacy update at `435-449`. The current scene creator has the same two-phase shape at `539-583` and `614-657`.

Agent `ClipAddArgs` at `astrid/core/timeline/schema/edit-command.schema.json:818-858` requires a complete parent-owned row including stable `id`, `clipType`, `track`, `at`, and positive `hold`. Agent `clip.set` producer handling is an existing-clip field carrier; it does not establish a new managed owner. Therefore the concrete missing existing carrier is the fresh row that establishes `app.managedBy` and generated identity while also carrying the required authored timing/host fields. The current App minimal add plus legacy update cannot be treated as the proposed producer carrier. This is a carrier mismatch, not a guessed operation-name issue.

### Stale owned removal

Transcript regeneration has a concrete, provenance-guarded removal positive at `extension.ts:452-463`, with the corresponding expectations at `transcriptLane.test.tsx:1065-1102`. Preserve mode does not remove stale outputs (`877-939`); explicit regenerate mode does. The Agent producer proposal does not add a stale-removal behavior. Keep this existing App safety case separate from producer field refresh, and do not broaden removal to foreign or user clips.

### Timing move/hold

The kept positive is already mapped to the ordinary safety case: scene markers emit `clip.move {at}` and `clip.update {hold}` for same-track members (`extension.ts:660-728`), and the real five-member fixture asserts all ten operations (`ordinaryRealBatch.test.ts:9-50`). The producer source can account for a host `hold` field on an existing clip, but it does not replace the separate move carrier or make cross-track/mixed batches native. No change is proposed to the guarded fallback.

### Existing host-field refresh

Agent source `57af3fffe192ad369c4282d9ab3a67efd57dc51c` extends the existing `clip.set` carrier. In `astrid/sdk/timeline/_clip_scalar_commands.py`, its producer implementation reads and validates `app` at lines `19-47`, writes known app/text/root leaves at `154-162`, and preserves opaque text siblings at `49-59`. The source schema accepts root `label`, text leaves (`content`, `fontSize`, `color`, `bold`, `align`), and app `managedBy`/`__generated__` leaves at `astrid/core/timeline/schema/edit-command.schema.json:2576-2672`.

That overlaps the existing transcript refresh values at `extension.ts:435-449`: `hold`, `label`, text leaves, and generated metadata. It does not cover the App's flat `x`, `y`, `width`, `height` geometry or crop fields. Those are the separate position-source subset evidenced by `timeline-reader.ts:905-934` and the position witness; they must not be invented as producer `params` leaves. `params` remains an independent raw root carrier in `timeline-data.ts:44-76`, and no current transcript or Agent producer source maps it. The concrete semantic mismatch is therefore twofold: the producer source is an existing-owned-field refresh, while current fresh App creation has no owned row carrier; and App geometry is flat root data while the proposed producer subset does not carry it. The safe kept positive is only the overlapping existing host-field subset.

## Ownership and refusal checks

- Agent's exact producer conformance lane passed three positives, including preservation and refresh behavior. The same source's negative cases reject a user/unowned clip and a foreign managed clip with `unsupported_ownership`; an exact-source probe reproduced both refusals.
- App's `src/tools/video-editor/lib/timeline-reader.ts:129-153` only derives managed ownership from a nonempty string `app.managedBy`; empty ownership is not treated as managed by the App reader.
- The Runtime source review found a separate persisted-empty `managedBy`/`extensionId` acceptance path in the new producer implementation. That is the declared Runtime HOLD. It is not repaired or re-qualified here: no ACK, public pin, activation, or broader save behavior is recommended. Until Runtime rejects that malformed existing owner, the empty-owner case is not a qualified positive.

## Verification

App targeted tests:

`npm exec vitest run --no-cache --configLoader=runner src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts src/tools/video-editor/commands/ordinaryScalarMember.test.ts src/tools/video-editor/commands/ordinaryRealBatch.test.ts src/tools/video-editor/lib/timeline-reader.test.ts src/tools/video-editor/lib/managed-object-guard.test.ts`

Result: 6 test files passed, 183 tests passed, 8.74s. The npm `cache=false` config warning was non-fatal.

Exact Agent-source producer lane, run from a temporary archive with the shared read-only environment and no repo edits:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$SRC_TMP:/home/user/work/runtime" /home/user/work/venv-app2-native/bin/python -m pytest -q -o addopts= -p no:cacheprovider "$SRC_TMP/tests/editing_conformance/test_recipe_producer_clip_set.py"`

Result: 3 passed, 2 warnings in 0.76s. The warnings were unknown local pytest timeout configuration. No full, browser, localhost, or live-socket suite was run.

Changed live callers: none. Product edits: none.

## Next step

Repair and regression-test the Runtime persisted-empty-owner rejection first. After that, compose the existing App fresh-row carrier, producer field-refresh subset, position subset, and guarded timing/removal positives as separate qualified cases. Do not activate or publish the producer mapping before that repaired Runtime evidence exists.

Commit message and completion marker are recorded at the paths named by the task.
