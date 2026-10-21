# VW-D09b/c partial presenter crop source

## Result

Prepared one future partial-input case on the retained real registered-presenter
four-still fixture. The existing explicit-anchor positive remains the default
capture mode and keeps its 799-pixel private/public equivalence and controls.
The new `partial` mode uses only raw `mouth: {x: 151, y: 104}` and captures the
same frames `[0, 3, 4, 5]` through the same registered component, prepared Root,
component-zero query, renderer entrypoint, package, browser and cleanup path.

The future partial assertions compare private `(298, 202, 339, 219)` (697 px)
with the existing public compatibility crop `(298, 202, 345, 219)` (799 px),
using the public crop's private-width subset for actual pixel equality. The
erase control remains `(300, 206, 343, 215)` (387 px). Natural transitions,
the unchanged strict `> .02` comparator, 8/15/16/20 planted controls, padding
control, PNG byte preservation, frame zero, and source/graph cleanup guards are
retained. No default pixel positive, raw-invalid fallback, statistic, product
code, DTO, public type, caller, pin, or version change was made.

## Files

- `tests/packs/rendering/presenter_crop_capture.mjs`: one private `partial`
  mode in the existing four-still capture source; explicit remains default.
- `tests/packs/rendering/presenter_crop_capture.py`: retained explicit test,
  shared capture/cleanup helper, and one unrun partial physical test.
- `tests/packs/rendering/presenter_crop_entry.mjs`: existing fixture entrypoint
  restored with the ordinary registered host map.
- `tests/packs/rendering/test_presenter_crop_equivalence.py`: pure expected
  partial 697/799/387 geometry and threshold controls.

Live callers changed: none.

## Verification

Pinned read-only inputs:

- Node: `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`,
  version `v20.19.4`, SHA-256
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
- Composition public13 artifact SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Qualified read-only peer graph:
  `/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules`.

Passed:

- Pure geometry/control lane: `10 passed in 4.41s`.
- Node `--check` on geometry, entrypoint and capture source: passed.
- Fixture collection: `2 tests collected in 0.21s`; neither physical test ran.
- `ruff check --no-cache` on the touched Python sources: passed.
- `git diff --check`: passed.
- Readback SHA-256:
  - `test_presenter_crop_equivalence.py`:
    `2419620a92c9972c1a7e4bd5a3b79790631ced2661227cc9420b6977946957b1`
  - `presenter_crop_capture.py`:
    `68291e26500154b0ac2531a0b69558c5ef64d02aac10b8261f8329e036b87016`
  - `presenter_crop_capture.mjs`:
    `38abb1a8854a97473f01dd2886bf805945200f9cc45bd6c61d2e17233c2be49f`
  - `presenter_crop_entry.mjs`:
    `5223ef4ecf007124920773bef10a9f543749cd07c943e5143720837f18e29947`
  - retained `presenter_crop_geometry.mjs`:
    `3b63d3ad5d9c14296092c1263811a425b91b1d3de60ffe39df9931967cbfa14a`

Not run by design: browser, renderStill, socket, central service, physical
qualification, full suite, install, Runtime, or any runner retry. The partial
physical variant remains NOT RUN and needs normal source/tuple/custody
qualification after the main Gate 6 environment is fixed. The exact 0244
original four-still physical result remains explicit-only; its PNGs were not
relabelled as partial.

## Initial environment note

An initial pure invocation omitted the qualified `ASTRID_REMOTION_PROJECT_DIR`
and stopped during fixture setup because the registry verifier could not find
the public package. No source or shared dependency was changed. The rerun with
the qualified read-only public13 runtime above passed.
