## F-D52-core-five qualification report

Compared the retained five-node result with Agent commit `4e7f822ec607b163535acc2c4e478907c55f12d2` using read-only `git show`. No product, test, generated, schema, fixture, registry, or source files were changed.

### Retained five-node mapping

| Node | Result | Parameter | Preserved source/body hashes |
|---|---|---|---|
| `test_captured_config_root_mirror.py::test_captured_config_root_rejects_tampering_without_mutation[native-order]` | PASS | `native-order` | source `526c2cf2…fe559f`; body `859e238a…f07007` |
| `test_nested_config_root_history.py::test_root_config_history_rejects_tampering_without_mutation[native-order]` | PASS | `native-order` | source `bfb72c87…976374`; body `49cc7062…b604a1` |
| `test_occurrence_fork_source_baseline.py::test_retained_app_fork_reload_undo_restores_exact_closure` | PASS | none | source `cd921e3f…f3c9ad0`; body `cc16d7a6…7af085` |
| `test_timeline_inverse_fork_guard.py::test_fork_output_guard_allows_independent_parent_edit_and_preview_redo` | FAIL | none | source `83028710…a93c6`; body `43d9a97c…988180` |
| `test_timeline_inverse_fork_guard.py::test_valid_fork_history_distinguishes_output_consumers_from_retained_sibling[retained-sibling]` | FAIL | `retained-sibling` | source `83028710…a93c6`; body `ad8f28a0…53f51` |

No separate parameter-hash receipt exists in the retained packet; the exact parameter strings above are preserved. I did not invent hashes.

The shared physical fixture identity is:

- `shot-shared` / `shot-rev-1` → `internal-1`
- retained by `f2-occurrence` and `shared-sibling`
- project `project-1`; timelines `film` and `main`

### New-source relevance

Commit `4e7f822e` changes only:

- `astrid/sdk/timeline/_commit_patch.py`
- `astrid/sdk/timeline/_step_undo.py`
- adds `tests/editing_conformance/test_redo_retained_boundaries.py`

The original five tests are unchanged from the retained base.

Both retained failures map directly to the `_commit_patch.py` materialization-site hunk. It permits reuse only when:

- the old and new sides contain the exact same physical reference,
- the payload is equal,
- no root-write effect exists for that reference.

That matches the observed failure: `pins=[]`, unchanged `shot-revision:shot-rev-1`, and no after-side root effect. Strict validation remains for changed roots and mismatched or forged pins.

The `_step_undo.py` hunk reconstructs ancestor configuration inputs and is relevant to broader redo coverage, but not directly to either retained failure.

The new retained-boundary tests are relevant source coverage, but the commit’s claimed pass count is author evidence only. It is not independent acceptance or PASS credit for the retained five. Agent1234’s later custody changes and 336-pass result are a separate source and were not conflated.

### Custody limits

The retained evidence shows:

- publication 1 records authenticated `commit.materialization` custody;
- publication 3’s inverse stage has no after-side `commit.effect` for the retained shared source;
- the observed `pins=[]` is therefore a custody-boundary gap, not proof that the source is unauthenticated.

The new hunk narrowly permits exact retained physical reuse without a root-write effect. It does not prove propagation of prior materialization custody into the later inverse stage, nor does it establish HTTP, wire, installed-package, browser, or security-audit behavior.

### Missing durable receipt

Normalhub flat paths were checked. The following remain unpublished:

- `design/agt-R2-removal-redo-sol-1210.md`
- the named author XML receipt for `agt-R2-removal-redo-sol-1210`

The local Agent commit exists and was inspected, but no XML/report was reconstructed. Independent review `agt-R2-redo-security-review-1234` remains separate and is not credited.

### Verification

Retained worker command/result:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
[the five retained selectors] --junitxml=evidence/assigned.xml
```

Result: `3 passed, 2 failed, 0 errors, 0 skipped` in 4.246s. The two failures were the retained inverse-stage image mismatch. Not rerun here.

- `git diff --check`: PASS
- worktree status: clean
- Ruff/typecheck: N/A; read-only qualification
- No full suite, HTTP, browser, live-socket, or security audit run

Required commit message and empty `DONE` marker were created.