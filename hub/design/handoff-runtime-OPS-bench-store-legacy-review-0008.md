## Verdict

- Recovery source packet: **PASS, bounded source qualification only.**
- Legacy cleanup/adoption readiness: **FAIL/BLOCKED. Do not mark DONE.**

## Evidence

Reviewed commit `d0324cde63543f065eceb2829539a50469c33869`, parent Runtime `abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e`.

The packet:

- Adds only `--recover-store` → exact `BENCHRECOVER` → production `dispatch_request()` → `Store.recover()`.
- Adds no target, adoption, force, cutover, liveness waiver, or custody-stamping input.
- Preflights deletion authority before projection/index writes and retains existing mutex, journal, flock, lease, and transaction controls.
- Preserves existing request shapes.

Independent checks:

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python ops-bench-store-legacy/test_legacy.py` — **14 passed**.
- `/home/user/work/venv-agent/bin/ruff check --no-cache ops-bench-store-legacy/bench_store.py ops-bench-store-legacy/test_legacy.py` — **PASS**.
- In-memory Python compilation — **PASS, 2 files**.
- `bash -n ops-bench-store-legacy/request-runtime ops-bench-store-legacy/dispatcher-daemon` — **PASS**.
- Private baseline `patch --dry-run`, apply, and `cmp` — **PASS, 3 files**.
- `git diff --check` — **PASS**.
- Pyright 1.1.414: candidate and exact baseline each have the same one pre-existing diagnostic; **zero new diagnostic identities**.

No live install, queue, store, process, target, permission, or cleanup action occurred. Worktree is clean.

## Limits/findings

The fixture proves normal and `env -i` requester/dispatcher routing, refusal/no-write controls, interrupted recovery, lease inheritance, marker/link/path substitutions, and protected-current preservation.

Race/permission acceptance remains unqualified: recovery holds descriptors during preflight, but `_roll()`/`_delete_owned()` do not consume them; final deletion still uses path-based checks and `path.rmdir()`. Concurrent directory replacement, queue-directory substitution, and permission changes are not proven fail-closed. This is an acceptance limitation, not a reason to weaken guards.

Installed baseline hashes matched the recorded kit, including:

- `bench_store.py`: `6d936820…`
- `request-runtime`: `471fd470…`
- `dispatcher-daemon`: `f18bc20b…`

## Legacy readiness

All seven named targets exist but have no `.bench-owner.json`; `/home/user/work/bench-store` is absent. Five remain referenced by active suite/configuration sources. The two partial runtimes contain only `verify-installed` failure metadata and do not establish historical launch custody. Missing current metadata does not prove universal historical absence.

The four unavailable referenced pins remain unchanged:

`7d1cfa6b…`, `a0dca169…`, `95202c2b…`, `f8da4b6d…`.

Next evidence must come through the existing dispatcher-managed Store lifecycle (`request-retire-venv`/`retire-child-venv` for child environments and the existing `request-runtime`/`make-runtime` lifecycle for runtimes), with an authoritative journal/entry/lease custody chain and guarded current-reference resolution. No bypass, new marker, proc-liveness waiver, or manual cleanup is justified.