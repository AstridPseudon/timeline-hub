# Agent SDK scene-only caller contract reconciliation

Status: implementation-ready handoff; ordinary live executor qualification remains held.

The private caller uses the existing `rendering.timeline_visualize` executor with
`mode: "scene_only"`, `view: "filmstrip"`, `formats: ["md"]`, the existing
`composed_capture`/`include_media` controls, and `every_frames: 1`. It does not
add a DTO, result wrapper, source reference, certificate, provider, store,
endpoint, factory, projector, or query path.

## Exact managed result contract

The result must contain the existing managed output `filmstrip_bundle`. The SDK
reads its digest and size through the existing managed-output row and
`client.media.read_bytes("sha256:<digest>")`, then verifies the ZIP and nested
manifest. The nested `manifest.json` must be `timeline_filmstrip`, declare the
`scene_answers` entrypoint as `scene-answers.json`, and carry an integrity record
for that member. The JSON member has exactly these top-level keys:

```json
{
  "answers": [],
  "scene_clips": {},
  "snapshot_label": {}
}
```

The managed output row must carry `provenance.video_digest` equal to the exact
prepared `capture_identity` and, when the prepared snapshot has a timeline ID,
the same `provenance.timeline_id`. The prepared snapshot's `metadata.capture_identity`,
`metadata.capture_authority`, and `metadata.scene_clips` are checked before any
answer is formatted. The returned `scene_clips` map must equal that prepared map;
each layer `clipId` must be a key in it. The returned `snapshot_label` must be
the exact committed or candidate label derived from the prepared source. Missing,
stale, forged, `uncertified`, or `unavailable` labels never produce canonical
Scene coverage. Answers must be ordered and complete for every frame in
`range(duration_frames)`.

Missing/stale/malformed custody, source, label, map, layer, or frame binding
returns one advisory `UNAVAILABLE` span. It does not alter save, transaction,
publish, saveNoNode, OFFCANVAS, or core-valid behavior. No D09 deletion or
pixel/audio parity claim is made by this handoff.

## Implemented tree evidence

- `astrid/sdk/timeline_filmstrip.py`: `a5a3e87821f2170435bca9244cbb7da0541aeca42ca2120a5b0cadc645d352fd`
- `tests/sdk/test_scene_caller_preservation.py`: `7fcfb26b972058a46a9a5a6e879319dfd7890a05073346624180721e7e82698a`

Focused Agent lane: 89 passed. The 87 prior semantic/save assertions remain
green, with one missing-managed-source negative and one candidate-label positive
added. Ordinary live executor/Node qualification was not run here.
