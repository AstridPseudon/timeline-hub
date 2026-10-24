## PASS — read-only integrated R5 proof

Base verified:

- Runtime `faf6a5477f9f6e4d96829046957518fef7a0dbed`
- Tree `5e909a876c780025c4b8aca10e42ff57cac092fd`
- `tl/integration` before: `2b49da8d6`; after: `faf6a5477`
- Parents: reviewed `2b49da8d6`, lint-reviewed `f8051e52b`
- Fixture blob matches `f805`: `c8d2e453…`
- Only fixture changed from `2b49`; product blobs unchanged.
- Authentication blob preserved: `9754e2d…`

Agent custody:

- Commit `9f2da582a6767030055e54092287d40f2b8f74bb`
- Tree `80c4f98ca5a57c19b99f9e729ef6963ac662c32b`
- Private read-only archive: `/tmp/w-5b72f0dd9c/agent-source-9f2`
- Imported module resolved from that archive; no overlay.

Test command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/tmp/w-5b72f0dd9c/agent-source-9f2 /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_legacy_occupancy.py
```

Result: `16 passed in 45.92s`.

All original 15 occupancy nodes passed:

- `test_legacy_publication_refuses_unrelated_destination_before_any_write[False-False]`
- `[False-True]`
- `[True-False]`
- `[True-True]`
- `test_exact_f1_over_http`
- `test_legacy_occupied_destination_without_shot_head_is_not_adopted[False]`
- `[True]`
- `test_legacy_current_closure_update_and_exact_retry_precede_live_checks`
- `test_legacy_current_destination_requires_verified_current_closure[receipt]`
- `[occurrence]`
- `[digest]`
- `[projection]`
- `[removed]`
- `test_legacy_historical_reuse_keeps_newer_global_shot_head[False]`
- `[True]`

The 16th passing node, `test_legacy_publication_route_is_directly_retired_without_write`, is newly added and receives no original-36 credit.

Accounting: original D43 `11 closed / 25 open`; after crediting the 15 original occupancy nodes: **26 closed / 10 open**. The 10 headless selectors remain open.

Checks:

- Ruff fixture: exit 0.
- `git diff --check`: passed.
- Worktree/head/tree stable and clean.
- No full suite, extra provider/HTTP/journey/benchmark/provisioning run, or product/test/Git edits.

Commit message and `DONE` marker written.