# D09 core on-screen behavior map report

## Result

`MAP.md` maps all 14 tests currently present in the two requested legacy files
to named current-source public Scene/evaluator tests and records each missing
assertion. No legacy test, SDK code, evaluator code, Root code, or caller was
changed. No retirement or `UNKNOWN` substitution was performed.

The map finds no complete one-to-one public replacement for all old assertions.
That is expected input for a later deletion review, not a green deletion gate.
In particular, live private assertions for layer opacity/order, declared
geometry, `none` omission, audio filtering, YAML fallback, boundary call count,
and entrance behavior remain explicitly unresolved.

## Settled coverage decisions reused

- The approved MAIN6-vs-unified pixel proof is treated as settled evidence for
  the intentional difference: independently authored overlapping element fades
  are DIP during the overlap in the unified viewer. It does not certify the old
  private `COVERED` assertion.
- The incoming-transition `COVERED` positive is kept separately. The approved
  real-AM evidence names `test_actual_am_public_incoming_crossfade_stays_covered`;
  the current-source compiled-transition analogue is
  `tests/packs/rendering/test_scene_host.py::test_native_host_passes_public12_compiled_transitions_unchanged`.
  These are not interchangeable with the old two-independent-fades case.
- The approved real-AM one-sided fade evidence and current-source
  `test_real_plate_fade_dip_and_translucent_gap` cover per-frame DIP then
  COVERED, but not the old private continuous-span/RLE shape.

The approved pixel report was inspected at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/escalations/closed/viewing-20261020T0436Z-main6-intended-dip-pixels-pass.md`

The prior coverage-positive report was inspected at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-coverage-positive-equivalents/report.md`

Those reports are evidence references only; this worker did not copy or modify
their artifacts, and the named AM-positive test is not present in this current
checkout.

## Test evidence

All commands used the exact required Node executable:
`/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`.

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
/home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= \
-p no:cacheprovider tests/core/timeline/test_onscreen.py \
tests/core/timeline/test_onscreen_more.py
14 passed in 0.23s
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
/home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= \
-p no:cacheprovider tests/packs/rendering/test_scene_answers.py
30 passed in 2.68s
```

The attempted combined current-source public/native-AM lane was not a valid
qualification run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
ASTRID_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules \
/home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= \
-p no:cacheprovider tests/packs/rendering/test_scene_answers.py \
tests/packs/rendering/test_scene_host.py \
tests/packs/rendering/test_am_snap_plate_scene_capability.py
```

It produced **30 passed, 29 setup errors**. The native fixtures could see the
read-only peer directory when `ASTRID_TEST_NODE_MODULES` was supplied, but the
current generator still resolved the Composition package from this worktree's
default `remotion/node_modules`, where `@banodoco/timeline-composition` is not
installed. No shared dependency was changed and no behavioral result is claimed
for those 29 setup errors. Existing approved real-AM evidence is therefore
reused as documented above rather than relabelled as a fresh run here.

Not run: full suite, browser/localhost/socket tests, actual render or pixel
capture, audio parity, package install/build, or any deletion candidate.

`git diff --check` passed. The supplied prior-research directory
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/luna/reports/`
was absent in this environment; the two available ORCH evidence reports are
named above instead.

## Decisions and next steps

No new public-query test was added. The current public query already covers the
supported per-frame and real-AM subsets; the unresolved cases require either
package-owned crop/entrance/audio/none capability or private caller/source
joining. Adding a synthetic test for one of those would create a false
replacement rather than qualify retirement.

Next review should use this map to select the exact remaining owner work before
any module or test deletion. In particular, do not delete the private tests or
replace their expectations with refusal/`UNKNOWN` until each MISSING assertion
has a real public test on the same source/caller path.
