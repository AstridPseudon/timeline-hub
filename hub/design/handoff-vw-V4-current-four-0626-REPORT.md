# V4 actual four-case scoped proof

## Result

PASS: the mandated original four cases passed on the actual integrated Agent
HEAD after the reviewed boundary repair.

Exact command, run once:

```sh
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ad823e0a PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-ad823e0a /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_native_word_anchor.py -k 'native_move_refuses_anchor_basis_until_explicit_clear or native_acceptance_refuses_review_source_counterexamples_before_writes or half_open_window_and_exact_rational_fps_are_validated_at_acceptance'
```

Result: `4 passed, 50 deselected in 4.29s`; exit `0`. The four selected
cases are the native move guard, the two parameterized review-source
counterexamples (`short-occurrence` and `raw-source-window`), and the
half-open/exact-rational-FPS acceptance case. Full first output and exit are
preserved in `actual4-command.log`.

## Preflight identities

- Agent HEAD: `3e4261e9694c7bd7c1b5fada9bf01d91007bcc80`; tree
  `fbaebb606643a38391dbaf7f4a584bef390048af`.
- Reviewed boundary repair `b42b7d72a65cab305a4b953093963019aabc70b9` is an
  ancestor of HEAD.
- Approved 5292 test pair is exact: fixture blob
  `af7407a5a2d42bb63b5cc11ba4a4924d3186c607`; test blob
  `5db819f485da679f613ef04455ec19708d316d6a`.
- Original f894 recipe blobs are unchanged for
  `word_binding_recipe.py` (`c980d9897657ea91f096486f19eb6f084b49a476`) and
  `test_word_binding_recipe.py` (`510e2b691f6c47b36cfef9fcae01342f430e2a46`).
- G234 review ancestry is present. Current landing metadata retains the exact
  c793 `rebase.py` blob `9b416d026183703db31d8f008272f6c1d4a7e181`; current
  `commit.py` and provider-test blobs are the later integrated composites.
- Runtime is exactly `ad823e0a0f5be4a7acf1d3006df6f794709da63d`, tree
  `33904550800ee3e2fa34fe0b13c26754b46c7fdc`.
- Official client source `34eac0041b0891e9011966b39bcbd26053fde5bc` was
  checked read-only: vendor lock reported `ok runtime.lock.json (matches
  producer manifest)` for all 15 mappings, and `artifact_manifest.py --check`
  reported `artifacts.json is current`.

The fixture uses `agent.create_runtime_commit_service()` and the real Runtime
`commit_timeline` route; production acceptance/preview calls remain the
provider's `port.accept`/`port.preview` path. No mock or alternate executor was
used.

## Checks and scope

- `/home/user/work/venv-agent/bin/ruff check --no-cache tests/editing_conformance/native_word_anchor_fixture.py tests/editing_conformance/test_native_word_anchor.py` — PASS.
- `git diff --check` — PASS.
- Worktree status — clean; no product, test, fixture, recipe, generated, pin,
  package, assertion, or deletion changes were made.
- Typecheck — N/A: this was a read-only proof over the exact reviewed files;
  no source was changed.

The stale-window case is an independently known failure pending scope0549 /
Agent0607 and was intentionally not rerun. The two D14 equal-text undo cases
remain unchanged, unskipped, and visibly failing. No 5-case, 52-case, 54-case,
native14, full, browser, or V4-DONE claim is made. Later original-54 proof
remains separate.

## Durable logs

- `actual4-command.log` — exact mandated command, complete output, and exit.
- `postcheck.log` — scoped Ruff, diff check, and clean status.
- `provenance-check.log` — official 34e vendor-lock and artifact checks.
