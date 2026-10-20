# ORCHREPORT — vw-m3-presenter12-qualification

## Result

APPROVE qualification evidence for presenter port `802669926` against the
immutable Composition 0.0.12 artifact. No production files, presenter callers,
crop/statistics code, SDK code, or repository fixtures were changed in this
worker worktree; `git status --porcelain` is empty.

The exact 802 presenter source was staged into this ORCH-owned offline fixture:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/presenter12-fixture.51i7Ur`

The fixture uses the existing source/test contract, with only its offline
artifact identity/path changed from public10 to public12. The public12 archive
is the existing Git object from Agent consumer commit `f29a9475e`, not a new
archive or release:

- SHA-256: `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`
- archive contents: 77 files
- lock version/resolved: `0.0.12`, `file:artifacts/banodoco-timeline-composition-0.0.12.tgz`
- lock integrity: `sha512-490yQtC4k3cuBQJ4Aee5qEqOPNrlQrXPQkE0p6R8UDACAcT8amHe8EjCRI4vE+HtvXwUiy8zBjm7RcW7aTv9eA==`

## Evidence

From the fixture directory, with Node `20.19.4`, the known read-only peer
graph at `/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules`,
and the shared Agent venv:

```text
Q=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/presenter12-fixture.51i7Ur
cd "$Q"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$Q" \
ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node \
ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
tests/packs/rendering/test_presenter_scene_capability.py \
tests/packs/rendering/test_presenter_crop_equivalence.py \
--basetemp=/tmp/vw-m3-presenter12-qualification-pytest-final2
```

Result: **17 passed in 9.71s**.

This includes:

- registered capability states, preparation, geometry, clock and owner
  dispatch;
- the historical SSR fixture: **22 cases / 286 hashes**, all preserved;
- public12 declarations through ordinary `node_modules` resolution;
- 77-file archive hash preservation and six known peer path/version checks;
- source closure and explicit owner/resource checks;
- default, partial and malformed-anchor KNOWN geometry;
- legacy-unqualified crop distinction and mosaic/unsupported-outer UNKNOWN;
- crop geometry and the retained 2% counterexample.

The fixture also asserts Composition 0.0.12's `DEFAULT_THEME` is the Agent
navy value (`#050814` background, `#FAFAFA` foreground, `#67E8F9` accent,
Arial, 450ms). Historical SSR cases use an explicit pre-12 theme so the 286
hashes remain a true preservation check rather than silently adopting the new
package default. Explicit fixture inputs remain explicit.

Independent immutable-package/readiness check, using the exact 0.0.12
consumer package/lock and runtime expectation in the same offline fixture:

```text
Q=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/presenter12-fixture.51i7Ur
cd "$Q"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$Q" \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
-m 'not integration' tests/packs/rendering/test_composition_package.py \
--basetemp=/tmp/vw-m3-presenter12-package-pytest-rerun
```

Result: **5 passed, 1 deselected in 0.23s**. This covers lock identity,
artifact hash, built export targets, refusal of incomplete/unsafe exports, and
runtime package readiness without install or network.

Additional checks:

```text
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/presenter12-fixture.51i7Ur/tests/packs/rendering/presenter_scene_capability.mjs PASS
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/presenter12-fixture.51i7Ur/tests/packs/rendering/presenter_crop_geometry.mjs PASS
/home/user/work/venv-agent/bin/python -m ruff check --no-cache --isolated --select E4,E7,E9,F,I,BLE /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/presenter12-fixture.51i7Ur/tests/packs/rendering/test_presenter_scene_capability.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/presenter12-fixture.51i7Ur/tests/packs/rendering/test_presenter_crop_equivalence.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/presenter12-fixture.51i7Ur/tests/packs/rendering/test_composition_package.py PASS
git -C /home/user/work/wt/vw-m3-presenter12-qualification diff --check PASS
test -z "$(git -C /home/user/work/wt/vw-m3-presenter12-qualification status --porcelain)" PASS
```

All five presenter production files in the staged fixture have SHA-256 bytes
identical to the corresponding files at `802669926` (including `scene.ts`);
no production fix was necessary.

## Decision / limits

The first public12 run correctly exposed one failure: the old SSR hashes were
implicitly rendered with public10's black/Georgia default, while public12's
default is the required Agent navy theme. I did not weaken or rewrite the
286 expectations. I made the offline fixture's historical theme explicit and
added the exact navy-default assertion; the final run passed all 17 tests.

No browser, full suite, live socket, renderer/export, install, network,
callback/source grant, or SDK change was run. No new archive/release was
created. The source/capture consumer join and any later private crop migration
remain outside this qualification.

## Recommended next step

Land the current presenter port and the already-qualified Agent 0.0.12
consumer through the normal manager merge path, carrying this fixture-only
theme/default distinction into the combined qualification review.
