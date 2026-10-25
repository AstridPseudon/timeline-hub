# D139 final review validation

Result: **FAIL_SOURCE**. This was a source/protected review only. No live
Store/root, installation, child, cleanup, acquisition, provider, suite,
browser, or full-suite operation was performed.

## Canonical commands

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m unittest discover -s ops-d131 -p 'test*.py' -v` — PASS, 14 tests.
- `/home/user/work/venv-agent/bin/ruff check ops-d131/bench_store.py ops-d131/retire_entry.py ops-d131/test_retire_entry.py` — PASS, zero baseline diagnostics.
- `/home/user/work/venv-agent/bin/ruff check ops-d131/bench_store.py ops-d131/retire_entry.py ops-d131/test_retire_entry.py --ignore EXE002,BLE001` — PASS.
- `sh -n ops-d131/install-prep/check-cas.sh` — PASS.
- Private `/home/user/work/venv-agent/bin/python -B` `compile()` for `bench_store.py`, `retire_entry.py`, `test_reserve.py`, `test_retire_entry.py` — PASS, 4 files.
- `ops-d131/install-prep/check-cas.sh "$PWD" tl/rt-OPS-D131-kind-reserve-1558` — PASS; installed preimage SHA-256 `123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2`, mode `0755`, no installation.
- `git diff --check` — PASS.
- `git diff --check tl/rt-OPS-D131-kind-reserve-1558..HEAD` — PASS.
- `retire_entry.py --help` and `bench_store.py --help` — PASS; manager-facing route has no `--now` option.

## Private adversarial controls

- Caller future age claims and API/CLI clock override — REFUSED.
- Valid self-hashed activity rewrites for workers, queues, services, KEEP and
  ACTIVE — initial references REFUSED; erased references then **FAIL_OPEN**.
- Process after final scan — cwd, fd and cmdline each **FAIL_OPEN**; all had
  three scans and returned `retired`.
- Late KEEP after marker audit — **FAIL_OPEN**; marker was deleted.
- Late activity reference after lifecycle audit — **FAIL_OPEN**.
- Detached authorization path, inode/no-follow/hardlink and supplied
  pre-quarantine process controls — PASS in candidate tests/source review.
- Receipt malformed member/type matrix — all tested mutations REFUSED.
- Valid-shaped wrong receipt node/sequence/registration association —
  **FAIL_OPEN** by `_load()`.
- Old-format private fixture — REFUSED at `store owner schema` when
  `owner.activity`/`activity.json` are absent; REFUSED at `entry schema` when
  `registered_at`/`not_before` and registration `anchor`/age fields are
  absent.
- Three private child admissions — PASS, exactly two active entries remain.

The private controls used only temporary directories and were cleaned up by
their fixture lifetimes. No author test was changed or weakened.
