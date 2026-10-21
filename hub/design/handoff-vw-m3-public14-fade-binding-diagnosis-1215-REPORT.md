# Public14 fade binding diagnosis

## Result

This was a product join defect, not a wrong fixture/import. The current Agent
source had the reviewed `prepareFootageScene` implementation in
`astrid/packs/astrid_motion/rendering/elements/effects/am-footage/scene.ts:19-43`,
but `component.tsx` did not attach it to the component. Before this patch the
component was still a plain default function; therefore the real host's
generated owner wrapper forwarded no scene capability and Composition correctly
returned `UNKNOWN` for both public14 cases.

The existing registration seam is in
`scripts/gen_effect_registry.py:591-600`: the generated owner wrapper selects
the effect component and forwards its `prepareSceneCapability` property. The
same seam is used by `am-snap-plate/component.tsx:21,156` and
`am-presenter/component.tsx:23,293`. The public14 fixture copied the current
`host-scene.ts` and `host-registries.ts` and regenerated those maps at
`tests/packs/rendering/test_d09_same_film_public.py:65-72`; it was exercising
the real host path, not bypassing registration.

The patch is limited to `am-footage/component.tsx`:

- import the existing `prepareFootageScene` export;
- export the existing component through
  `Object.assign(AmFootage, {prepareSceneCapability: prepareFootageScene})`.

No renderer, coverage/math, factory, API, type, registry authority, package
pin, lockfile, or activation was changed. The original two public14 assertions
remain unchanged. The private fade source and its 19 positive assertions are
preserved.

## Evidence

Passed after the patch:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_COMPOSITION_TEST_ARTIFACT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.14.tgz ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider -o addopts= --basetemp=/tmp/vw-m3-public14-fade-binding-diagnosis-1215-public14 -m integration tests/packs/rendering/test_d09_same_film_public.py
2 passed in 4.46s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider tests/core/timeline/test_onscreen.py tests/core/timeline/test_onscreen_more.py tests/sdk/test_coverage_empty_cut.py
19 passed in 0.62s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m py_compile tests/packs/rendering/test_d09_same_film_public.py
/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node --check tests/packs/rendering/d09_same_film_public.mjs
git diff --check
all passed
```

The neighboring `test_am_snap_plate_scene_capability.py` was attempted with
the read-only peer graph, but remains blocked in this worktree because its
fixture expects a pinned Composition package at
`remotion/node_modules/@banodoco/timeline-composition/package.json`. No install
or shared write was performed. No full, browser, socket, physical, or Gate6
run was performed.

## Recommended next step

Have the viewing owner review/merge this one-line capability join, then rerun
the same public14 targeted lane on the pinned integration package. Keep
activation and any package pin changes separate from this source fix.
