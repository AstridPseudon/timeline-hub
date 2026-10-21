# AG05 — Viewing consumer ACK

## Verdict

**ACK / confirmed for the exact scope.** Removing only the outer read-row
`created_at` fields and the duplicated outer parent
`dependency_manifest` from `expansion.graph` cannot affect the current Viewing
viewer, host, or check semantics. This does not authorize removing any
`payload.created_at`, authored payload field, root manifest, ID, digest, pin,
order, or opaque value.

## Current consumer evidence

- The current graph path injects `row.composition_graph` into the visual config
  at `astrid/packs/rendering/actions/timeline_visualize/run.py:406-411`.
  `astrid/core/timeline/snapshot.py:269-284` accepts that graph only to run
  `project_shot_composition`; the projection reads parent payload/config,
  occurrences, shot/internal revision IDs, payloads, clips, tracks, registries,
  assets, timing and placement (`astrid/core/timeline/shot_composition_projection.py:472-497,511-675`).
  It does not read outer row `created_at` or the duplicated outer parent
  manifest.
- The text/visual model consumes projected authored occurrence data and clip
  timing/identity (`astrid/packs/rendering/actions/timeline_visualize/model.py:377-420`),
  not those excluded graph decorations. `select.py:325-350` does read a
  timeline listing's `created_at` fallback for `head_created_at`; that is the
  listing/head timestamp, not `expansion.graph` row decoration.
- Host/capture paths carry the complete expansion into authority
  (`astrid/packs/rendering/actions/render/managed_timeline.py:713-739`;
  `astrid/sdk/timeline_filmstrip.py:344-364`) and bind the complete recorded
  authority in the capture identity (`astrid/sdk/timeline_filmstrip.py:870-888`;
  `astrid/packs/rendering/actions/timeline_visualize/composed_frame.py:710-718`).
  `astrid/core/rendering/verified_source.py:63-71` likewise compares the
  recorded capture authority as a whole. These are identity/byte-preservation
  checks, not field-level consumers; do not compare hashes after stripping.
- Candidate preview does read `publication["dependency_manifest"]` at
  `astrid/sdk/authoring_render_preview.py:50-71` and `:119-164`, but that is
  the authored publication manifest used to resolve pinned children, outside
  `expansion.graph`, and must remain untouched.

## Historical compatibility and evidence

Recorded snapshots/CAS/source bindings must remain byte-identical and verify in
their recorded form. If an old record cannot be verified after the new shape is
introduced, it must remain explicitly legacy `UNCERTIFIED`; it must not be
renormalized or silently recertified. This is the prior 02:42/02:59 decision
and the existing `viewing-capture-envelope-confirmation.md` boundary.

Prior recorded evidence (not rerun here): the Agent projection lane reported
304 focused passes and the exact saved/authored-field plus six candidate
goldens reported 8 passes with `--runxfail`; the prior Viewing audit reported
no semantic viewer/host/check dependency. Current source inspection also finds
the existing regression assertions in
`tests/sdk/test_timeline_capture_projection.py:312-337` preserving payloads,
manifests, order, pins, and authored nested fields while requiring the excluded
outer fields to be absent.

## Tests and limits

No tests, browser/helper/Runtime/renderer/socket/central/full qualification,
install, or product/schema/projection change was performed. This was the
requested source-only ACK; the prior qualification evidence was not retried.

