# Agent M2 element current union — S2 source composition

Completed the bounded source task on `tl/agt-m2-element-current-union`, based on current integration `df2739f903edac02bd36b4446deeea847524c040`. No commit/merge/rebase/checkout/push, dependency install, Runtime pin/client change, endpoint cut, integration or ledger edit occurred. Shared dependencies stayed read-only; tests used worktree code through PYTHONPATH and disabled pytest cache writes.

## Changes, separated by responsibility

1. **Producer delta only:** ported producer.guard registration, provider capture, recorder/rebase forwarding, settled proposal builder and support in the existing durable requester outbox from `0a0ac7ba`. Kept all current auto/pool/eligibility code and auto/media fixtures unchanged; no old whole fixture overwrite. Ported producer/numeric/outbox tests and the existing complete-schema compatibility helper/floors.
2. **Element/WC4 source delta:** ported `167d0505^..98c38a7c` on the bounded paths. Parent element updates emit one native batch (set-element, optional literal source-seconds hold, optional nonempty explicit params patch). Removed the helper's whole-candidate publisher and helper-owned mirror updates. Exact retained declaration/snapshot inputs and pack owner are enforced for element-only updates. Params remain literally absent/empty where appropriate, opaque state survives, inverse/redo/replay use retained inputs.
3. **Current merge preservation:** public12, D07, auto+pool and equal-state occurrence-delete positives stay current. No capturing-host `92427b3a` changes were imported; its host/capture work was absent from this base. Existing `commit.py` hunks were preserved by narrow patch application. No parent clip.add-media/assembled-target variants.
4. **Canonical schema:** 48 definitions / 22 operation conditions. S2 is byte-identical to frozen S1 `0a0ac7ba` except the reviewed ClipSetElementArgs definition: ONE optional existing DocumentPin schema_source plus its reviewed owner/retained-pin description. Required elementRef and closed args remain. Every other definition, op conditional, consumed field, numeric constraint, root and inverse/restore shape is unchanged. Raw S2 SHA256: `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`.
5. **Permanent gaps:** main-suite Runtime tests now include 14 raw element-only negatives (missing pin, inline schema, bad version/digest, changed id/kind/owner, unadmitted revision, revoked/legacy admission, missing/corrupt snapshot, foreign-project pin, authorization) and a second genuinely admitted pack with matching id/kind. Provider and helper both refuse the admitted cross-owner substitution. Assertions retain head, document and history on refusal. The original nine retained-element cases remain intact; the module now has 24 cases.
6. **Compatibility regression:** complete immutable S1, current df2739f9 and existing Agent c456b328 / published Runtime6023cfb floors are guarded by pinned raw snapshots. Every definition/op deletion is detected despite the generic envelope. Existing numeric narrowing is refused. An independent exact S1 comparison permits only the reviewed element-source addition/description.

Published the separate flat handoff `design/agent-canonical-element-successor.md` under ORCH. The S1 `design/agent-canonical-current-union.md` freeze remains untouched. S2 is a source candidate awaiting explicit manager freeze and normal generation, not an activation approval.

## Exact source commands

All ran in `/home/user/work/wt/agt-m2-element-current-union`. Existing product hunks were checked with `git apply --check` before application; exit 0. New test/helper files were then included in the bounded application commands below.

```sh
git diff 0a0ac7ba^ 0a0ac7ba -- astrid/sdk/timeline/__init__.py astrid/sdk/timeline/_recording.py astrid/sdk/timeline/commands.py astrid/sdk/timeline/commit.py astrid/sdk/timeline/rebase.py astrid/sdk/timeline/sync.py astrid/sdk/timeline/producer.py tests/editing_conformance/test_producer_guard.py tests/editing_conformance/test_settled_proposal_contract.py tests/editing_conformance/fixtures/settled_proposal_move.artifact.json tests/editing_conformance/fixtures/settled_proposal_move.json tests/editing_conformance/fixtures/settled_proposal_numeric.artifact.json tests/sdk/command_schema_compatibility.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_producer_guard.py tests/sdk/test_timeline_producer_guard_runtime.py tests/fixtures/current-union-command-schemas | git apply

git diff 167d0505^ 98c38a7c -- astrid/sdk/timeline_elements.py astrid/sdk/timeline/_clip_scalar_commands.py astrid/sdk/timeline/commit.py tests/core/test_timeline_element_publication.py tests/core/test_timeline_element_publication_runtime.py tests/editing_conformance/fixtures/recipe_m2_clip_set_element.json tests/editing_conformance/test_recipe_clip_set_element.py tests/sdk/test_timeline_selected_schema.py | git apply
```

Both exit 0. Full source refs: `0a0ac7baaa74e15485b10bcbaa80eda1afe48c00`, `167d050506b9ae81fe8839f122de34d2082558cf`, `98c38a7c85a3f1d2a8c5a1019a5815898ec922f5`.

Schema composition used read-only `git show 0a0ac7ba:astrid/core/timeline/schema/edit-command.schema.json` and `git show 98c38a7c:astrid/core/timeline/schema/edit-command.schema.json`, replacing only the raw ClipSetElementArgs block in S1. Kept original whitespace everywhere else. S1/current complete snapshots came from `git show 0a0ac7ba:<schema-path>` and `git show HEAD:<schema-path>`. Promoted review scratch probes into the permanent Runtime module and added the unadmitted revision/history assertions, rather than claiming scratch evidence as permanent coverage.

Product source manifest SHA256: `82102acd57bc562a321708eda295053953cb582bc52f36d3f03125928fb5c88a` (exact manifest and definition in S2 handoff). Central snapshot Git tree: `65fe2ed84a8cc09914f3dec0e4ddb854d9b30612`. A read-only comparison of every changed product/test file using `git show <snapshot>:<path>` confirms all bytes match final local source/tests. Only documentation was added after the snapshot. Final harness commit is pending; manager must resolve and explicitly freeze it.

## Exact test commands and results

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/core/test_timeline_element_publication.py tests/editing_conformance/test_recipe_clip_set_element.py tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/editing_conformance/test_recipe_scalar_commands.py tests/sdk/test_timeline_selected_schema.py tests/sdk/test_timeline_clip_scalar_provider.py tests/sdk/test_timeline_commit_provider_scalar.py
```

**287 passed in 112.64s; exit 0.** Same selected file set as the source review. Includes scalar hold/rational-fps/source-seconds neighbors; this is not pixel/render evidence.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_producer_guard.py tests/editing_conformance/test_settled_proposal_contract.py tests/sdk/test_timeline_producer_guard.py tests/editing_conformance/test_recipe_m2_auto_placement.py tests/editing_conformance/test_recipe_m2_shared_auto_placement.py tests/editing_conformance/test_recipe_occurrence_media.py tests/editing_conformance/test_recipe_m2_placement_create_unplace.py --tb=short
```

**331 passed in 43.69s; exit 0.** Current auto/pool neighbors account for the higher count than the older producer-source run. Includes native guard, JS numeric forwarding, artifact custody/value vectors and existing-outbox exact-flight restart tests.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_composed_schema.py
```

**23 passed in 172.20s; exit 0.** Whole-schema compatibility, deletion/narrowing regressions, exact S1 delta, JSON Schema validity and operation goldens.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_sync_native.py tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_document.py tests/sdk/test_timeline_semantic_reservations.py --tb=short
```

**250 passed in 96.15s; exit 0.** Ordinary outbox/native batching/provider/reservation neighbors.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/core/test_timeline_element_publication_runtime.py
```

**24 passed in 61.55s; exit 0.** Original retained-element nine plus 15 permanent refusal controls. In-process RuntimeService only, no daemon/socket. This module selects immutable vendored Runtime94114269 despite the locator's current HEAD.

Central request (once, named suite only):

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-m2-element-current-union commit-integration --files "tests/core/test_timeline_element_publication_runtime.py tests/sdk/test_timeline_selected_schema_runtime.py tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py"
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test agt-m2-element-current-union-commit-integration-1020100507-2360 1
```

The named suite executes:

```sh
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_m1.py tests/core/test_timeline_element_publication_runtime.py tests/sdk/test_timeline_selected_schema_runtime.py tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py
```

**49 passed in 143.97s; central pass, exit 0** (original 34 plus 15 negatives). Service elapsed 159s; final wait-test returned exit 0. Prior nonblocking `wait-test ... 0` checks returned 124 while service finalization was pending; never resubmitted. Result directory: `ORCH/tests/agt-m2-element-current-union-commit-integration-1020100507-2360`. External locator head was Runtime c0dcd387; pinned test module still runs 94114269. Source/test snapshot matches final files exactly.

Real producer check uses an untouched worker-owned Runtime archive from:

```sh
git -C /home/user/work/runtime archive 6023cfb10307b4c0004642b5fa1995d72ba4f6d1
```

Archive bytes were extracted with Python tarfile (data filter) to `ORCH/workers/agt-m2-element-current-union/runtime6023cfb`, never over a shared checkout/dependency.

```sh
env ASTRID_RUNTIME_CHECKOUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-element-current-union/runtime6023cfb PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/sdk/test_timeline_producer_guard_runtime.py -rx --tb=short
```

**4 passed, 1 strict xfailed in 13.69s; exit 0.** This is not a green producer positive. Original acceptance/restart/exact retry/one-shot/undo expectation is unchanged and marked strict xfail with the D13 restoration requirement.

```sh
env ASTRID_RUNTIME_CHECKOUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-element-current-union/runtime6023cfb PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_numeric_proposal_accepts_retries_after_restart_and_undoes --runxfail --tb=short
```

**1 failed in 7.81s; exit 1**, reproducing the known normalized-guard boundary at preview: `producer_dependency_unavailable`, “producer authority requires its guard record”, Runtime timeline_commit_port.py:357. Runtime compares Agent's normalized recorded command to the bare original request guard. This was not worked around and no accepted producer behavior is claimed.

```sh
/home/user/work/venv-agent/bin/ruff check --no-cache astrid/sdk/timeline/__init__.py astrid/sdk/timeline/_clip_scalar_commands.py astrid/sdk/timeline/_recording.py astrid/sdk/timeline/commands.py astrid/sdk/timeline/commit.py astrid/sdk/timeline/producer.py astrid/sdk/timeline/rebase.py astrid/sdk/timeline/sync.py astrid/sdk/timeline_elements.py tests/core/test_timeline_element_publication.py tests/core/test_timeline_element_publication_runtime.py tests/editing_conformance/test_recipe_clip_set_element.py tests/editing_conformance/test_producer_guard.py tests/editing_conformance/test_settled_proposal_contract.py tests/sdk/test_timeline_selected_schema.py tests/sdk/command_schema_compatibility.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_producer_guard.py tests/sdk/test_timeline_producer_guard_runtime.py
git diff --check
sha256sum astrid/core/timeline/schema/edit-command.schema.json
```

Ruff: **All checks passed, exit 0**. Diff check: **exit 0**. Hash matches above. Initial promoted scratch lambda triggered E731; changed it to a def before any Runtime tests/central snapshot, then lint passed. An initial schema-construction assertion failed before writing; corrected block extraction and verified exact S1 diff before tests. No failed tests were skipped/disabled/weakened.

Preservation check, exit 0:

```sh
git diff --exit-code HEAD -- runtime.lock.json astrid_runtime_client astrid/sdk/timeline/native_auto_placement.py astrid/sdk/timeline/native_occurrence_media_commands.py astrid/sdk/timeline/native_placement_commands.py tests/editing_conformance/fixtures/recipe_m2_auto_placement.json tests/editing_conformance/fixtures/recipe_m2_shared_auto_placement.json tests/editing_conformance/fixtures/recipe_m2_occurrence_media.json tests/editing_conformance/fixtures/recipe_m2_placement_create_unplace.json astrid/core/execution/generic_host.py astrid/core/rendering/verified_source.py astrid/sdk/timeline_filmstrip.py
```

## Decisions, limitations and next steps

No design decision was changed. Used the review's exact S1-plus-element successor; copying the older element schema would incorrectly drop producer/consumed behavior. Source composition is complete, so DONE is appropriate; qualification gates remain held explicitly.

The public element helper preflights expected_head on every invocation. Calling it again with the old head after acceptance returns conflict before reaching idempotency storage; Runtime replay of the original captured request is the proven retry boundary. There is no new helper outbox guarantee. HTTP/public ErrorObject mapping and element-specific changed-payload/same-key behavior on a newly generated pair remain unverified.

Runtime pin is still 94114269/0.2.9, whose generated client has no typed set-element variant. Runtime6023cfb/0.2.10's published schema also lacks typed producer.guard. These tests demonstrate source/service behavior through existing envelopes, not new typed publication. No full/full* suite, make check, renderer/pixel parity, sockets/browser/App journey, authentic assembler-selected-video handoff or macOS test ran or was requested. No WC4 deletion-ledger closure or endpoint retirement is claimed.

Manager next: resolve the harness commit, verify S2 hash and explicitly freeze this successor separately from S1; gate NEW normal Runtime generation/release from the full S2 bytes; reconcile Runtime's normalized guard boundary; refresh Agent with the normal vendor-lock procedure; rerun the original positive producer and retained-element qualification on the immutable generated pair before activation or WC4 closure. Private Runtime extraction was removed before exit; no build/temp output remains in the worktree.
