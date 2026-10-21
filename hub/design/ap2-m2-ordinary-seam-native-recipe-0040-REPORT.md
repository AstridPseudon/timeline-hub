# App2 ordinary seam patch ingress — worker report

## Result

No App source change is safe for this row. The live visual-seam acknowledgement is authored film state, but the current pinned Agent recipe/registry has no command that writes the timeline `app.visualSeamContract` namespace. The render seam report is derived and must not be captured.

The existing snapshot path remains required until Agent supplies and Runtime qualifies that carrier. No `useTimelineOps` edit, new DTO/store/API/authority, native activation, pin/adoption, fallback deletion, or repeat of real26437 was performed.

## Live gesture and classification

The exact live path is:

1. `useRenderState.ts:994-1016` handles `declareSeamsAsHardCuts()` / `acknowledgeVisualCuesAsSynchronized()` and calls the injected `persistVisualSeamConfig` only after the derived report has been revalidated.
2. `useTimelineState.ts:721-741` calls `prepareVisualSeamSnapshotConfig`, which removes the newly derived `report`, preserves an already stored opaque `report`, rebuilds `TimelineData`, and calls `commitData(nextData, { save: true, semantic: true })` followed by the durable save barrier.
3. `useTimelineOps.ts:270` routes only patches classified as supported/mixed to the native generic port. The seam acknowledgement is not currently a TimelinePatch ingress, and the exact attempted `app.update` shape is classified unsupported by the current generic adapter.

Classification:

- `app.visualSeamContract` declarations (`version`, mode, picture/continuity tracks, gaps, intents, participant/context data) are authored film state and need one guarded film edit.
- `visualSeamContract.report` produced by `analyzeVisualSeams` is derived diagnostic state. It must not be copied from the render configuration into the authored command.
- `compiler-canary.ts` project-data source/source-map entries and generated clip metadata are extension-owned derived/catalog data. They are not a carrier for the film seam contract and must remain separate.

## Exact refusal

This is the smallest current Agent-shaped attempt, with the exact live authored leaf represented under `clip.set`:

```python
from astrid.sdk.timeline.commands import CommandError, validate_command

command = {
    "schema_version": 1,
    "op": "clip.set",
    "version": "1",
    "select": "parent/clip:clip-1",
    "args": {
        "values": {
            "app": {
                "visualSeamContract": {
                    "version": 1,
                    "mode": "enforced",
                    "intents": {"120": "hard-cut"},
                },
            },
        },
        "clear": [],
    },
}

validate_command(command)
# CommandError: Additional properties are not allowed ('app' was unexpected)
```

Executed against the current Agent source with the shared App2 Python environment; the refusal was exact. The current pinned registry is:

```text
clip.add, clip.delete, clip.move, clip.set, clip.set-element, clip.set-params,
clip.split, clip.trim, occurrence.add-media, occurrence.delete,
occurrence.duplicate, occurrence.swap-media, placement.create, placement.move,
placement.unplace, producer.guard, shot.pool, shot.set, track.create, track.set
```

`timeline.restore` is an inverse/restore mechanism, not an acceptable seam recipe or row-local capture.

## Smallest Agent request

Provide one closed native film recipe for a single visual-seam acknowledgement batch, or extend an existing recipe only if its literal contract genuinely matches. It must:

1. guard the exact prior `app.visualSeamContract` presence/value and the target timeline identity;
2. write only the authored contract delta, preserving opaque app siblings, raw order, explicit absence, and existing stored report opacity;
3. record stable seam frame/participant/context references and support normal inverse, rebase, retry, and A→B→A guards; and
4. refuse malformed/ambiguous/derived-report-only input atomically.

The request deliberately does not name a speculative operation, add an App DTO, or move compiler-canary/project-data state into film history. Once Agent publishes the closed recipe and the matched Runtime artifacts, App can add the smallest row-local capture/builder and one refusal plus one success test. Until then, the current snapshot fallback is the truthful behavior.

## Evidence

Passed:

```text
./node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/hooks/useTimelineState.visual-seam.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/commands/commitSession.genericPatch.test.ts
=> 4 files, 73 tests passed (83.06s)
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent \
  /home/user/work/venv-app2-native/bin/python -u <literal refusal probe>
=> CommandError: Additional properties are not allowed ('app' was unexpected)
```

Also passed `git diff --check`. No browser, socket, central request-test, full suite, dependency/cache mutation, or real26437 replay was run.

## Exports and callers

Changed exports: none; no product files were changed.

Relevant existing exports and actual live callers, verified with `rg`:

- `prepareVisualSeamSnapshotConfig` — `useTimelineState.ts:728`; three direct focused test callers in `useTimelineState.visual-seam.test.ts:54,74,105`.
- `useTimelineOps` — `useTimelineState.ts:827`; its generic port classification call is `useTimelineOps.ts:270`.
- `persistVisualSeamConfig` — passed from `useTimelineState.ts:749` to `useRenderState`; invoked by `useRenderState.ts:1003`.

