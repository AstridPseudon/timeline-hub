# Fastlane producer/source lifetime join review

Decision: **HOLD — do not approve activation yet.**

Reviewed candidate `0a6162f12` (`fix(rendering): activate fast-lane scene result carrier`) against approved consumer seam `de7ab77f1` and the settled Timeline plan. The source/result carrier itself is bounded and uses the existing managed `scene_only` bundle: `_scene_only_spans` and `_scene_only_bundle_payload` validate source, snapshot label, frame extent, and compiled address bindings before `_scene_frame_carrier` materializes `CaptureSceneLabels` rows. No live provider or context is carried past executor cleanup; no new DTO, source factory, authority, store, public field, or entrypoint was added. The original stale/forged/unavailable refusal behavior remains fail-closed.

The required activation proof is missing. The new test at `tests/packs/rendering/test_fast_lane_words.py:136-167` calls `_scene_frame_carrier` directly, stores the returned object in a local `provider`, and injects it into `_labelled_tiles(..., frame_providers={"published": provider})`. It therefore proves the consumer seam can consume a test-created carrier, not that a normally invoked successful `prepare_pair`/managed executor result reaches public labels. The existing normal `prepare_pair` integration test at `tests/sdk/test_timeline_checkout.py:1232-1456` asserts render/video/snapshot behavior only and does not assert `frame_providers` or public label output. Its docstring explicitly says caller keys were not recorded (`:1233-1236`). This is the exact blocker under the task brief; the dormant consumer must not be counted as activation.

Required follow-up: extend the existing normal `prepare_pair` caller test (or an equally direct normal-caller test) so the managed `scene_only` executor invocation returns a successful, source-bound bundle, `prepare_pair` returns its materialized `frame_providers`, and the public labels path consumes those rows while private `visible_at`/PNG/config inference is tripwired. Keep the existing stale/forged/refusal positives active. No new carrier or authority mechanism is needed based on this review.

## Evidence

- `git diff --check de7ab77f1 0a6162f12`: passed.
- Candidate focused suite from throwaway archive `/tmp/fastlane-review-10LQb5`: `PYTHONPATH=/tmp/fastlane-review-10LQb5:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q /tmp/fastlane-review-10LQb5/tests/packs/rendering/test_fast_lane_words.py /tmp/fastlane-review-10LQb5/tests/sdk/test_scene_caller_preservation.py` — **24 passed**.
- Candidate normal prepare-pair integration lane: `PYTHONPATH=/tmp/fastlane-review-10LQb5:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q /tmp/fastlane-review-10LQb5/tests/sdk/test_timeline_checkout.py -k 'fast_lane_pair_keeps_real_explicit_working_snapshot_and_original_video' -m integration` — **5 passed, 99 deselected**. This validates the existing prepare-pair/render boundary, but not the required label activation.
- `ruff check` on the two candidate-touched files: passed.
- No full, browser, native, socket, install, or shared-dependency write was run.

Author execution log reviewed: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-fastlane-real-producer-join-1240/log.txt`.

No product files were changed in this review worktree.
