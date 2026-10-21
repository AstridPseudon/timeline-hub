# Runtime published014 integration full: result 25226

## Verdict

The one authorized result `runtime-full-retained-owned-temp-integration-1021025626-25226` is valid and passes. `bin/wait-test` returned `pass exit=0`; no retry or resubmission was made. There were no failed tests, so there is no first failure cause to classify.

Exact counts:

```text
5997 passed, 26 skipped, 15 xfailed, 12 warnings
in 310.11s (0:05:10); wait-test wall time 311s
```

The test process exited `0`, and this is not an EXIT-MISMATCH or fake pass.

## Literal source and test setup

- Requested/current Runtime source: integration commit `be8d254aef249cd421946cbf06ed86d58bc4b307`; snapshot tree `6d74348b66ee4a3602cfa4fd56b9b7c0ed7508e0`.
- The result directory has no separate `source` file; the source record is the `snap` tree, `ext` pins, exact command, and independent git readback above. The current server source is `be8d254`, not published producer `95` and not frozen physical source `8f`.
- The current Runtime commit includes transcript merge `2a9bd811` (source `e2912b3`) and rational-FPS merge `be8d254a` (source `60a919a`).
- Recorded external source pins in the result metadata: Agent `04fdd64205b4a2365e50455bd3ac81b027c617f3`, App `1be92c689c77efc3fe1d82eced116e86459139cf`, Composition `7bb54bbd64107e5090643ecca1e4d33164173e85`.
- The command used exactly:

  ```text
  env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-full-temp-retain-all-final/runtime-full-retained-temp.py -- /home/user/work/venv-runtime/bin/python -m pytest -q -n 3
  ```

- The retained-temp wrapper supplied a private `/tmp/rt-full-xd1nglhz` root, exact `TMPDIR`/`TMP`/`TEMP` overrides, and pytest `--basetemp`; the root remains present, owned by root, mode `0700`, with worker temp contents. This validates the requested diagnostic storage setup, not a product behavior.
- Immutable publication inputs were not changed: published producer `95`, tree `d3a`, schema `7d4`, raw `6ba`, client `0.2.14`, artifact producer `95` / `all76` / artifact `54205`. The separate prior candidate `31902` (`5988/26/15`) was not used as evidence.

The Runtime full suite is therefore valid evidence for the recorded Runtime integration tree and command. It is not evidence that the external Agent has adopted this source: the external Agent may still be on public013 pending coordinated pinning. It also does not establish broad native-platform coverage, physical media/audio/video proof, App/browser journeys, Composition qualification, publication, or release adoption.

## Skips (all 26)

All skips are Linux-host skips for Windows-only APIs:

- `tests/test_m1_review.py`: lines 225, 240, 255, 280, 290 — native Windows socket exclusivity and file DACL APIs (5).
- `tests/test_platform.py`: line 273 — Windows token and process-time APIs (1).
- `tests/test_platform_filesystem.py`: lines 49, 88, 101 — native Windows dir-fd adapter, Windows reparse-point rejection, Windows SQLite backup snapshots (3).
- `tests/test_dirfd_windows.py`: lines 293, 318, 343 (2 skips), 360, 378, 533, 581 — native Windows dir-fd adapter (8).
- `tests/test_platform_windows.py`: lines 20, 27, 44, 61, 81, 91, 109, 126, 173 — native Windows process and lock APIs (9).

These are expected platform exclusions under the plan's Linux test policy, not failures.

## Expected failures (all 15)

The 15 strict xfails are the already-authorized retired direct-write/legacy-publication surface, awaiting the `/v1` commit replacement:

- `tests/test_second_client_e2e.py::test_second_client_core_journey_is_executable` — RT02/D04 direct shot writes and legacy timeline publication retired.
- `tests/test_runtime_domains.py::test_generated_python_client_timeline_publication_is_retired_pending_commit_replacement` — `update_timeline` retired.
- `tests/test_stage1_runtime_contract_completion.py::test_timeline_update_archive_recover_replay_the_same_committed_receipt` — direct timeline writes retired.
- `tests/test_runtime_domains.py::test_generated_direct_timeline_shot_reference_writers_remain_retired` — direct timeline update writer retired.
- `tests/test_runtime_exact_idempotency.py::test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting` — direct shot writes retired; the reference catalog half is retained.
- `tests/test_timeline_clip_replacement.py`: `test_replace_timeline_clip_is_atomic_cas_and_exactly_replayable`, `test_replace_timeline_clip_rejects_cross_project_source`, `test_replace_timeline_clip_rejects_malformed_source_without_mutation`, `test_replace_timeline_clip_rejects_tampered_cas_without_mutation`, `test_replace_timeline_clip_rejects_wrong_stream_without_mutation`, `test_replace_timeline_clip_rejects_too_short_source_without_mutation`, `test_replace_timeline_clip_requires_source_to_reach_authored_end`, `test_replace_timeline_clip_generic_visual_media_requires_video_stream`, `test_replace_timeline_clip_replays_after_intervening_edit_and_reopen`, and `test_replace_timeline_clip_public_http_route` — direct clip replacement retired pending the commit-path replacement (10).

The xfails were reported as expected and were not converted into failures or removed.

## Warnings and scope

The 12 warnings are `DeprecationWarning` instances from Python 3.13's `multiprocessing` fork path: 10 from `tests/test_realm_admission_hardening.py` and 2 from `tests/test_t4_replacement_foundation.py`. They do not affect the exit status.

This result proves the Runtime full suite on the stated integration tree, including the retained transcript and rational-FPS changes. It does not prove matching cross-repository adoption, native Windows behavior, physical media behavior, or publication. Preserve the retained root and all result artifacts; no follow-up full run is indicated. A future coordinated Agent pin/adoption check remains a separate manager-owned action.
