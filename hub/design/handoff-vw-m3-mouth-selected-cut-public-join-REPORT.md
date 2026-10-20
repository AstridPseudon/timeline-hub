# D09a selected-cut public join

## Result

Added a bounded public semantic aggregate to the existing selected-cut query
fixture. It prepares one registered presenter Root, checks component-zero
ownership with the existing `seriesInspection`, then queries exactly the
retained frame keys `[0, 3, 4, 5]` using the ordinary public evaluator. Each
row is checked against the registered presenter's existing `motionAt` and
state codebook. The Python test compares the public states with the existing
ordinary `model.mouth_state` caller and leaves the pixel crop/statistics lane
unchanged.

Added negative controls for changed presenter state, a changed public
codebook, and an omitted selected frame. Existing missing/duplicate/order,
window, missing-image, threshold, and cut-selector controls remain intact.

## Deliberate non-migration

No private helper was deleted or replaced. `render_lipsync` still needs its
private `mouth_box` for pixel statistics and `mouth_state` for the ordinary
visualize panel. More importantly, cached cards have PNG bytes but no retained
public scene rows, and `LayerContext` does not carry final Root props/source
identity/component-zero selection. Migrating that caller would either query
outside the real Root lifetime or downgrade cache fallback behavior. The
exact gap is recorded in the caller map.

The existing `test_live_source_label_native.py` source->exactRoot proof is
separate evidence for the trusted lifetime; this test does not relabel its
retained four-still fixture as a Runtime source certificate.

## Verification

- Python AST parse: PASS.
- `node --check tests/packs/rendering/presenter_selected_cut_query.mjs`: PASS.
- Pure targeted pytest lane: **2 passed** (mouth-state core cycle and cut
  selector refusal).
- The public Composition query tests could not run in this worker because the
  qualified Node 20/composition dependency environment is unavailable here;
  no shared dependencies or caches were modified.
- Full/browser/render/network/install suites were not run.
