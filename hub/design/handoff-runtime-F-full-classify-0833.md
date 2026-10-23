# Runtime F corrected full handoff

Corrected sole full result on Runtime commit `eb13b2051d4d30a4d8b7df8878bb7451701eab5a`, tree `5c307b9173aaccdb79697304bf5d5ac64a2487cc`; service `runtime-full-1023083244-8246`.

Command:

```text
env ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -n 3
```

Result: **FAIL** — `31 failed, 6162 passed, 26 skipped, 15 xfailed, 12 warnings, 45 errors in 400.65s (0:06:40)`, exit 1. The service captured Agent dependency commit `d462103985e3d4c4591ed76c5d5f261b2398fb36` (tree `eee66dc206817b16f0621087a12505389ec41630`). Complete node inventory and raw evidence are in [worker report](../workers/rt-F-full-classify-0833/report.md) and the durable service log.

Disposition:

- 29 FAIL nodes are a test-fixture compatibility gap from `fcdfb41ea4`: `tests/test_timeline_commit_port.py:111` rejects the two-command ABI-1 producer request. R2r test-fixture owner: scope the one-command bound to v2 metadata requests, preserve strict v2 shape checks, and accept all 29 FAIL + 45 setupERROR nodes.
- 45 setupERROR nodes are the same `PreparedProvider fixture supports one command only` exception in `tests/test_timeline_producer_record_boundary.py` parameter expansions: 19 forged metadata, 6 authority-only effects, 20 normalization values.
- `tests/test_shot_composition_runtime.py::test_stale_head_conflict_carries_machine_readable_reason_over_http` is Agent-origin: Agent `_commit_errors._details()` supplies `code`, `path`, `hint`, and `suggested_command` required by v2, while the Runtime test asserts the old exact five-key mapping. Hand back to Agent/test ownership; do not remove structured fields in Runtime.
- `tests/test_timeline_current_union_contract.py::test_public_python_union_types_and_nested_item_references_resolve` remains the known frozen `DocPatchArgs` package-root export gate, same bytes/cause as the reviewed R0 evidence; P1/freeze remains explicit. No new producer/schema/client fix.

No upstream-4563 classification, collection failure, Runtime product regression, or service-row edit. `git diff --check` passed; repository worktree remained clean. No second full suite was requested.
