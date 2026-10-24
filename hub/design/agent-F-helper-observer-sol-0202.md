Completed the diagnostic-only change in [helper-sequential-diagnostic-0149.py](/home/user/work/wt/agt-F-helper-observer-sol-0202/tools/helper-sequential-diagnostic-0149.py). Added cached code-identity filtering, bounded validator-field capture, atomic fsynced evidence writes, and offline selfchecks. Production, tests, guards, and pins remain unchanged.

The single original `[True]` run captured the real failure on Agent `415181d…` / Runtime `8ea0766f…`: Runtime rejected `(0, read, parent, [config, theme_overrides], batch-read)` at `timeline_commit_auth.py:2195`. That entry was absent from `expected_map` and had not been seen. Original and landing bindings both use physical reference `parent`; Runtime adds expected read keys only when physical references differ.

[Complete evidence packet](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-helper-observer-sol-0202/helper-sequential-diagnostic-0202.json): 4,879,737 bytes; SHA-256 `ea99da6e6340d74627a12ea351b4bfd49208b0af55a0ec69d152af656157546f`. Full capture/context/prepared inputs and validator locals survived. Digest matches; origins/body hashes unchanged; credential matches and observer errors empty; rejected-request database hashes identical.

Commands and results:

- Qualified environment: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-8ea0766f ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f ASTRID_RUNTIME_SOURCE_ROOT=/home/user/work/wt/rt-pin-8ea0766f`.
- `/home/user/work/venv-agent/bin/python tools/helper-sequential-diagnostic-0149.py --offline-probe` — passed serialization, interrupted-flush, exception-retention and credential checks; 10,000 unrelated calls added approximately 8 ms, with zero traced `Path.resolve()` calls.
- From `/home/user/work/agent`, `timeout 120 env <qualified environment> HELPER_SEQUENTIAL_EVIDENCE=<linked packet> /home/user/work/venv-agent/bin/python /home/user/work/wt/agt-F-helper-observer-sol-0202/tools/helper-sequential-diagnostic-0149.py` — **one attempt**, `1 failed in 15.85s`; original node, normal fixture, pytest timeout 45 seconds.
- `/home/user/work/venv-agent/bin/ruff check --no-cache tools/helper-sequential-diagnostic-0149.py` — passed.
- `ruff check --no-cache . --output-format json` — 2,147 existing findings, exact parent identities unchanged.
- Private-cache `/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid scripts/reshape --hide-error-context --no-color-output --no-pretty --show-error-codes` — 1,911 existing errors; output byte-identical to parent.
- `scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004`, `scripts/artifact_manifest.py --check`, and `git diff --check` — passed.

No blockers or additional test runs. Recommend a separately authorized repair aligning replay-carrier read entries with Runtime’s expected-map rule. Commit message and empty `DONE` marker written.