# D134 root-008 corrected evidence validation

Result: **CORRECTED_EVIDENCE**. Behavior status: **NOTRUN** by instruction. The retained original 2110/2111 artifacts were read and not modified.

## Identity and exact membership

- Agent `HEAD`: `96a6b2deea46eb33ba5184203a10e966cc5e9179`; base and head are identical.
- Owned files are byte-identical to their 96a6 blobs: `tests/editing_conformance/test_fork_abi1_binding_set.py` and `tests/editing_conformance/test_recipe_occurrence_fork.py`.
- The derivative `predicate-map.json` has all 18 authoritative root-008 node IDs with the full `tests/editing_conformance/` prefix and exact parameter spellings. No normalization is applied.
- Exact multiset comparison against `$ORCH/design/agt-F-D134-root-clusters-2022-root-clusters.json`: PASS, count 18, no omissions or extras.
- Frozen R4 candidate SDK: both owned test paths are absent; no frozen test blob was substituted.
- Runtime source was read from `/home/user/work/runtime` at head `cf0b82dd47452a7a34fc63eb233e9b1dc0532806`.

## Static commands and results

- `PYTHONPYCACHEPREFIX=/tmp/w-9af77265ee/pycache /usr/bin/python3.11` AST parse and compile of both owned files: **PASS**.
- `/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_fork_abi1_binding_set.py tests/editing_conformance/test_recipe_occurrence_fork.py`: **PASS**.
- `/home/user/work/venv-agent/bin/mypy --cache-dir=/tmp/w-9af77265ee/mypy tests/editing_conformance/test_fork_abi1_binding_set.py tests/editing_conformance/test_recipe_occurrence_fork.py`: **PASS**.
- JSON parse of all four derivative JSON files and exact root-008 multiset check: **PASS**.
- `git diff --check`: **PASS**.
- Outside-scope source/blob comparison: **PASS**; only the five evidence files are new, with no product, test, fixture, schema, generated, pin, Runtime, or shared-kernel changes.

## Not run by instruction

No pytest or collection, original18, replay, body, Runtime/service, socket, browser, full/family/core/profile/collector/build/install/acquisition suite, retry, alternate qualification, SWAP/WAL/recovery work, or D130-related tour was run. No raw payload, receipt, authentication material, private record, or retained historical record was collected or invented.
