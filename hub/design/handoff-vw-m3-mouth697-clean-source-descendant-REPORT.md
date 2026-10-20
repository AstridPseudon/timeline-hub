# Corrected 697px partial-mouth clean-descendant handoff

## Result

Applied the independently approved physical-test patch to a worktree based
on Agent `ee71010a0947edcbbacbf8178e5fee11ab6bab3d`. The patch adds only the
direct presenter crop fixtures and the central two-frame physical test. The
existing explicit-width 799/387 four-still controls are unchanged. The new
case remains raw `mouth: {x: 151, y: 104}` with omitted width, frames `[0, 3]`,
crop `(298, 202, 339, 219)`, area 697, and a 20-pixel negative using the
strict `>2%` comparator. Default and malformed inputs remain no-inspection /
unknown source-only cases.

Published corrected flat artifacts:

- controller SHA256:
  `005b01bc3ed95a7da5ee5f6e5035fda27db30d66357d90ee5eafd38c813a84fb`
- manifest SHA256:
  `8d3d3d2842b88516725a799ea5a8a10f4c178f86ffaf205857769686eea9694a`
- patch SHA256:
  `9624922e36ff9668d2458704368a16ea87d4e82551959e46d9e0b197ca122d5c`

The corrected controller uses only the retained current-root worker Node path
and verifies its exact SHA256, v20.19.4 version, full f816 graph, six peer
hashes, Chrome155 tree, immutable public12 archive, source hashes, manifest
hash, patch hash, and controller/tool bytes. It validates the clean source
before creating `RUN_STARTED`; after the harness completes, all source,
dependency, browser, and tool bytes must still match before it writes
`POSTFLIGHT_OK` containing the final exact source SHA.

No `READY_GRANTED`, `REVIEW.md`, browser grant, render, socket, network,
install, full suite, or stale-root artifact regeneration was performed.
The central physical 697px result remains unverified. If normal renderer
admission requires root artifact regeneration, the controller must refuse and
wait for the owner rather than bypassing that requirement.

## Validation

- `git apply --whitespace=error-all <approved patch>` — PASS.
- `git diff --check` — PASS.
- Retained Node `--check` on all three new `.mjs` files — PASS.
- Python `py_compile` on both new Python tests and the corrected controller — PASS.
- `python3 -m json.tool` on the corrected manifest — PASS.
- `PYTHONPATH=$PWD ASTRID_NODE_EXECUTABLE=<retained Node> ASTRID_COMPOSITION_TEST_ARTIFACT=<public12> ASTRID_COMPOSITION_TEST_NODE_MODULES=<f816 peers> /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/vw-m3-mouth697-targeted-pytest tests/packs/rendering/test_presenter_crop_equivalence.py tests/packs/rendering/test_presenter_scene_capability.py` — **17 passed**.
- `PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/packs/rendering/test_presenter_crop_partial_physical.py` — **1 collected**.

The current worktree is intentionally uncommitted because the harness owns
the commit. The manager must use the resulting clean harness HEAD as
`VIEWING_CROP_REVISION` and write the fresh grant inputs separately.
