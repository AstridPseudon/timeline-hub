# Runtime M2 current catalog and clip gates

## Qualification snapshot

This is post-merge evidence for Runtime `6ab3243972f8dc49105819e6d7ba7aef1a2888b8`, tree `c225a680c645c67c3fe1f43b5e564b2a77a05d80` (`text9f` plus native clip parity). No Runtime product or test files were changed by this worker. The central current full was analyzed from its completed artifact; no full suite was requested or rerun by this worker.

## Current full source and classification

`runtime-full-restore-integration-1020160931-14898` targeted
`integration:runtime` and snapshotted Runtime commit `6ab3243` / exact tree
`c225a680c645c67c3fe1f43b5e564b2a77a05d80` (snapshot key
`234cd8b43da0e24a87be6e48dacae3d5`). The external source record is Agent
`f133a87986d839d7716d3efac2c2ba25fe036098`, App
`a04f90cf60eac69a5079f0ab03188abcbd1571fc`, and Composition
`5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8`.

The full source includes catalog promotion `81f8c7e0`, selected-media CAS
`a51af88`, catalog text `9f211fc`, and native clip `6ab3243`; unmerged audio,
ordinary014, carrier, and strict-marker patches are excluded. Its raw result
was **5515 passed, 7 failed, 18 skipped, 18 xfailed, 12 warnings** in
**684.66s** (service elapsed **687s**), exit 1. The seven failures are exactly
the known baseline cohort: six Runtime boundary nodes and one zero-shim node;
there are **0 new failures**. This full is raw RED, not an all-green catalog or
clip gate. No private-floor or storage-floor result is substituted for it.

The current public tuple remains Runtime producer `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`, contract `0.2.13`, schema digest `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`, and public artifact version `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`.

The ordinary014 test fixture deliberately selects a frozen Agent source: `tests/test_timeline_clip_replacement.py:_native_agent_source()` uses `ASTRID_CHECKOUT` when it contains `astrid/sdk/timeline/native_occurrence_create.py`, otherwise `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source`. The intended frozen source is Agent `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`, tree `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`, raw schema `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`. In the central marked lane, `ASTRID_CHECKOUT=/home/user/work/agent` resolved to Agent `f133a87986d839d7716d3efac2c2ba25fe036098`, tree `3f38f816181d7564e5cd7db4d9672a0d6dea9ac3`, which lacks that native module; the deliberate frozen fallback path was also absent. Native marked evidence is therefore unqualified, not waived.

## Central evidence

All requests snapshotted this worktree at tree `c225a680c645c67c3fe1f43b5e564b2a77a05d80`.

1. Bounded ordinary catalog/text/authority/replay lane — result `rt-m2-current-catalog-clip-gates-targeted-1020155957-20270`:

   ```sh
   /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-m2-current-catalog-clip-gates targeted --files "tests/test_shot_text_bindings.py tests/test_shot_candidate_promotion.py tests/test_timeline_shot_authority.py tests/test_timeline_text_binding_clear.py"
   ```

   Service command: `/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_shot_text_bindings.py tests/test_shot_candidate_promotion.py tests/test_timeline_shot_authority.py tests/test_timeline_text_binding_clear.py`.

   **127 passed, 2 deselected, exit 0, 103.17s.** This includes the four unplaced text positives and two original promotion positives.

2. Explicit marked native/CAS/catalog-fence/C4 lane — result `rt-m2-current-catalog-clip-gates-marked-integration-1020160026-30721`:

   ```sh
   /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-m2-current-catalog-clip-gates marked-integration --files "tests/test_timeline_clip_replacement.py::test_native_clip_swap_is_atomic_cas_and_exactly_replayable tests/test_timeline_clip_replacement.py::test_native_clip_swap_rejects_tampered_cas_without_mutation tests/test_timeline_clip_replacement.py::test_native_clip_swap_rejects_selected_source_corruption_between_capture_and_accept tests/test_timeline_clip_replacement.py::test_native_generic_visual_media_accepts_verified_image_swap tests/test_timeline_clip_replacement.py::test_native_clip_swap_replays_after_intervening_edit_and_reopen tests/test_timeline_clip_replacement.py::test_native_clip_swap_public_http_route tests/test_shot_candidate_promotion.py::test_catalog_promotion_preserves_accepted_film_and_retries_before_live_guards tests/test_shot_candidate_promotion.py::test_catalog_promotion_prevents_native_overwrite_after_historical_reuse tests/test_timeline_projection_occupancy.py::test_actual_provider_historical_slot_rematerializes_after_verified_restore"
   ```

   Service command included `-m integration` and used `ASTRID_CHECKOUT=/home/user/work/agent`.

   **3 passed, 5 errors, 1 failed, exit 1, 7.19s.** The three catalog-promotion/C4 controls passed. The five native fixture cases errored because the selected Agent source lacked `native_occurrence_create.py`; the public HTTP native case failed for the same source-selection reason. The log contains no native behavioral pass from this lane. This is an environment/source qualification limitation, not a product refusal and not a new expected failure.

3. Explicit nine-test commit lane — result `rt-m2-current-catalog-clip-gates-commit-integration-1020160030-4237`:

   ```sh
   /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-m2-current-catalog-clip-gates commit-integration --files "tests/test_timeline_commit_integration.py"
   ```

   Service command: `env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/test_timeline_commit_integration.py tests/test_timeline_commit_integration.py`.

   **9 passed, exit 0, 21.45s.** The duplicate file argument was de-duplicated by pytest.

No full, broad, browser, or live external suite was run.

## Retention and coverage audit

The original ten direct clip-writer tests are all retained, with no removals, and remain under the strict `retired_writer` marker (`strict=True`, `raises=RetiredRouteError`, ledger D04 reason). The current file has 13 marked native integration tests, up from 11 in the merge parent; the two additions are:

- `test_native_clip_swap_rebases_after_disjoint_intervening_edit`;
- `test_native_generic_visual_media_accepts_verified_image_swap`.

The current native set retains atomic replay, cross-project, malformed source, tampered CAS, capture-to-accept CAS race, wrong stream, short/end-short source, reopen retry, and public HTTP coverage. The existing parent-route public-schema `pytest.xfail` remains in place; no new skip or xfail was added.

Read-only source checks passed:

```sh
git status --short                         # empty
git rev-parse HEAD^{tree}                  # c225a680c645c67c3fe1f43b5e564b2a77a05d80
git diff --check HEAD                      # pass
```

## Decision and next step

Catalog/text authority, promotion, replay, C4, and the nine-test commit lane are qualified on this snapshot. Native clip/CAS parity is not qualified by the marked lane because the required deliberate frozen ordinary014 Agent source was not available at either selection path. Re-run only the explicit marked native nodes after the exact frozen Agent source is materialized or the central lane is pointed at that exact source; do not relabel the current failure as a native product regression.
