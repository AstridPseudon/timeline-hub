# WC8 size current-preserving Agent packet

Result: one three-blob Agent merge packet for approved retained `size` support and the actual `a52331e3aedea0c2c470aea3ed663574990d29f8` proof.

## Exact ancestry

- HOME/base: `hub/timeline/agent/tl/integration` at `7c9ef2ed5e70da1a13e89278496c74321453955a`.
- Common candidate ancestor: `45729a6be200e48fbe6d92d5be58d09dd3dd3dca`.
- Supplied merge parent: `a52331e3aedea0c2c470aea3ed663574990d29f8`, whose parent is approved size commit `4542b759c7cdc9074260d8f6d0f193a7147f72a1`.
- Current packet tree: uncommitted changes on HOME; the harness must create the two-parent commit with first parent `7c9ef2ed5e70da1a13e89278496c74321453955a` and supplied merge parent `a52331e3aedea0c2c470aea3ed663574990d29f8`.

## Exactly three changed blobs

The working blobs exactly equal the corresponding blobs in `a52331e...`:

| Path | Blob |
| --- | --- |
| `astrid/sdk/timeline_sheet.py` | `8d198be5a51aa7b92f162b5c436eb1c66d84af15` |
| `tests/sdk/test_timeline_sheet_native.py` | `c7d08b99427ad9ea92ec0db78d683b561b47261f` |
| `tests/editing_conformance/test_native_sheet_ordinary_runtime.py` | `10c481eaca1cd86d5129f5b6f943d8271ac0b839` |

The brief called the third path `tests/sdk/test_native_sheet_ordinary_runtime.py`; the repository’s actual path is `tests/editing_conformance/test_native_sheet_ordinary_runtime.py`, and that is the path carried. No other blob changed. `git diff --quiet -- .` with these three paths excluded returned 0, and the complete status check found no outside or untracked changes. No Runtime, schema, generated, pin, store, or fixture-authority file was touched.

## Focused evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sheet_native.py::test_detached_static_size_uses_retained_native_params_command tests/sdk/test_timeline_sheet_native.py::test_detached_size_preserves_neighbor_presence_and_order tests/sdk/test_timeline_sheet_native.py::test_detached_size_reloads_rebases_and_undoes_through_native_session tests/sdk/test_timeline_sheet_native.py::test_detached_mixed_edit_with_unsupported_neighbor_is_not_staged` — **5 passed in 1.58s**.
- `git diff --check` — **PASS**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest --collect-only -q -p no:cacheprovider -o addopts='' -m integration tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_current014_detached_size_clear_uses_one_native_http_commit_and_guarded_inverse` — **1 test collected** (`[detached-historical]`). The default invocation deselected it because the file is marked `integration`; no HTTP test was executed.

The prior central proof is evidence for its exact tested tree only: `rt-m2-wc8-size454-one-actual-proof-0743-rt-wc8-current14-integration-1021074723-46`, **1 passed in 4.27s**. It is not a rerun or relabelled qualification of this current packet. Its report records two early executions failing only on over-specific retained-vs-rendered banner and canonical parameter-order assertions; those assertions were corrected before the sole qualifying run. No original old-test assertion was deleted.

## Live caller and limits

The only live production size bridge is the retained path `apply_sheet` → `_stage_sheet` / `NativeSheet` session → `_duration_sheet` → existing `clip.set-params` capture. The direct tests prove numeric size, explicit clear, presence/order/opaque preservation, disjoint rebase, inverse, and atomic unsupported-neighbor refusal. No actual HTTP replay, full suite, browser, renderer, install, or native run was performed for this current-preserving packet. WC8 remains open; the manager should perform the exact merge-parent check before submission.
