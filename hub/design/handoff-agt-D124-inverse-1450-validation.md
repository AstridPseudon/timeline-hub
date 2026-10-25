# D124 R2 validation

Agent parent a4e016b6a9f91fbe372672bdcf382c630bf59186/tree60d45288145414ee4702fcce61af7c7810c2a3df. Product sources unchanged. Exact Runtime5e9ad1c6f74241d8771d3284fdd2ce7a214fd344/treede2954a0ceadb4455903d9abdfec3b773318a50f was clean before and after tests. Initial and final import checks resolve Agent modules from this worktree and Runtime service/auth from that pin. Shared venv and projection package paths supply dependencies only.

All commands below run from /home/user/work/wt/agt-D124-inverse-alias-sol-1435. TMPDIR is the harness-owned /tmp/w-a83a9a60b8; raw logs/XML and temporary fixture realms stay there. The only worktree addition is tests/sdk/test_d124_grouped_inverse_boundary.py.

## Final focused regression

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-D124-inverse-alias-sol-1435:/home/user/work/wt/rt-pin-5e9ad1c6:/home/user/work/agent-runtime-projection-0856/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short --basetemp="$TMPDIR/new-inverse-custody" --junitxml="$TMPDIR/new-inverse-custody.xml" tests/sdk/test_d124_grouped_inverse_boundary.py > "$TMPDIR/new-inverse-custody.log" 2>&1
```

Exit1: **2 passed,1 failed in3.87s**. Source custody and ungrouped inverse comparison PASS. Grouped inverse FAIL at ordinary undo submission with `provider occurrence alias is outside its boundary`. Its exact output/redo assertions are unreached. This is parent-product RED, no product change and no newGREEN claim.

Earlier authoring iterations on this same new test file:

- Same command, basetemp/new-inverse, XML new-inverse.xml, log new-inverse.log: **1 passed,2 failed in4.01s**, exit1. Besides the intended grouped failure, the initial new comparator incorrectly tried undoing a birth after a later child consumer and its inverse. C0's later-history guard correctly refused that request; no original test or production behavior was changed. The new comparator was corrected to undo/redo birth before authoring the child edit, then separately undo the child edit with exact boundary equality.
- Same command, basetemp/new-inverse-final, XML new-inverse-final.xml, log new-inverse-final.log: **2 passed,1 failed in4.00s**, exit1. Later source-only assertions added exact native previous/after values and both physical root effects/pins/owners; final run is above.

## Strict existing controls

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-D124-inverse-alias-sol-1435:/home/user/work/wt/rt-pin-5e9ad1c6:/home/user/work/agent-runtime-projection-0856/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short --basetemp="$TMPDIR/strict-controls" --junitxml="$TMPDIR/strict-controls.xml" tests/sdk/test_timeline_inverse_fork_guard.py::test_fork_materializations_require_complete_unique_authenticated_edges tests/sdk/test_timeline_inverse_fork_guard.py::test_equal_payload_sibling_cannot_supply_fork_source_authority tests/editing_conformance/test_doc_patch_v2.py::test_ambiguous_entity_alias_refuses_and_qualified_revision_selects_one tests/editing_conformance/test_step_undo_v2.py::test_aba_tail_refuses_even_when_the_current_guard_matches > "$TMPDIR/strict-controls.log" 2>&1
```

Exit0: **20 passed in7.03s**. These cover17 materialization tamper cases, equal sibling/wrong owner authority, ambiguous aliases and ABA. They use their existing DetachedRealm/runtime_abi fixtures, so they are scoped producer-guard evidence, not original Runtime acceptance results. They preceded the final added source-custody assertions; no product or control source changed afterward.

## Static checks on final test source

```bash
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR="$TMPDIR/ruff-cache" /home/user/work/venv-agent/bin/python -m ruff check tests/sdk/test_d124_grouped_inverse_boundary.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-typecheck-v2/bin/python - <<'PY'
import os, py_compile, sys
from pathlib import Path
assert sys.version_info[:2] == (3, 11), sys.version
py_compile.compile('tests/sdk/test_d124_grouped_inverse_boundary.py', cfile=str(Path(os.environ['TMPDIR']) / 'grouped-inverse-final.pyc'), doraise=True)
print('Python 3.11 compile PASS')
PY
git diff --check
```

All exit0. Ruff and an earlier Python3.11 compile also passed before the final source-custody assertions; the commands above verified the final file. Product Ruff2143/mypy1902 baseline comparisons were not requested/run because there are no product changes. No full/core suite was requested.

## Limits

Initial available disk4,686,970,880 bytes; before first tiny run4,686,196,736; before final tiny run4,617,977,856; after final run4,617,261,056. All observed values exceed the4.6GB source-only start floor and4.0GB stop line. No heavy body, install, build, service/socket, archive, fixture acquisition, unchanged-original retry, originalFalse/numeric/recipes, native5, TEN/95/P4/core/full, profile, release or adoption. No regular5GB admission and no meaningful Agent product correction, so originalTrue was not run and there was no floor wait. Scratch measured3.4MB after final focused tests. No exact original stage/physical pairs were invented.

Independent final source/security review completed read-only via final_review_retry; no blocker in the test, Runtime-owned root confirmed, no tests run by reviewer. Initial full-context review dispatch failed before creating an agent; the context-free retry succeeded. Farm core is downstream once per batch after the owning product correction.
