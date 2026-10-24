**BLOCKED on legacy adoption; a reviewable recovery source packet is complete. No live cleanup occurred.**

The packet in `ops-bench-store-legacy/` contains copies of `bench_store.py`, `request-runtime`, and `dispatcher-daemon`, plus [source.patch](/home/user/work/wt/rt-OPS-bench-store-legacy-sol-2352/ops-bench-store-legacy/source.patch) and one finite stdlib fixture.

Its route is `request-runtime --recover-store` → `BENCHRECOVER` → the production `dispatch_request()` function → existing `Store.recover()`. It accepts no target, adoption, force, or custody-stamping arguments.

A private baseline probe found that installed recovery writes index and suite/env projections before refusing a corrupt victim marker. The packet moves the existing deletion-authority validation before those writes, retains directory descriptors through recovery, and repeats validation during deletion. Existing ownership rules, journal, mutex, leases, transactions, and recovery remain in use.

All inventory paths below are relative to `/home/user/work/`:

| Exact target | Current suite references | Finding |
|---|---:|---|
| `venv-agent-child-s2` | 7 | No tuple/owner markers; retained refusal says “candidate is referenced.” Provisioner dependency remains current. |
| `venv-agent-child-s2-c13` | 2 | Agent marker `0b2f662e32e1a6818d58f9cf12130f0a89fb5a3b`; Runtime/client markers absent. Retained refusal says tuple marker pair is incomplete. |
| `runtimes/agent-remotion` | 4 | Package/lock bytes match `cbd91c3bc8fca99256974e992c4f06f7d053bde7`; no Store custody. |
| `runtimes/agent-remotion-0013` | 6 | Package/lock bytes match `30da0a5e05d4529a2b97b3c1818cf9e15842d628`; current env/provision references remain. |
| `runtimes/agent-remotion-current` | 15 | Source marker and package/lock bytes match `7970544bb17dfcf234bd1cc1bb55ab5d713decd8`; current references remain. |
| `runtimes/agent-remotion-independent-review.partial.HIa4dVUW` | 0 | Failure metadata says `verify-installed`; no ownership or historical launch custody. |
| `runtimes/agent-remotion-independent-review.partial.6U6z45XJ` | 0 | Same finding; separate exact target. |

Both partials record Agent `f6116e1b658514021cbbf08d5a6f16a240523f1a`. None of the seven has `.bench-owner.json`; live `bench-store` is absent. Package-byte matches and failure receipts confer no deletion authority.

The bounded audit inspected 2,145 worker metadata files, six boards, 461 pending requests, and 1,593 retained test requests. No matching pending test request was found after joining current suite definitions. These metadata checks do **not** establish historical quiescence. Four checkout pins remain referenced but unavailable: `7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e`, `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, `95202c2b09e83aaae028287d6c59b773410141f3`, and `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414`.

Validation from the assigned worktree:

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python /home/user/work/wt/rt-OPS-bench-store-legacy-sol-2352/ops-bench-store-legacy/test_legacy.py` — **14 tests passed**.
- `/home/user/work/venv-agent/bin/ruff check --no-cache ops-bench-store-legacy/bench_store.py ops-bench-store-legacy/test_legacy.py` — **passed**; exact installed baseline comparison: **0 baseline findings, 0 new findings**.
- `bash -n ops-bench-store-legacy/request-runtime` and `bash -n ops-bench-store-legacy/dispatcher-daemon` — **passed**.
- In-memory compilation of both Python files — **passed**.
- Private baseline `patch --dry-run`, actual private apply, and `cmp` — **passed for all three source files**.
- `git diff --check` and individual packet whitespace checks — **passed**.

The fixture covers normal and explicit `env -i` requester/dispatcher execution, inherited leases after parent descriptor closure, interrupted creation/eviction recovery, marker and metadata substitution refusals, and protected-current preservation. Total retained fixture data was 7,234,985 bytes. Full adversarial race/permission acceptance and successful **legacy** provenance remain unqualified.

All six installed hashes still match the supplied baselines. Actual Runtime remains clean at `abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e`; C0v2/frozen schema sources are untouched. Live target root inodes/modes are unchanged. Ruff initially created an ignored local `.ruff_cache`; subsequent runs used `--no-cache`. No shared dependencies were modified.

Commit message and `BLOCKED` were written. Next step is independent Luna review. Installation requires separate approval and qualification; legacy action additionally requires a supported interface proving complete historical custody. No live retry, initialization, adoption, eviction, cleanup, or reclaimed-space claim was made.