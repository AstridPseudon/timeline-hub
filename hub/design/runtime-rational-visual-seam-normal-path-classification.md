# Runtime rational FPS visual-seam normal-path classification

Date: 2026-10-21 UTC

## Verdict

This is a **genuine normal render-admission defect**, not a save-path defect.
The supported Agent provider preserves `parent_composition.config` verbatim in
the committed `canonical_document`; Runtime stores that payload losslessly.
Runtime's normal managed render admission then loads that exact parent closure
and invokes `admit_closure(..., materialize=True)`. Before this correction,
`visual_seam.normalize_closure()` passed authored `output.fps` directly to
`finite()`, so valid raw mapping/list rational FPS raised
`ValidationError("visual timing fps must be finite and positive")` before the
render projection was materialized. The post-`fc7979e` advisory behavior does
not make malformed seam input advisory: timing validation still raises.

The repair is bounded to the existing seam conversion boundary. Rational FPS
is parsed through Runtime's existing bounded `_fraction` helper, converted
only to the local seam clock, and never written back to the authored payload.
No compiled schema, commit API, DTO, store, read normalization, timing
compiler, or renderer path changed.

## Exact source trace

- Agent normal provider: `/home/user/work/agent/astrid/sdk/timeline/commit.py:244`
  builds `parent = copy.deepcopy(publication["parent_composition"])`; the
  publication's `final_parent` is copied from the authored parent payload at
  `astrid/core/timeline/authoring_bundle.py:1057-1059`.
- Runtime normal commit acceptance validates and persists that exact
  `canonical_document` through
  `runtime_protocol/timeline_commit_store.py:555-590, 860-905`; no visual seam
  call occurs on `/v1` commit acceptance.
- Normal render admission loads the persisted pinned closure and calls
  `admit_closure(..., materialize=True)` at
  `runtime_protocol/store.py:1982`. Its `seam_metadata["render_config"]`
  becomes the frozen render source at `store.py:2039-2041`.
- The old rejection was `runtime_protocol/visual_seam.py:141-143`, where
  scalar-only `finite()` rejected both `{"numerator": 30000,
  "denominator": 1001}` and `[30000, 1001]`.
- Agent's optional capture projection is a separate supported caller:
  `RuntimeCommitService.project_capture()` at
  `/home/user/work/agent/astrid/sdk/timeline/commit.py:663-766`. It projects
  the closure for capture parity and does not call Runtime visual seam; it is
  not the source of the render-admission rejection.

## Source changes

- `runtime_protocol/timeline_inspection.py`: extend the existing bounded
  `_fraction` parser to accept the raw mapping spelling alongside its existing
  list/tuple spelling.
- `runtime_protocol/visual_seam.py`: use that helper only for local FPS
  evaluation when the authored value is a mapping/list. Scalar `int`/`float`
  behavior remains through `finite()`. Bool, zero, negative, malformed,
  denominator-zero, and nonfinite values still refuse.
- `tests/test_visual_seam_admission.py`: add the two rational wire forms, assert
  the materialized authored FPS remains unchanged, and cover invalid FPS
  refusals. Existing strict timing tests were not changed.

## Evidence

Final targeted commands on the changed tree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_visual_seam_admission.py::test_render_materialization_still_rejects_invalid_timing tests/test_visual_seam_admission.py::test_render_materialization_accepts_raw_rational_fps tests/test_visual_seam_admission.py::test_render_materialization_rejects_invalid_fps tests/test_direct_render_admission.py::test_direct_managed_render_admission_freezes_snapshot_before_claim tests/test_timeline_native_inspection.py::test_generic_fraction_still_rejects_null
14 passed in 1.07s

git diff --check
passed
```

An earlier exploratory targeted command also included the existing
`test_fractional_occurrence_bounds_match_render_frames_and_preserve_real_gaps`
neighbor and returned `17 passed`; that command unintentionally reran a
previously passing rational-admission neighbor despite the no-replay
instruction. No renderer, browser, live-socket, full, or full-conformance
suite was run.

## Merge condition

Runtime source is bounded and tested. Because this changes a normal Runtime
render-admission consumer, an independent Main-infrastructure preservation
review is required before merge. Agent has no Runtime carrier gap to fix; its
raw authored carrier is the reason the Runtime seam conversion is needed.
