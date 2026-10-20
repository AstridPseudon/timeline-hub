# Runtime current-test carryforward report

Date: 2026-10-20 UTC

## Exact delta

- Base: Runtime commit `919c9017fda6b17d6e2420511fd588729b9e90e4`, tree `e9ec260a247bd44feef8ae996630d1a52a7a2497`.
- Copied `tests/test_timeline_clip_replacement.py` exactly from `6ab3243972f8dc49105819e6d7ba7aef1a2888b8`.
- Test blob SHA-1: `183f14dbe64466c9a8c7aec5b34850da9272f107` (verified against the source commit).
- Relative to current source `9f211fcdb66023a577a14111f99c87fb32ef573c`, the required test delta is exactly `+215/-41`.
- Relative to this private carrier base `919`, the resulting test-file diff is `+215/-98`, because the carrier's prior test blob differs from current `9f`.
- Removed the accidentally committed product document `design/runtime-carrier-cas-text-current.md`. Its exact content is published at:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-carrier-cas-text-current.md`.
  Source and published document blob SHA-1: `91ef2683a7fc3bb8e200cfb78ec39ab34dc44845`.

No other product or generated files changed. The private f802 schema/bundle, current 0.2.13 floor, private carrier files, audit/shell/text/catalog paths, and existing xfail markers remain untouched.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B generators/generate.py` — PASS.
- Same environment, `generators/generate.py --check` — PASS.
- Same environment, `scripts/artifact_manifest.py --check` — PASS.
- `git diff --check` — PASS.
- Central targeted socket-capable lane:
  `/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_clip_replacement.py tests/test_shot_text_bindings.py tests/test_timeline_shot_authority.py tests/test_shot_candidate_promotion.py tests/test_render_native_historical_retry.py tests/test_timeline_projection_ownership.py`
  — PASS: **164 passed, 20 deselected, 10 xfailed** in 124.36s. The 10 xfails are the pre-existing strict D04 retired direct clip-replacement expectations.
- Local direct clip-file run:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider tests/test_timeline_clip_replacement.py`
  — sandbox-blocked at the unmarked public HTTP route test with `PermissionError: [Errno 1] Operation not permitted` while binding a localhost socket; 9 existing xfails and 14 deselected. The central socket-capable lane above passed this route as an existing xfail.

No full suite and no coordinated `3730` native pair were run.

## Harness tree

The central targeted harness snapshot after the edits was tree `0a5bd960862875eac265deeedb543611675ca577`. Its diff from `919` contains exactly two product-repository paths: the required test carryforward and the carrier-document deletion.

## Decisions / next steps

The settled review decision was followed: carry the exact current `6ab` test blob, remove the accidental product document, and publish its content only under orchestration `design/`. No public adoption, release, ordinary `0.2.14` import, or native-pair qualification was attempted.

Recommended next steps are the planned Agent peer review of the `919`/carrier composition and then exactly one coordinated `3730` pair.

