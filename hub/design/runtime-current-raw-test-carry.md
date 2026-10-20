# Runtime current raw test carry

## Result

Carried only the approved test changes from `f8f775f41f5478e13c705f5646bfe534c2514b6d` onto Runtime base `8f105c26e3b62f9c2683f717a9773a12bc775a8e`.

The worktree matches the source candidate byte-for-byte for both approved paths:

- `tests/historical_audio_fixture.py`
- `tests/test_timeline_public_s2_mixed_cli_journey.py`

`git diff --name-only` shows exactly those two paths. No Runtime product,
schema, client, source-pin, generated, artifact, or private tuple-specific test
file changed. The existing historical-audio `xfail(strict=True,
raises=HistoricalAudioCaptureGap)` remains unchanged.

The fixture carries the approved child-scope/dependency-graph repair, genuine
WAV setup, ordinary Runtime readback, startup admission, and `open_bundle`
control. The `_views` assertion accepts only the exact registered raw or
literal pin and requires the matching dependency-manifest pin.

## Verification

- `git diff --check` — passed.
- AST parse of both changed test modules — passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider tests/test_precut_realm_fixture.py tests/test_timeline_commit_baseline.py` — **62 passed**.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check` — passed (`contract/artifacts.json is current`).
- Public artifact comparison against `/home/user/work/wt/rt-m2-pin-2c4ac180/contract/artifacts.json` — **75/75 byte-identical**.
- Central scoped request `capture-legacy-integration --files tests/test_timeline_public_s2_mixed_cli_journey.py`, request/result ID `rt-m2-current-raw-fixture-testonly-carry-capture-legacy-integration-1020192801-27477` — **1 passed, 1 xfailed** in 28.55s, exit 0, Runtime tree `f12fab3a1f7caf80117bbccedbf9589925b2b0da`. The historical-audio case remains the exact narrow strict xfail; the literal current control passed.

No private historical-positive rerun, full suite, or broad-neighbor suite was
run or claimed. The approved historical expectation review
is `APPROVE` at `design/runtime-historical-f8-expectation-review.md`.

## Handoff

The harness will commit the two test changes using the worker commit message.
The narrow historical capture gap remains a current-source limitation and is
not relabeled as a passing current qualification.
