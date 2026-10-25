# Validation

## Required author commands

| Command | Result |
|---|---|
| `python3 ops-drop-staging/test_drop_staging.py` | PASS — 8 tests, 0 failures |
| `/home/user/work/venv-agent/bin/ruff check ops-drop-staging/drop_staging.py ops-drop-staging/test_drop_staging.py` | PASS — All checks passed |
| in-memory `compile()` for `drop_staging.py`, `drop-staging`, `test_drop_staging.py` | PASS — 3 files |
| `git diff --check HEAD^ HEAD` | PASS |

`bash -n` was not applicable to `ops-drop-staging/drop-staging`: it is a
Python launcher, and bash correctly rejected Python syntax; this is not
counted as a candidate failure.

## Independent private controls

All controls used only `tempfile.TemporaryDirectory` fixtures and the actual
`ops-drop-staging/drop-staging` caller (except the explicit preflight/execute
identity control). No repository tests or source were edited.

- `parent/{ACTIVE,active,LEASE,lease}/staging`: **incorrectly accepted** and
  removed under forced low-disk fallback.
- preflight old worker, replace pathname with another valid worker, execute
  old preflight: **incorrectly removed replacement target**.
- swap regular staging file to outside symlink at lstat/hash boundary:
  **incorrectly hashed outside bytes without refusal**.
- symlink `ORCH/managers` to external manager tree containing matching lease:
  **incorrectly accepted and removed target**.
- target-root marker controls: `KEEP` refused by incidental ancestor check;
  `ACTIVE`, `active`, `LEASE`, and `lease` accepted.
- hardlink from staging to evidence file: archive completed and evidence
  remained present; no positive destructive escape was observed, but link
  identity is not included in the listing record.

No full, browser, product, live socket, network, provider-body, child,
acquisition, install, or real-worker cleanup run was performed.
