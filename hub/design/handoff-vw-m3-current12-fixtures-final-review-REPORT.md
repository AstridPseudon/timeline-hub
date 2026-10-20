# Final review — current12 consumer fixture unit

## Verdict

**APPROVE the narrow fixture/default12 overlay; DEFECT the owner commit as a
whole.**

The approved narrow scope is eight unique test paths: the six f29 consumer
tests plus the two additional presenter files from the approved three-file
companion (the package test is the overlap). It is test-only and leaves the
current `tl/vw-m3-current12-pcm-kernel-cohort` product/kernel, Root, client,
and adoption source unchanged.

Do not merge `5f6c81309d96e7cd7abc2f22b32a377621c29092` wholesale onto staging.
Relative to `082cf265b448712b031730d61cf3b9f63b813ab3`, that commit deletes ten
current inactive-PCM product/test paths and adds a separate 20-path
presenter selected-cut fixture/query cohort. Those are outside this brief and
would delete positive PCM coverage. The narrow eight-path overlay is the
approved handoff; no kernel/root-chain remote request was made.

## Scope and preservation checks

- Staging source: `082cf265b448712b031730d61cf3b9f63b813ab3`.
- Current consumer base: `c456b3281497653cecf44f61acd6fa30565d83c8`.
- Original f29 consumer reference: `f29a9475ee1cb5c13bc1371eee8ff36030dede3e`.
- Owner source inspected: `5f6c81309d96e7cd7abc2f22b32a377621c29092`.
- Approved companion source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-presenter12-pair-test-patch-proposal.patch`.
- `git apply --check --whitespace=error-all` for the companion proposal: PASS.
- Approved eight-path diff: no deletions; `git diff --check`: PASS.
- `presenter_ssr_before.json`: unchanged from the current base; 22 cases and
  all 286 historical hashes remain present.
- The presenter MJS keeps the historical black/Georgia theme explicit and
  separately asserts the full public12 Agent navy default object. No expected
  historical hash was rewritten and no implicit old-fixture override was used
  in the validation run.
- Public12 artifact: 77 regular tar members, SHA-256
  `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.
  Lock metadata names `0.0.12`, the matching file path, and the approved
  SHA-512 integrity string.

## Executable evidence

Tests ran in a disposable overlay archived from staging, with only the eight
approved test paths overlaid from the owner source and a private copy of the
provisioned Remotion peer graph. Shared dependencies and the worktree were not
modified.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$OVERLAY \
ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node \
ASTRID_TEST_NODE_MODULES=$OVERLAY/remotion/node_modules \
ASTRID_COMPOSITION_TEST_NODE_MODULES=$OVERLAY/remotion/node_modules \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
  -m 'not integration' -k 'not admission_travels and not runtime_request and not task_events and not runtime_restart and not render_export_adapter_writes_real_mp4' \
  tests/core/timeline/test_clip_fields.py \
  tests/journeys/test_journey_plumbing.py \
  tests/packs/rendering/test_composition_package.py \
  tests/packs/rendering/test_scene_answers.py \
  tests/packs/rendering/test_scene_host.py
# 231 passed, 9 deselected, exit 0.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$OVERLAY \
ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node \
ASTRID_COMPOSITION_TEST_NODE_MODULES=$OVERLAY/remotion/node_modules \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
  tests/packs/rendering/test_presenter_scene_capability.py \
  tests/packs/rendering/test_presenter_crop_equivalence.py
# 17 passed, exit 0; includes all 286 historical SSR hashes.
```

The first command deliberately excludes six listener-backed journey cases and
one real-MP4 test under the no-socket/no-render worker restriction; those are
not claimed. No browser, socket, install, network, full suite, Runtime pair,
activation, or parity qualification ran.

## Worktree result

No repository patch was created because this is a readonly gate review. The
assigned worktree is clean. The narrow overlay is approved for the owner’s
normal merge path; the whole owner commit remains rejected until its unrelated
selected-cut additions and current-kernel deletions are separated.
