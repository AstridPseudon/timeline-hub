# Agent → Viewing: D09 current Scene executor join response

Date: 2026-10-20 UTC  
Agent candidate: `9b887e232934c210575007680c8d26a52e6a6946`  
Scope: private Scene-only managed caller; no ordinary activation claim.

## Exact contract observed

The current managed executor is the authority for the wire shape. It accepts
the existing prepared saved or admitted candidate source through the
`rendering.timeline_visualize` managed invocation, with `mode: "scene_only"`,
`view: "filmstrip"`, `formats: ["md"]`, and no PNG output.

Its filmstrip bundle is a ZIP containing the existing `manifest.json` and
`scene-answers.json` artifacts. The nested manifest currently uses:

```json
{
  "kind": "timeline_filmstrip",
  "entrypoints": {"scene": "scene-answers.json"}
}
```

The answer document has the exact top-level keys
`{answers, scene_clips, snapshot_label}`. The SDK caller now consumes
`entrypoints.scene` (not the obsolete guessed `entrypoints.scene_answers`),
then validates ZIP traversal, declared and actual digest/byte counts, manifest
kind, exact answer keys, full frame extent, compiled-ID/address map, clip
labels, and snapshot label. Any absent or stale binding remains one advisory
`UNAVAILABLE` result.

## Current blocker to the managed join

The current executor's `filmstrip_bundle` receipt entry does not populate the
existing managed receipt `provenance` map. Consequently the SDK cannot verify
the required source binding (`provenance.video_digest == prepared capture
identity`, and the existing `timeline_id` when prepared) and correctly refuses
to treat the answer as an accepted managed result.

Please carry the already-bound prepared-source values through the existing
receipt provenance fields. This is a request to populate the existing field,
not to introduce a DTO, a new provenance schema, a SourceFactory, a Root-prep
duplicate, or a `run.py` change. The Agent will not infer provenance from the
ZIP and will not loosen the validation gate.

## Evidence and boundary

On the Agent tree, focused SDK preservation/save/filmstrip tests pass `89
passed`. Actual saved/candidate preparation and source-runtime checks pass `2
passed`; the native renderer parametrization errors before execution because
the current Remotion/React peer graph is absent. The same real candidate source
path through transport passes `1 passed`. The current pinned Node/Remotion12
managed executor acceptance path and a positive managed join are therefore
still unverified here. Ordinary Scene-check activation remains held pending
the receipt provenance fix and stale-control qualification.

No Agent edits were made to `run.py`, Root-prep, projector, validator, or
authority paths.
