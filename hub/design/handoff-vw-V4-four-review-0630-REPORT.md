# V4 independent actual-four proof review

## Result

**PASS — scoped actual four-case proof only.** This review does not claim the
five-case, 52-case, 54-case, native14, full-suite, browser, or V4-DONE gates.

## Verified boundary

- Agent HEAD: `3e4261e9694c7bd7c1b5fada9bf01d91007bcc80`; tree:
  `fbaebb606643a38391dbaf7f4a584bef390048af`.
- Reviewed boundary repair `b42b7d72a65cab305a4b953093963019aabc70b9` is an
  ancestor. G234 ancestry is present; current `sdk/timeline/rebase.py` is the
  exact blob from `c79398561e5612d0a393074e6b9a198992d77f5b`:
  `9b416d026183703db31d8f008272f6c1d4a7e181`.
- Exact 5292 pair is unchanged: fixture
  `af7407a5a2d42bb63b5cc11ba4a4924d3186c607`, test
  `5db819f485da679f613ef04455ec19708d316d6a`.
- Original f894 recipe pair is unchanged: `word_binding_recipe.py`
  `c980d9897657ea91f096486f19eb6f084b49a476`, and
  `test_word_binding_recipe.py`
  `510e2b691f6c47b36cfef9fcae01342f430e2a46`.
- Runtime is exactly `ad823e0a0f5be4a7acf1d3006df6f794709da63d`; tree:
  `33904550800ee3e2fa34fe0b13c26754b46c7fdc`.
- `runtime.lock.json` points to producer `34eac0041b0891e9011966b39bcbd26053fde5bc`;
  `artifact_manifest.py --check` reports current. The producer’s recorded
  official 34e all-15 mapping check also passed.
- The producer’s temporary worktree was absent, so the exact clean
  `/home/user/work/agent` checkout at the claimed HEAD was used for independent
  source and test verification. No source/test/fixture/recipe/generated/pin/
  package edits or deletions were made.

## Independent evidence

Exact mandated command, run once from this review worktree:

```sh
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ad823e0a PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-ad823e0a /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_native_word_anchor.py -k 'native_move_refuses_anchor_basis_until_explicit_clear or native_acceptance_refuses_review_source_counterexamples_before_writes or half_open_window_and_exact_rational_fps_are_validated_at_acceptance'
```

Result: `4 passed, 50 deselected in 4.14s`, exit `0`.

The four selected cases are the native move guard, the two parameterized
review-source counterexamples, and the half-open/exact-rational-FPS acceptance
case. The fixture registers `agent.create_runtime_commit_service()` and uses
the real Runtime `commit_timeline` route; production acceptance/preview remain
the provider `port.accept`/`port.preview` path.

Postchecks:

- `/home/user/work/venv-agent/bin/ruff check --no-cache tests/editing_conformance/native_word_anchor_fixture.py tests/editing_conformance/test_native_word_anchor.py` — PASS.
- `git diff --check` — PASS.
- Review worktree status — clean.
- Typecheck — N/A: this was an exact read-only review; no source changed.

The known stale-window failure and the two D14 equal-text undo failures remain
unchanged, unskipped, and visibly failing; they were not rerun per scope. No
repair or rerun was performed after the successful first targeted run.

## Blockers and next steps

No blocker. Record this as the scoped V4 actual-four PASS only. Preserve the
stale-window and D14 failures as separate follow-up work; do not broaden this
result into any excluded gate.
