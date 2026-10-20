# App peer review: repaired transition findings

## Verdict

**ACK — bounded repair accepted for the two prior App findings.**

This ACK is for the clean Agent descendant `ca9f5f8eeba96bb9cb8f9d700c2714c2ed9f9a20`, whose source is equivalent to repaired commit `5b3e41941b1263011f52f9f1291cbbc854563dbb` and whose only change is deletion of the accidental process document. It is not an App activation, generated-artifact, sourcefreeze, or end-to-end consumer approval.

## Reviewed identity and scope

- App base: `hub/tl/integration`, current worktree `20ea14c26`.
- Repaired Agent commit: `5b3e41941b1263011f52f9f1291cbbc854563dbb`.
- Repaired committed tree: `705fc969ffcc2281d3b3e808e68e8a02467066bc`.
- Clean descendant tree: `87b432d48b0e1a5e0410c630ca76150095075eff`.
- Schema SHA-256 (unchanged): `a70f0e8898c6acccb34062e73733c93dd4e7bc22c34ef012431e1791907e1f4a`.
- Repaired source hashes: `_clip_scalar_commands.py` `db72c5dbaed2eac46b9a5132dcbbc5533bcca904fdc725e9a5e821b9d6dbf8d6`; `_selected_param_authority.py` `2747d3c64a5eebe9ee11c5c8fca5f23afaa13f6c9ef406a98eeaec572924bed8`; `commit.py` `d5faef1698d183017eb6a39710ca012e83d26469f88e1621f0214ab164c6ce88`.

Only the two repaired findings were rechecked: Main adjacency/frame-fit acceptance and retained P1 authority for an unchanged selected reference. The existing carrier, schema, clear semantics, and other transition contract were not re-reviewed beyond confirming that this repair does not alter them.

## Findings

### Main adjacency and shortest-clip fit — closed

Current App `element-adapter.ts` requires same-track adjacency with `abs(from.end - to.start) < 0.001` and rejects a duration greater than the shorter adjacent clip. The repaired Agent `_transition_set` now:

- requires exactly one recorded `transition.predecessor`;
- reads the predecessor and destination rows and checks the same authored `at`/`at_ms` endpoint relation with the same strict `< 0.001` rule; and
- rejects `frames > min(predecessor_duration, target_duration) * fps + 0.0001`, without clamping or stripping fields.

The existing selector supplies the same-track predecessor and the repair preserves the recorded selection/binding path for parent and occurrence-owned targets.

### Same-reference selected-pack authority — closed

For `clip.set`, the repaired schema resolver recognizes a same `(packId, id, kind)` reference and invokes the existing retained selected-authority chain. The association then compares the recorded original element identity, including revision, and requires the command’s `elementRef` to equal that retained identity. A later P2 for the unchanged reference therefore refuses atomically; it cannot replace the original P1 merely by supplying a newer `schema_source`.

The authority resolver retains owner-qualified bindings and occurrence/history checks. `clip.set-element` remains the explicit reselection path, so a genuine reselection can intentionally establish a new authority rather than being smuggled into an ordinary same-reference transition update.

### Clear, paired removal, and opaque data — unchanged

The repair diff does not modify `_transition_clear_pair` or the transition-only clear branch. The prior contract remains: explicit paired `clear: ['transition', 'elementRef']` validates the matching transition identity and removes the legacy alias when valid; ordinary `clear: ['transition']` does not infer or remove either reference and preserves unrelated/opaque fields. No DTO, operation, schema, pin, generation path, or App product source changed.

## Evidence

Supplied Agent evidence, not rerun here because the successful source lanes were already reported:

```text
PYTHONPATH=. /home/user/work/venv-agent/bin/pytest -q tests/sdk/test_timeline_transition_schema.py tests/sdk/test_timeline_selected_param_authority.py tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/sdk/test_timeline_clip_scalar_provider.py tests/sdk/test_timeline_current_union_schema.py
```

Result: **183 passed**.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/pytest -q -p no:cacheprovider --basetemp=/tmp/agt-review-transition-current-peer-repair-tests tests/editing_conformance/test_recipe_clip_scalar_fields.py -k 'private_transition or transition_only_clear or explicit_transition or transition_set_enforces' tests/sdk/test_timeline_transition_schema.py
```

Result: **7 passed, 136 deselected**.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/pytest -q -p no:cacheprovider --basetemp=/tmp/agt-review-transition-current-peer-repair-authority-tests tests/sdk/test_timeline_selected_param_authority.py -k 'disjoint_peer_and_paginated_reload or inverse_consumed_pin or batch_reselection_changes_stage_authority or param_after_inverse or equal_selection_aba or param_cannot_reselect_pin_after_relevant_peer_selection'
```

Result: **7 passed, 20 deselected**.

```text
PYTHONPATH=. /home/user/work/venv-agent/bin/pytest -q tests/editing_conformance/test_recipe_clip_scalar_fields.py -k 'transition' tests/sdk/test_timeline_transition_schema.py
```

Result: **29 passed, 87 deselected**.

Fresh focused App controls run for this review:

```text
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs ./node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/runtime/element-adapter.test.ts src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx src/tools/video-editor/commands/ordinaryScalarMember.test.ts
```

Result: **3 files, 51 tests passed**.

No full suite, browser, localhost/socket, dependency install, Runtime-door run, generation, pin, or sourcefreeze operation was run.

## Consumer prerequisite

No remaining mismatch was found in the two repaired findings. Before App consumes this contract, integrate the clean Agent source/schema pair and publish the normal generated Runtime artifact. Then qualify the App native element producer through the existing scalar capture/session/outbox path with apply, same-reference update, explicit reselection, paired remove, ordinary clear, parent/occurrence, retry/reload/undo, and zero legacy direct-save traffic. This review does not claim those consumer gates are complete.
