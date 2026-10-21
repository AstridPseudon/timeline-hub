# Footage scene join review

## Decision

**APPROVE** the 1215 patch for integration.

This review found no request for source changes. The worktree is the exact
1215 commit `5dfa37d28` (`fix(rendering): bind AM-footage scene capability`);
this worker made no product, package, version, pin, registry-authority, or
shared-graph changes.

## Reviewed source and fixture

- `astrid/packs/astrid_motion/rendering/elements/effects/am-footage/scene.ts:19-43`
  already contains the deterministic `prepareFootageScene` capability.
- `astrid/packs/astrid_motion/rendering/elements/effects/am-footage/component.tsx:15,186,319`
  imports that existing capability and attaches it with the same
  `Object.assign(..., {prepareSceneCapability})` seam used by
  `am-snap-plate`, `am-presenter`, and `am-sprite`.
- `scripts/gen_effect_registry.py:591-601` is the normal generated owner
  wrapper: unqualified/default refs return the winner, matching `packId`
  selects the registered owner, and an unknown owner fails closed. Its
  `prepareSceneCapability` forwarding is unchanged. The footage join therefore
  does not activate a caller, source, package, or pin ahead of the qualified
  Composition14 overlay.
- `tests/packs/rendering/test_d09_same_film_public.py:50-72` stages the
  immutable 0.0.14 artifact in a private temporary project, copies the current
  Agent host files, and regenerates the real generated maps. It does not
  bypass the host registration seam.
- The original assertions remain intact:
  - independent legacy fades are `COVERED` through frame 15, `DIP` on
    frames 16..29, and `COVERED` again from frame 30;
  - incoming canonical transition remains `COVERED` for all 60 frames.

## Tests

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_COMPOSITION_TEST_ARTIFACT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.14.tgz ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider -o addopts= --basetemp=/tmp/w-31fe5f6a2e/public14 -m integration tests/packs/rendering/test_d09_same_film_public.py
2 passed in 4.46s
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-31fe5f6a2e/private tests/core/timeline/test_onscreen.py tests/core/timeline/test_onscreen_more.py tests/sdk/test_coverage_empty_cut.py
19 passed in 0.62s
```

Also passed:

- Python AST parse of `tests/packs/rendering/test_d09_same_film_public.py`
- `node --check tests/packs/rendering/d09_same_film_public.mjs`
- `git diff --check`
- source-declared `am-footage` implementation closure exists: shared `am.tsx`,
  `mosaic.tsx`, `component.tsx`, `helper.ts`, `scene.ts`, and
  `element.yaml`.

## Freshness / handoff requirement

`astrid/packs/astrid_motion/pack.yaml` already declares both
`am-footage/component.tsx` and `am-footage/scene.ts`. The tracked
`artifacts.json` digest for `component.tsx` is stale because it records the
pre-1215 source; `scene.ts` is fresh. Agent HOME may run its usual
deterministic metadata/artifact refresh after this source join is integrated.
Do not edit the digest manually or invent a fake hash. This metadata refresh is
a delivery follow-up, not a defect in the reviewed source join.

## Not run / limitation

No browser, full suite, live socket, physical/Gate6, or package installation
was run. A bare-worktree registry-generation probe correctly refused because
the local `remotion/node_modules` does not contain the pinned Composition
package; the required private 0.0.14 overlay generated the real maps and
passed both public tests. The separate snap-plate neighbor lane was not
needed for this two-control review.

Exact temporary pytest directories created for this review were removed.

