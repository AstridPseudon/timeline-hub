# Agent U2b independent final review — FAIL

## Verdict

**FAIL. The U2b return fixes the four findings from review 1019, but the exact
candidate remains merge-blocked by four mandatory inventory-test failures that
were exposed by the upstream no-invisible-skips merge.** This is not a new
product-source regression created by return `6c3d92645`; it is a merge-result
coverage regression that must be resolved by the author/orchestrator before
approval. No retired document was restored and no assertion was relaxed here.

Reviewed exact candidate:

- `6c3d9264564bd533995e35c2b8f1f44bb1161cf6`
- parent/return base: `55c1e7aa782239ce8001ea0b6cf7d2795c6d1c89`
- merge base for the cumulative review: `ef851b22c506245441b9a630c093b3460e39cbdc`
- upstream parent: `74f3f7edba35230d0a01824eae7b663143e6aa5b`
- `git merge-base --is-ancestor 74f3f7ed... HEAD`: **pass**

## Return scope and conflict audit

`git diff --name-status 55c1e7aa7..6c3d92645` contains exactly the seven
expected return paths:

- delete the three accidentally tracked `.pyc` files;
- delete `tests/packs/rendering/test_timeline_inspector_viewer.py`;
- remove EOF whitespace in `tests/packs/runpod/conftest.py` and
  `tests/test_runtime_correctness_inventory.py`;
- port the stale publication test in
  `tests/packs/video_editing/test_runtime_publication_chain.py`.

The cumulative tree has no tracked `.pyc`/`__pycache__` files, no new binary
diffs, and no product-source deletions. The dead-inspector decision is
source-backed: at `ef851`, the inspector product and test were both absent;
the upstream `74f3` side reintroduced both; merge `55c1` retained the upstream
test while preserving the parent product deletion. The return deletes that
orphan test, preserving the approved dead-inspector cut without a skip or
xfail.

The cumulative changed paths are limited to CI/config/docs/tests (plus the
rename-tool test); protected schema/client/lock/Composition package paths are
byte-identical to `ef851`. `git diff --check ef851..HEAD` passes.

## Lane policy review

The exact requested focused policy suite passed:

```
/home/user/work/venv-agent-child-f1012-installed/venv/bin/python -m pytest -q \
  tests/test_lanes.py tests/test_lane_registry.py tests/test_skip_policy.py \
  tests/test_skip_guard.py
```

Result: **55 passed**. This covers exact marker/node attribution, lane and
reason custody, strict reason matching, copied-reason and unregistered-node
negatives, zero-pass failure, module import suppression, and deselection/
`--deselect` negative controls. The registry/CI/default-off consistency checks
also pass.

Rendering collection also passes and the deleted inspector test is absent:

```
/home/user/work/venv-agent-child-f1012-installed/venv/bin/python -m pytest \
  --collect-only -q tests/packs/rendering
```

Result: **1510/1551 collected, 41 deselected by lane**.

## Publication test port review

The changed target passes:

```
/home/user/work/venv-agent-child-f1012-installed/venv/bin/python -m pytest -q \
  tests/packs/video_editing/test_runtime_publication_chain.py \
  -k 'requester_commit_publishes or legacy_assembler_admission'
```

Result: **2 passed, 11 deselected**.

The port is semantically appropriate for the retired host route. The current
production path is `publish_stitched_render` →
`publish_authoring_proposal` (`astrid/packs/rendering/shared/runtime_stitch.py`),
not `GenericPackHost._publish_assembled_timeline`, which no longer exists.
The surviving caller requires the original requester session/client/timeline,
checks the admitted project/timeline scope, checks producer `attempt_id`,
`fence`, and `runtime_epoch`, sends one requester commit, then admits exactly
one ordinary `rendering.render` task at the accepted revision with
`idempotency_key + ':render'`.

The replacement test asserts one commit call, admitted project/timeline and
base revision/publication, producer attempt/fence binding, one rendering task,
and no `save`/`invoke` traffic. The neighboring requester tests retain the
full v2 envelope, label/merge/reads/source/steps, receipt, render capability,
render idempotency, lost-ack replay, refusal details, dry-run, peer-head replay,
and mutable-producer non-reread coverage. The old host lease-token assertion
is not semantically portable: the surviving requester caller has no host lease
token and intentionally owns publication through the requester commit. No
fake executor, blanket refusal, or weakened expectation was introduced.

## Inventory failure and causality

The required targeted command is red:

```
/home/user/work/venv-agent-child-f1012-installed/venv/bin/python -m pytest -q \
  tests/test_runtime_correctness_inventory.py tests/packs/runpod/test_worker_process.py \
  -m 'not integration'
```

Result: **44 passed, 4 failed**. All four failures are
`tests/test_runtime_correctness_inventory.py` and fail at line 22 because
`docs/runtime-correctness-m3-inventory.md` is absent. The RunPod neighbors
pass.

This is not “preexisting” in the sense of a harmless inherited failing
assertion. Exact blob causality is:

1. parent `ef851` retained the inventory test, but `_inventory_text()` used
   `pytest.skip` when the document was absent, so the parent did not fail;
2. the document was legitimately retired by `d90c6818b` and is absent from
   both `ef851` and upstream `74f3`;
3. upstream’s no-invisible-skips commit `f9e58fbdb` deleted the stale inventory
   test, but the merge result `55c1` kept the parent test and changed its
   missing-document behavior from skip to fail;
4. return `6c3d92645` only removes EOF whitespace from that test and does not
   cause or conceal the failure.

Therefore this is a mandatory merge-result coverage failure, not a reason to
restore the retired document or turn the assertion back into a skip. The
author/orchestrator must either remove/port the legitimately retired test into
current source-backed coverage, with the policy decision recorded, or otherwise
resolve the merge conflict. Until then, this candidate is blocked and cannot
receive a PASS.

## Static and protected-artifact evidence

Passed:

- `make PY=/home/user/work/venv-agent/bin/python ruff` — **2149/2149**.
- `MYPY_CACHE_DIR=/tmp/.../workers/agt-U2b-final-review-1034/tmpdir/mypy-cache make PY=/home/user/work/venv-agent-typecheck-v2/bin/python mypy` — **1912/1912**.
- `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json` — **ok**.
- `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` — **artifacts.json is current**.
- `/home/user/work/venv-agent/bin/python scripts/reshape/check_repo_hygiene.py` — **exit 0**.
- `git diff --check ef851b22c..HEAD` — **pass**.
- runtime lock `source_commit` — **34eac0041b0891e9011966b39bcbd26053fde5bc**.
- `astrid/core/timeline/schema/edit-command.schema.json` — **d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d**.
- protected schema/client/lock/Composition package path comparison against
  `ef851` — **unchanged**.
- Composition artifact hashes: 0.0.12 **0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3**;
  0.0.13 **9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738**;
  pinned 0.0.14 artifact (`635f4de...tgz`) **819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234**.

Not run by instruction: full suite, Runtime full/render-20 qualification,
HTTP/live-socket, browser, native 14/58, or duplicate full journeys. No
product/test/env/service/contract/pin/Git writes were made; no daemon or
shared install was modified. The worktree is clean apart from the requested
external reports.

## Recommended next step

Resolve the inventory-test merge conflict as source-backed current coverage
owned by the author/orchestrator, then rerun the exact inventory command and
this final review. Do not restore the retired inventory document or relax the
no-invisible-skips policy merely to obtain green output.
