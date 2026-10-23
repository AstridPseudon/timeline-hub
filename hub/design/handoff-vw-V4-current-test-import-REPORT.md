# V4 current-test import report

## Result

Applied only the reviewed V4 two-file test deltas on actual Agent integration
base `9729c07b764ba6cce1bb31686cb93d29fc72b14d`:

- `tests/editing_conformance/native_word_anchor_fixture.py`: added the
  canonical initial `track.create` created reference
  `[`"`parent/track:initial`"`]`.
- `tests/editing_conformance/test_native_word_anchor.py`: changed the three
  donor-approved `invalid_anchor` status expectations to `invalid`, `invalid`,
  and `conflict`. The other relevant negative expectation was already
  `conflict` and was unchanged.

No production/provider/runtime/schema/generated/lock/manifest files changed;
no latent rebased expectation was updated.

## Exact source parity

Final working-tree blobs exactly match donor commit `5292b388a`:

- `native_word_anchor_fixture.py`:
  `af7407a5a2d42bb63b5cc11ba4a4924d3186c607`
- `test_native_word_anchor.py`:
  `5db819f485da679f613ef04455ec19708d316d6a`

The worktree started clean. `git status --short` after editing listed only the
two assigned test files. No donor commit was merged, cherry-picked, or added to
ancestry; the branch remained directly on the required base until the harness
commit.

## Checks

- `/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/native_word_anchor_fixture.py tests/editing_conformance/test_native_word_anchor.py`
  — passed (`All checks passed!`).
- `git diff --check` — passed.
- The required combined five-case command was run once with Runtime pin
  `ad823e0a` — failed during fixture setup for all five selected cases before
  their assertions. The initial seed was rejected by the pinned Runtime with
  `candidate: all authored fps values must be the same rational rate`.
  Result: `49 deselected, 5 errors in 5.26s`.

No full, browser, heavy replay, or additional targeted test was run.

## Blockers / next steps

The requested test evidence is blocked by the Runtime-pinned setup failure,
not by the imported hunks. Investigate the exact-rational-FPS setup mismatch
with the orchestrator/Runtime owner; do not change these reviewed tests to make
the run green. Independent review and home-integrated proof remain required.

