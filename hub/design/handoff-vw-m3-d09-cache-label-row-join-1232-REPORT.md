# D09 cached-label source-row join — handoff

Agent branch `tl/vw-m3-d09-cache-label-row-join-1232`, based on
`tl/vw-m3-d09-label-existing-row-carry-1226`.

The remaining private semantic fallback at
`astrid/packs/rendering/actions/timeline_visualize/_filmstrip_cache.py:20-22`
is retired. When `scene_for_frame(frame)` returns an already-admitted public
row, the helper continues to validate and format it through the existing
`_labels_for_scene_facts`/`labels_for_scene` path. When no row exists, the PNG
remains usable as image evidence but semantic `addresses` is `null`; no
timeline visibility evaluator or invented source is consulted.

The direct tests preserve the exact public-row positive and cache controls,
including exact-key/source/basis/address/PNG/frame checks and stale/forged
MISS behavior. A minimal execution provider test has no source-row carrier;
its original positive assertion is retained as a strict xfail. The exact
caller contract needed to turn that xfail green is the existing
`scene_for_frame(frame) -> CaptureSceneLabels | None` method with the
provider's `source_identity`, returning only an exact frame/basis/address-map
bound row.

Evidence: 96 scoped transport/source tests passed with 19 native cases
deselected; the nearby execution selection passed 1 case and produced 4
strict expected failures for the carrierless test double; scoped Ruff and
`git diff --check` passed. Full/native/browser/live-socket/install suites were
not run. The patch is in the adjacent `.patch` handoff artifact.
