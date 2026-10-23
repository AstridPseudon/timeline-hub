# AP2 P1/D12 scoped re-credit handoff

## Result

PASS on exact Agent base `9729c07b764ba6cce1bb31686cb93d29fc72b14d`.

The original P1 corpus positives were run against the production
`create_runtime_commit_service().commit` provider: `params-absent-to-explicit-values`,
`params-null-to-object`, `params-remove-and-preserve-opaque`, and
`disjoint-field-merge`. The smallest existing D12 negative selector was also
run for `create`, `modify`, and `invalidate-by-target-change`.

Exact command/result:

```text
PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
PYTHONDONTWRITEBYTECODE=1 timeout 45s /home/user/work/venv-app2-native/bin/python \
-m pytest -q -p no:cacheprovider --tb=short \
tests/sdk/test_p1_doc_patch_provider.py::test_child_vectors_use_runtime_commit_service_and_preserve_shared_alias \
tests/sdk/test_p1_doc_patch_provider.py::test_disjoint_child_merge_executes_through_service_on_complete_closure \
tests/sdk/test_p1_doc_patch_provider.py::test_new_or_invalidated_legacy_timing_is_422_and_atomic

7 passed, 1 warning in 1.37s
```

The warning is the shared environment's unknown pytest `timeout` option.
Scoped Ruff passed, private mypy passed, and `git diff --check` was clean.

## Provenance and caller

The four source vectors remain unchanged and hash-match the manifest:

- `recipe_m2_scalar_params_absent.json` —
  `9687956ee3850c5d873580a28cd6e8354f0b76dcb9a17bf56eb6ae0213f24b36`
- `recipe_m2_scalar_params_null.json` —
  `15e945496b805af2554d78777be4585aa684615de575960352376f1dd4eaba74`
- `recipe_m2_scalar_params_object.json` —
  `ae9f96e55432d0cf892f6045285e56265c6adc66058caf146bf4a7d7b1869638`
- `recipe_m2_scalar_disjoint.json` —
  `0aab88bff6040ad741771fe8ed2198c141347970420ede78a981ba1416f6e866`

Their original `clip.set-params` bindings/reads are retained; no timing
binding was invented and no declaration was removed. The production caller
is `commit.py:1114` → `validation.py:441` → timing validation.

The run re-confirms accepted canonical output, disjoint merged/rebased
canonical/head/receipt behavior, and atomic invalid refusal with unchanged
head/history. Full-v2 base pair/scope/commands/label/steps patch+reads,
merge/reads, dry-run/key, complete applicable digest/receipt/steps/deps/history
and conflict/invalid envelope fields remain unchanged from the reviewed base;
this narrow corpus run does not fabricate or newly claim route/wire coverage.

The prior V2 home proof's 144-test result and exact `89c700a…` direct-P1/V2
blobs remain applicable. The unrelated first-parent `ccc521b78` ancestry is
still separately unqualified. No whole-home/P1GO, HTTP, browser, full-suite,
build, or Runtime-wire claim is made.

No product/test/fixture/generated/pin changes were made. The local detailed
record is `report.md` in the assigned worktree.
