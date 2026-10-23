# P1/D12 scoped re-credit

## Verdict

PASS for the requested read-only P1/D12 final-validation slice on Agent base
`9729c07b764ba6cce1bb31686cb93d29fc72b14d`. The worktree had no product or
fixture delta. Only the requested reports are task output; no tests, generated files,
pins, or production code were changed.

## Original corpus and provider

The four original positives are the vectors in
`tests/sdk/fixtures/p1_feasibility/doc_patch_requests.json`, backed by these
unchanged source vectors:

| P1 vector | Original source | SHA-256 |
|---|---|---|
| `params-absent-to-explicit-values` | `tests/editing_conformance/fixtures/recipe_m2_scalar_params_absent.json` | `9687956ee3850c5d873580a28cd6e8354f0b76dcb9a17bf56eb6ae0213f24b36` |
| `params-null-to-object` | `tests/editing_conformance/fixtures/recipe_m2_scalar_params_null.json` | `15e945496b805af2554d78777be4585aa684615de575960352376f1dd4eaba74` |
| `params-remove-and-preserve-opaque` | `tests/editing_conformance/fixtures/recipe_m2_scalar_params_object.json` | `ae9f96e55432d0cf892f6045285e56265c6adc66058caf146bf4a7d7b1869638` |
| `disjoint-field-merge` | `tests/editing_conformance/fixtures/recipe_m2_scalar_disjoint.json` | `0aab88bff6040ad741771fe8ed2198c141347970420ede78a981ba1416f6e866` |

Each source vector remains the original `clip.set-params` command with only
the recorded `scalar.owner`/`scalar.target` bindings and its original reads;
there are no added timing declarations or removed declarations. The source
vector file itself also remains byte-identical to the base.

The test helper calls the production `create_runtime_commit_service().commit`
through the detached Runtime ABI port. The mounted validation caller is
`astrid/sdk/timeline/commit.py:1114` →
`astrid/sdk/timeline/validation.py:441` → `validate_candidate_timing`.

## Exact evidence

```text
PYTHONPATH="$PWD:/home/user/work/runtime" \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
PYTHONDONTWRITEBYTECODE=1 timeout 45s \
/home/user/work/venv-app2-native/bin/python -m pytest -q -p no:cacheprovider --tb=short \
tests/sdk/test_p1_doc_patch_provider.py::test_child_vectors_use_runtime_commit_service_and_preserve_shared_alias \
tests/sdk/test_p1_doc_patch_provider.py::test_disjoint_child_merge_executes_through_service_on_complete_closure \
tests/sdk/test_p1_doc_patch_provider.py::test_new_or_invalidated_legacy_timing_is_422_and_atomic

7 passed, 1 warning in 1.37s
```

The seven tests are exactly four positives (three accepted parameter vectors
and one disjoint rebase) plus the three existing D12 negatives:
`create`, `modify`, and `invalidate-by-target-change`. The warning is the
shared environment's unknown pytest `timeout` configuration option.

Additional checks:

```text
/root/.local/bin/ruff check tests/sdk/test_p1_doc_patch_provider.py
All checks passed!

MYPY_CACHE_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P1-D12-recredit-0504/mypy-cache \
/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p1_doc_patch_provider.py
Success: no issues found in 1 source file

git diff --check
clean
```

Results exercised by the slice are: accepted canonical documents and exact
opaque/shared-alias preservation; a disjoint `fields` rebase retaining both
`params.x` and the intervening `params.y`, with the rebased receipt/head
relation; and atomic 422 `invalid_document` refusal with unchanged head and
history entry count.

## Full-v2 and qualification boundary

The v2 request/reply surface remains unchanged from the reviewed base:
base pair and scope, commands, label, step patch/reads, merge/reads,
dry-run, idempotency key, canonical/head and digest fields, receipt, steps,
dependencies, history, and structured conflict/invalid fields. This narrow
re-credit does not fabricate those envelope fields in the original corpus
vectors or newly claim route/wire coverage; it reuses the existing reviewed
provider assertions. The recorded R2/R3 evidence remains the source for the
broader envelope fields, while this run newly re-confirms the requested
provider positives and D12 negatives on the exact V2 home base.

The reviewed V2 home proof remains applicable: 144 targeted tests, with
`89c700aded947a4c498043e0f1a46b4ab3e0a873` direct-P1/V2 blobs and mounted
caller proof. The unrelated first-parent `ccc521b78` ancestry remains
separately unqualified; no whole-home, whole-P1GO, HTTP, browser, full-suite,
or Runtime-wire qualification is claimed here.

## Decisions and limits

- The named `/home/user/work/venv-agent/bin/python` was not installed in this
  environment. The same shared dependency set available at
  `/home/user/work/venv-app2-native/bin/python` was used; the initial missing-
  interpreter attempt failed before pytest and ran no tests.
- No full, browser, HTTP, live-socket, build, generated-file, or new-test run
  was performed, as required.
