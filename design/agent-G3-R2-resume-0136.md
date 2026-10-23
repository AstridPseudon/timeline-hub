# R2/G3 compound inverse recovery: completed source handoff

The physical-image failure is resolved by joining current R2. No additional
product semantics or guard changes were needed. This resume adds documentation
only; it preserves the regression extension already committed in the WIP.

## Actual ancestry and retained work

- Resume base: `374e869190277799d5a574472329beac1c5761c8`.
- First parent, completed G3: `44b46935a1bcf2eed87f9e048eb2725d52fa7c16`.
- Second parent, current R2: `4454a7a2f246e5bfc27c583cca4b660d2154fa91`.
- The prior worker's `MERGE_EXECUTED` records the manager's actual clean merge
  at 2026-10-23 01:21 UTC. The resume inspected the actual two-parent commit;
  it did not wait for another merge or change Git state.
- `git show --remerge-diff --stat HEAD` reports only the compound regression
  extension: 8 insertions and 2 deletions in `test_authoring_media.py`.
- The six R2 files below are byte-for-byte identical to current R2. G3's exact
  original-source hydration, public read, emitter, and helper changes remain.
  Current R1/P1/V4/U2/U4a are inherited through the R2 parent.

```sh
git log -1 --format='%H %P'
git show --remerge-diff --stat HEAD
git diff --quiet 4454a7a2f HEAD -- astrid/sdk/timeline/_collections.py astrid/sdk/timeline/_commit_patch.py astrid/sdk/timeline/_root_inverse.py astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/commit.py astrid/sdk/timeline/inverse.py
```

All three commands exited 0 on the resume base. The last produced no diff.

## Diagnosis and preserved authority

G3 alone reached forward acceptance and reload but attempted to treat a
physical `shot-revision:` binding as a native entity during inverse input
validation. Current R2 distinguishes authenticated physical guard inputs from
native entity aliases. The provider loads accepted records and their exact
before/after closures, verifies publication ancestry, selects original command
ordinals, and supplies `inverse_address_resolver` to the later-step scan. That
resolver requires the existing materialization bindings and original owner
edges for continuation. Physical refs are therefore not re-resolved as native
entities in `_validate_inputs`.

The existing `_root_inverse` and `_step_undo` helpers remain authoritative.
There is no new inverse DTO, raw inverse patch, alias inference, history rewrite,
or capture against a later head. Existing later-write, A-to-B-to-A, same-batch,
surviving-dependent, media, and transcript guards remain unchanged.

The retained compound regression exercises same-alias media replacement plus
residual timing, list order, opaque values, explicit null, and absence changes.
It checks exact original canonical-document restoration, bundle/document reload,
exact redo of the accepted document, another reload, and a second exact undo.
Each `MediaRealm.call` creates a fresh production provider over detached retained
history. This proves provider reconstruction and JSON reload; it does not prove
a live Runtime process restart or transport acceptance.

## Verification on this resume

Working directory: `/home/user/work/wt/agt-G3-R2-resume-sol-0136`.
The worker's `tmpdir` file contains `/tmp/w-1fca510a2a`; that resolved private
directory was used for scratch and caches.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime TMPDIR=/tmp/w-1fca510a2a /home/user/work/venv-agent/bin/python -m pytest -q tests/timeline/test_authoring_media.py::test_public_document_compound_inverse_restores_exact_original -o cache_dir=/tmp/w-1fca510a2a/pytest-cache --basetemp=/tmp/w-1fca510a2a/pytest-compound
```

**PASS: 1 passed in 10.86s.** The first setup attempt incorrectly used the
`tmpdir` pointer file as a directory and was interrupted (exit 130, no test
result); the command above used its contents and completed successfully.

```sh
git diff --check
```

**PASS: exit 0**, including after the documentation was written.

## Retained completed checks from the interrupted worker

These results were read directly from
`workers/agt-G3-R2-joined-inverse-sol-0119/log.txt` under the orchestration
scratchpad. They were run in
`/home/user/work/wt/agt-G3-R2-joined-inverse-sol-0119` on the joined source,
including the regression extension now retained in `374e86919`. They were not
rerun on this documentation-only resume, per the instruction to check only
unfinished or changed work.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o cache_dir=/tmp/w-cf3765b3d3/pytest-cache --basetemp=/tmp/w-cf3765b3d3/pytest-r2 tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_provider_step_undo_v2.py tests/editing_conformance/test_doc_patch_v2.py tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_timeline_commit_provider.py tests/editing_conformance/test_inverse_clear_batches.py tests/editing_conformance/test_grouped_clip_cache_inverse.py tests/editing_conformance/test_occurrence_media_manifest_inverse.py
```

**PASS: 425 passed in 105.05s.**

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o cache_dir=/tmp/w-cf3765b3d3/pytest-cache-g3 --basetemp=/tmp/w-cf3765b3d3/pytest-g3 tests/timeline/test_authoring_media.py tests/editing_conformance/test_document_patch_emitter_v2.py tests/editing_conformance/test_document_patch_emitter_engine.py tests/editing_conformance/test_recipe_occurrence_media.py tests/sdk/test_authoring_revision_diff.py tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_persistence.py
```

**PASS: 274 passed, 2 deselected in 74.95s.** Deselection is the unchanged
repository default lane, which excludes integration/live/platform/opt-in tests.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_collections.py astrid/sdk/timeline/_commit_patch.py astrid/sdk/timeline/_root_inverse.py astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/commit.py astrid/sdk/timeline/inverse.py astrid/sdk/_remote_timeline.py astrid/sdk/timeline/emitter.py astrid/sdk/timeline/sync.py astrid/packs/rendering/docs/scripts/timeline_document.py tests/timeline/test_authoring_media.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" MYPY_CACHE_DIR=/tmp/w-cf3765b3d3/mypy-scope /tmp/astrid-u2-typecheck/bin/python -m mypy astrid/sdk/timeline/_collections.py astrid/sdk/timeline/_commit_patch.py astrid/sdk/timeline/_root_inverse.py astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/commit.py astrid/sdk/timeline/inverse.py astrid/sdk/_remote_timeline.py astrid/sdk/timeline/emitter.py astrid/sdk/timeline/sync.py astrid/packs/rendering/docs/scripts/timeline_document.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" RUFF_CACHE_DIR=/tmp/w-cf3765b3d3/ruff-cache make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" MYPY_CACHE_DIR=/tmp/w-cf3765b3d3/mypy-ratchet make mypy PY=/tmp/astrid-u2-typecheck/bin/python
```

**PASS:** scoped Ruff; private mypy, no issues in 10 source files; ordinary Ruff
ratchet **2150/2150**; private mypy ratchet **1915/1915**. The 2150 Ruff baseline
was already retained from G3; this resume did not change either baseline. The
private mypy environment supplies the valid stubs absent from the dependency-only
shared environment. No shared dependency or cache files were modified.

## Remaining wire limits and handoff

The production caller remains `commit_session.Timeline.commit` → `TimelineSession.submit`
→ the remote commit operation, preserving label, steps, per-step patches, merge,
and reads. The provider retains `label`, `steps`, `merge_mode`, `undo_steps`, and
the complete v2 prepared result. No metadata was stripped to fit an older DTO.

Frozen Runtime compatibility remains unqualified: the prior R2 handoff records
16 Runtime failures rejecting v2 prepared fields (`label`, `merge_mode`, `steps`,
`undo_steps`) before acceptance. These failures were not rerun, bypassed, or
converted into passing expectations here. No actual wire success is claimed.
Schema768/floor repair, canonical/generated schemas, pins, Runtime, and G4
bootstrap/render publication remain outside this task and were not edited.

No full suite, browser, localhost service, cleanup, Git mutation, or new product
scope was requested or performed on this resume. Nothing is blocked within this
source handoff. Recommended next steps: independently review the exact joined
parents and retained regression, then let the Runtime owner qualify the complete
v2 wire and durable restart path after its DTO/store adoption.
