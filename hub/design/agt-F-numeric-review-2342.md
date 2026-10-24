## PASS_SOURCE

Reviewed `tl/agt-F-numeric-revision-2328`:

- One author commit only; only the assigned test file changed.
- Added import registers the genuine `selected_runtime_env` fixture used by `retained_pack`.
- Runtime path remains `commit_timeline` with the registered provider; no synthetic history, SQL, detached authority, or assertion weakening.
- All 9 selectors preserved: 6 numeric and 3 guard cases. Function ASTs, decorators, arguments, bodies, assertions, and `pytest.raises` sites are identical.

Checks passed:

- In-memory baseline/candidate compile
- Ruff baseline/candidate
- Mypy baseline/candidate
- `git diff --check`

Hashes:

- Baseline: `20f350633c5522437c657b86e0ccc434b6cf486ee94248401d072acd771f7297`
- Candidate: `d715740334878c67d39af14263bc9e14e67c3124fb8d71706616ddac180f41c6`
- `/home/user/work/agent` integration blob: same candidate hash

The author merge is already an ancestor of integration (`3edc45cb26`); no duplicate merge requested. Functional proof remains pending the single later batched rerun. No product tests or service runs were performed.