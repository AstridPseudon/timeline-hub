## Report — `agt-R2-captured-whole-path-1112`

### Source-cause: PASS

The retained captured fixture is faithful, not a setup seam:

- Capture literal hash matches its fixture assertion: `9a47bb...ade589` (`tests/editing_conformance/test_captured_nested_redo.py:22-30`).
- `replay()` reconstructs the retained SQLite history, compiles documents with `bundle_from_document`, and resolves authenticated boundaries/history (`:34-57`).
- The failing chain is:
  - current publication `txn-75285...`, revision `document-diff-...`;
  - accepted historical source `txn-7d039...`, revision `authoring-parent-...`;
  - restored nested root `selected-shot`, whose authenticated source mapping exists only in the accepted boundary.
- The retained trace shows `source null` for the current restored state, while the accepted boundary provides `selected-shot` with revision `authoring-shot-revision-e568...` and `item_id_map: {}`.

The concrete defect is in `inverse.py:123-129`: `_input_read_state()` requires the entire recorded root value to equal the post-stage state. The later inverse stage removes `params.text`, so the authenticated `shot:selected-shot` root is validly restored but no longer byte-equal. The source codec is therefore not installed, and `_command_state.py:296-304` raises `shot item source changed`.

The production caller is connected: `commit.py:1045-1067` loads authenticated boundaries, `commands.py:265-268` invokes `apply_inverse`, and `inverse.py:1094` performs the failing stage validation.

### Product behavior: FAIL / unqualified

Retained current11 XML:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/workers/agt-R2-full9758-review-1105/evidence/current11.xml`

SHA-256: `7f59c1b4dea3811518d177c2e985810eadfb624f28487c79517a448467ccc00d`

Result: 11 tests, 10 passed, 1 failed.

Failure:

```text
tests/editing_conformance/test_captured_nested_redo.py:
test_captured_nested_redo_compiles_and_partitions_without_rewriting_source
```

Trace: `inverse.py:882 -> _command_state.py:304`, `identity_conflict: shot item source changed`.

The ten nested recreation/forgery controls pass. Existing captured fork and real source-copy paths pass in their retained receipts, so this is specific to the nested historical stage transition.

Retained test command was:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-becfe6db" \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-becfe6db \
/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -pno:cacheprovider \
--timeout=45 --tb=short \
--junitxml="$ORCH/workers/agt-R2-full9758-review-1105/evidence/current11.xml" \
tests/editing_conformance/test_captured_nested_redo.py::test_captured_nested_redo_compiles_and_partitions_without_rewriting_source \
tests/editing_conformance/test_inverse_owner_occurrence_order.py::test_nested_delete_recreation_keeps_exact_stage_order \
tests/editing_conformance/test_inverse_owner_occurrence_order.py::test_nested_occurrence_partition_forgery_refuses_without_writes
```

### Supported correction

Sol1112 should make the historical codec lookup stage-aware: authenticate the exact restored root through its accepted `inverse.stage`/root-write boundary, then use that boundary’s source mapping and runtime document. Do not require full post-stage payload equality, and retain all source, owner, pin, order, range, history, and ABA guards. No caller map or equal-bytes authority is supported.

No code, tests, fixtures, or evidence were changed. Worktree remains clean; `git diff --check` passed. No full/gate suite was run.