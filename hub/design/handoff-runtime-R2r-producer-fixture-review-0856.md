# R2r producer-fixture compatibility review

Decision: **PASS**.

Reviewed candidate `014c0984853504d223cae1eb5f51b237421b49a` (`92e93956424e073c2d31c04c5f9937ea009c4800`), parent `eb13b2051d4d30a4d8b7df8878bb7451701eab5a` (`5c307b9173aaccdb79697304bf5d5ac64a2487cc`). The delta is exactly the permitted `tests/test_timeline_commit_port.py` change: four insertions and one deletion. No product, schema, client, config, skip, xfail, or assertion-relaxation change is present.

## Findings

- `_validate_prepared_request` now applies its one-command/one-step restriction only when `_v2_request` identifies v2 metadata (`label`, `steps`, `merge`, `reads`, or `doc.patch`). ABI-1 producer bodies remain API v1, rationale-only, and two-command; their existing `_candidate` specialization still replaces the fixture command record with the guard and authored command. The producer boundary, forged metadata, hidden effects, and normalization cases are unchanged.
- The malformed-shape guard fixture now explicitly includes `label`, so all 13 malformed shapes × both `prepared`/metadata entry points still exercise the strict v2 refusal path. Its `ClosurePort` proves refusal before head/closure facts; the 3 mutation cases × 2 dry-run modes retain the authenticated-step/no-write checks. `tests/test_timeline_commit_port.py -k prepared_fixture`: **32 passed, 35 deselected**.
- Repository-wide import audit found **26** modules importing this support module. The ABI-1 producer/checkpoint callers and all direct `prepared`/`_complete_v2_metadata` callers were inspected; no valid existing v2 multi-command specialization was found, and no helper caller was silently filtered.
- The prior full-classification review is consistent: the 29 FAIL + 45 setup ERROR nodes were the same fixture one-command exception, not Runtime product regressions. No v2 permissive fallback invents metadata or effects.

## Test evidence

Exact literal acceptance command requested by the brief:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_producer.py tests/test_timeline_producer_checkpoint.py tests/test_timeline_producer_guards.py tests/test_timeline_producer_record_boundary.py tests/test_timeline_commit_port.py tests/test_timeline_v2_request_store.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py .
```

Result: **exit 4 before collection** because `tests/test_timeline_v2_request_store.py` does not exist in this BASE. No PASS is claimed for that literal command.

Corrected existing-node command, same flags and scope with the absent path removed and existing history/authentication coverage included:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_port.py tests/test_timeline_history_boundaries.py tests/test_timeline_commit_producer.py tests/test_timeline_producer_checkpoint.py tests/test_timeline_producer_guards.py tests/test_timeline_producer_record_boundary.py tests/test_timeline_commit_authentication.py::test_valid_record_accepts_and_retry_or_preview_preserves_authoritative_steps tests/test_timeline_commit_authentication.py::test_forged_provider_records_are_rejected_without_writes tests/test_timeline_commit_authentication.py::test_read_claims_are_checked_at_input_and_in_dependency_union tests/test_timeline_commit_authentication.py::test_atomic_mode_requires_authoritative_scope_dependencies
```

Result: **296 passed in 55.40s**.

The central service ran the equivalent actual command with fixed service flags (`PYTHONPATH=$PWD:/home/user/work/agent`, `-p no:cacheprovider`, no literal `-o addopts=` because its file-argument validator rejected that option): **296 passed in 51.55s**, result `rt-R2r-producer-fixture-sol-0844-reference-fixture-agent-current-integration-1023084838-8658`, with exact-request collection matching **296/296** nodes. HTTP history ran only there. The service also confirmed all prior **74/74** non-PASS nodes were collected and passed.

Additional direct commands/results:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_authentication.py::test_valid_record_accepts_and_retry_or_preview_preserves_authoritative_steps tests/test_timeline_commit_authentication.py::test_forged_provider_records_are_rejected_without_writes tests/test_timeline_commit_authentication.py::test_read_claims_are_checked_at_input_and_in_dependency_union tests/test_timeline_commit_authentication.py::test_atomic_mode_requires_authoritative_scope_dependencies
```

Result: **36 passed in 7.64s**.

```text
mapfile -t NODES < /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-producer-fixture-sol-0844/previously-nonpass74.txt
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider "${NODES[@]}"
```

Result: **74 passed in 15.46s**.

The full suite was not run.

## Structural checks

- Original test ASTs: **33/33 unchanged** against the pre-R2r fixture parent (29 port, 4 history).
- Frozen paths: **77/77 byte-identical** to the candidate parent.
- `py_compile` for `tests/test_timeline_commit_port.py` and `tests/test_timeline_history_boundaries.py`: PASS.
- `git diff --check`: PASS; worktree clean.
- Scoped Ruff: parent/current **4/4**, added diagnostic identities **0**.
- Scoped Pyright: parent/current **43/43**, added diagnostic identities **0**; comparison uses path, rule, message, and unchanged source line, so line shifts do not create false deltas.

No blockers beyond the absent literal test path and the intentionally unrun full suite. No files were deleted or modified by this review.
