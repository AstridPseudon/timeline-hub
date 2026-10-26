# OPS D141h interim Runtime CAS validation

Result: `PASS_INSTALL`.

## Immutable source and review gate

- `git rev-parse tl/rt-OPS-D141-cancel-finalize-sol-0410^{commit}` → `56f2d56e7d241d303be85df62166570d51602101`.
- `git rev-parse tl/rt-OPS-D141-cancel-finalize-sol-0410^{tree}` → `744cca68f672153dd84f7ba20e580b6e917ccf6d`.
- Author 0410 handoff and independent 0418 review were read from the absolute paths recorded in `source-manifest.json`; independent verdict was `PASS`.
- `git status --porcelain --untracked-files=all` → empty for the source worktree.

## Installer controls and CAS

- Reviewed Git blob `0921ec1c8eb7cab668203963c5a5eeb0e4616c00:ops-child-custody/install-prep/install_atomic.py` was materialized privately; SHA-256 `81eb0818809cccf52c95fb4a536f2c86f29ad47e8395a8d5a725b8c3fb560ef9`.
- Private source-only probe invoking that exact helper: `PASS` for wrong-preimage, no-clobber, destination symlink, and foreign-parent refusal.
- Final live preflight: exact `0be17b74ad1e324bc84e50e61e50e3e07390b262b7abe17a37ad22b9bd10d0fe` preimage, regular single-link 0755; four helpers absent including dangling symlinks; physical owned receiving directories; no live test-run/dispatcher/helper process.
- CAS sequence: own lock; four helper `copy_reserved` stages and readbacks first; exact predecessor backup with no-clobber; staged `test-run`; `rename_if_same` device/inode CAS and atomic rename; directory fsync; final readback.
- Installed target and all helpers matched the reviewed five-file manifest. Backup matched the exact preimage. Lock and replacement staging path are absent after success.

## Installed-byte validation commands

- Installed-bound candidate controls: `TMPDIR=/tmp/d141h-cas-0422 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 python3 -I /tmp/d141h-cas-0422/installed-smoke-source/privateops-d141-measured-floor/controls/real-controls.py` → `PASS`, exit 0, 49 isolated checks.
- Ordinary exact receiving smoke copied actual installed bytes through `/tmp/d141h-cas-0422/exact-layout/installed/bin` → `publishedbin` → `receivedbin`; all five hashes/modes matched and no controls sibling was received → `PASS`.
- `bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/test-run` → `PASS`.
- Python AST and JSON parse over installed helpers/control manifest → `PASS`, 5 files.
- `ruff check --no-cache` over installed Python helpers and the bound control script → `PASS`, all checks passed.
- `python3 -m json.tool .../install-manifest.json` → `PASS`.
- `git diff --check` → `PASS`.

The installed-bound controls ran synthetic subprocesses only in the isolated root; no live `TEST` request, dispatcher activation, service body, queue mutation, receipt attachment, product test, full suite, build, ZIP, or release occurred.

An initial disposable attempt to invoke the older D139 dry-run path was not runnable because this D141 source commit intentionally has no `ops-child-custody/` checkout path; it happened before any live write. The exact reviewed helper was then materialized and its dedicated private fail-closed probe passed. No alternate installer was used.
