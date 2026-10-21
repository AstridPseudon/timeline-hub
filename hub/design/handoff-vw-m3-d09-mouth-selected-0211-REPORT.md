# D09 current-source packet

The existing presenter source/query seam already supplies the required public
facts; this worker only retargeted its registered-host qualification from
public12 to current immutable public13. Public13 artifact SHA-256 is
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` (77
members). Source tree checked: `4467c1c1a`.

The public Node query uses the ordinary generated host maps and registered
`pack:astrid_motion` presenter. It uses the shared source `mouthAnchor`,
`mouthStateRect`, `pixelGeometry`, `presenterAt`, and `motionAt`/static
`closed|half|open` codebook. It does not copy Python timing or geometry and
does not use private `mouth_state`/`mouth_box` to produce public rows.

Existing active tests now run against public13: `test_presenter_public_scene_contract`
(states, geometry, unknowns, clock, registration), registered SSR/declarations,
`test_series_inspection_retains_one_component_zero_query`, all six
`test_presenter_crop_equivalence` behaviors (including default/partial/raw-invalid
known diagnostics), and the selected-cut aggregate/fallback/identity/window/
threshold controls. Targeted result: **41 passed in 14.25s**. Public13 package
integrity/admission controls: **5 passed in 0.21s**.

This closes only the source prerequisite. `model.mouth_state` (builtin.py:473)
and `model.mouth_box` (builtin.py:512) remain live in `render_lipsync`, with
the private crop/statistics and fallback intentionally retained. The sole
remaining physical prerequisite is a fresh current-public13 registered-root
renderStill/PNG lane that retains component-zero public ROI for the selected
series and proves the unchanged aggregate plus planted mismatch. Prior physical
evidence is not relabelled as current-public13 proof; default/partial/raw-invalid
legacy equivalence remains unqualified.

Node syntax checks, Ruff, and `git diff --check` also pass. The first local
pytest invocation lacked the explicit public13 runtime project needed by
registry discovery (3 passed, 38 setup errors); the recorded 41-pass rerun
supplied that read-only project and made no shared writes.
