## FAIL_SOURCE

Reviewed `tl/agt-F-inverse7-hash-0223` read-only. No worktree source changes; no commit requested.

Candidate pins are internally authentic but stale for upcoming MAIN:

| Source | Candidate | Current normal |
|---|---|---|
| Agent commit | `7c94e9d2…`, `commit.py=eec60c…`, `inverse.py=0702c…` | `bd3c95b1ce…`, `commit.py=eec60c…`, `inverse.py=06bd41f4…` |
| Runtime | `a3cd1a3214…`, auth=`4ac2b8…`, store=`633bc0…` | `6634a17f3f…`, auth=`4ac2b8…`, store=`2a6899…` |

`use_runtime()` only adjusts `sys.path`; already imported `runtime_protocol` modules remain first-import-wins. Therefore MAIN can preload Runtime `6634`, and strict `_assert_source_identity` will reject the stale `a3cd` store hash. The candidate cannot honestly qualify current MAIN.

All seven test predicates are preserved: five parameterized forward/undo/redo cases plus forged-source/step refusal and native ABA/no-write refusal. AST comparison found only the four custody assignments changed.

Checks:

- In-memory AST/compile: PASS
- Ruff baseline and candidate: PASS
- `git diff --check`: PASS
- Mypy baseline and candidate: both environment-blocked by the shared NumPy stub syntax error (`numpy/__init__.pyi:737`); no test-source error reached
- No pytest, collection, fixture/helper/function execution, service, build, browser, or render run

Bounded correction for the original author branch: update only the four stale literals to Agent `bd3c95b1ce…` / inverse hash `06bd41f4…`, and Runtime `6634a17f3f…` / store hash `2a68990b…`; retain existing `commit.py` and auth hashes. Then repeat protected review and perform the mandatory MAIN seven-case functional proof.