# Default-mouth case map

| Concern | Committed source | Guard/evidence |
| --- | --- | --- |
| Normal default constructor | `tests/packs/rendering/presenter_crop_geometry.mjs:27-38` | `defaultParams` has no `mouth`; `defaultPropsFor()` goes through existing `propsFor` |
| Same registered drawing and public frame-0 ROI | `tests/packs/rendering/presenter_crop_capture.mjs:14-35` | `default` mode uses existing `prepareRoot` and `seriesInspection`; no copied geometry |
| Private/public comparison | `tests/packs/rendering/presenter_crop_capture.py:127-184` | Existing `model.mouth_box`, `png_crop`, `public_box`, `_diff_fraction`; no new statistic/threshold |
| Exact selected cut | existing `context`/`cut_ref` in `test_presenter_selected_cut_aggregate.py` | existing explicit case remains untouched; default helper keeps frames `[0,3,4,5]` |
| Physical executor | `handoff-vw-m3-default-mouth-physical-case-prep-0251-run.sh` | package13/9412, Node43d6, Chromium1194 path+hash, peers, source, flock, one test node |
| Named suite | `scratchpad/orch/tests/suites.conf` | `e2e-viewing-mouth-default-physical-case-prep-0251` |

## Source mismatch

For raw default params with no `mouth`, the registered public presenter returns
a known frame-0 ROI `(894,606,1032,654)` while the existing private
`model.mouth_box` returns `None`. The prepared physical test stops on this
fact, so no default crop equivalence or D09 closure is claimed. The smallest
next correction is component-owned compatibility for the omitted-mouth
constructor at the existing private consumer seam, preserving partial/raw-
invalid fallback and all explicit assertions.
