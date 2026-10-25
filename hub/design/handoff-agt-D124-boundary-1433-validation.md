# D124 validation — Runtime-owned source fact, no semantic patch

Agent base a4e016b6a9f91fbe372672bdcf382c630bf59186/tree60d45288145414ee4702fcce61af7c7810c2a3df; exact Runtime5e9ad1c6f74241d8771d3284fdd2ce7a214fd344/treede2954a0ceadb4455903d9abdfec3b773318a50f. Runtime was clean at the initial source inspection and final check. Candidate has ONE additive test file, no product edits. No shared dependency, source pin, original test, grouping, interval, input or assertion changed.

## New minimal registered-provider reproducer

This case uses the existing production native_child fixture (RuntimeService/RealmStore and registered create_runtime_commit_service), one child, two track-create commands and the normal synthesized single step. No media generation, copied checkout, socket, daemon, validator replacement or private-record collector. The test retains the acceptance and inverse expectations; no skip or xfail. It is deliberately RED pending the Runtime owner correction. Its post-acceptance/undo assertions are UNREACHED.

Initial reproducer (before the source-custody assertion was added):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-D124-shared-four-return-sol-1417:/home/user/work/wt/rt-pin-5e9ad1c6:/home/user/work/agent-runtime-projection-0856/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short --basetemp="$TMPDIR/sequential-parent" tests/sdk/test_d124_sequential_materialization.py
```

Pytest result: **1 failed in2.56s**. First failure: `provider successor differs from its authenticated physical edges`. Raw stdout/stderr stayed in `$TMPDIR/sequential-parent.log`.

After adding the source-custody test, the same scoped command with `--basetemp="$TMPDIR/sequential-source"` yielded **1 failed,1 passed in3.08s**. The passing test proves complete step source/successor edge pairs and final-command attribution. No semantic source change exists, so this is source discrimination, not parentRED/currentGREEN.

Final exact source, after fixture import/lint correction:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-D124-shared-four-return-sol-1417:/home/user/work/wt/rt-pin-5e9ad1c6:/home/user/work/agent-runtime-projection-0856/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short --basetemp="$TMPDIR/sequential-final" --junitxml="$TMPDIR/sequential-final.xml" tests/sdk/test_d124_sequential_materialization.py
```

Pytest exit1; **1 passed,1 failed in2.72s**. `test_materialization_keeps_step_source_and_complete_successor_edges` PASS; `test_grouped_child_materialization_uses_the_complete_step_input` FAIL at normal submit with the same Runtime physical-edge predicate. Raw log/XML remain private under `$TMPDIR`; hashes are in source-manifest.json. Nothing is normalized to GREEN.

## Strict selected neighbours

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-D124-shared-four-return-sol-1417:/home/user/work/wt/rt-pin-5e9ad1c6:/home/user/work/agent-runtime-projection-0856/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short --basetemp="$TMPDIR/strict-controls" tests/sdk/test_timeline_inverse_fork_guard.py::test_fork_materializations_require_complete_unique_authenticated_edges tests/sdk/test_timeline_inverse_fork_guard.py::test_equal_payload_sibling_cannot_supply_fork_source_authority tests/editing_conformance/test_doc_patch_v2.py::test_ambiguous_entity_alias_refuses_and_qualified_revision_selects_one tests/editing_conformance/test_step_undo_v2.py::test_aba_tail_refuses_even_when_the_current_guard_matches
```

Pytest **20 passed in6.92s**. These use the existing dependency-only Runtime ABI/DetachedRealm fixture and are scoped producer guard evidence. They are not genuine original acceptance outcomes. They cover 17 materialization tamper cases, wrong/equal sibling authority, ambiguous alias, and ABA. No guard changed.

## Requested static checks

```bash
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR="$TMPDIR/ruff-cache" /home/user/work/venv-agent/bin/python -m ruff check tests/sdk/test_d124_sequential_materialization.py
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR="$TMPDIR/ruff-cache" /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR="$TMPDIR/mypy-cache" /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
git diff --check
```

Final targeted Ruff PASS; baseline Ruff **2143/2143**, exit0; Python3.11 mypy **1902/1902**, exit0; diff check PASS. Initial targeted Ruff found import formatting/F811 in the new test; fixture retrieval/import formatting was corrected, with no assertion changes. Baseline scripts do not include this test in their product counts; targeted Ruff covers it separately.

Python3.11 compile command (PASS, one file; outputs private):

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-typecheck-v2/bin/python - <<'COMPILE'
import os, py_compile, sys
from pathlib import Path
assert sys.version_info[:2] == (3,11), sys.version
py_compile.compile('tests/sdk/test_d124_sequential_materialization.py', cfile=str(Path(os.environ['TMPDIR'])/'sequential.pyc'), doraise=True)
COMPILE
```

Module-origin imports after the regression resolve Agent commit/_commit_patch from this candidate and Runtime service/timeline_commit_auth from the exact pin. Initial git SHA/tree and cleanliness were checked before tests; pre-test module origins were not separately captured. This limitation is retained in source-manifest.json rather than fabricating a preflight packet.

## Limits and admission

Initial available4,897,193,984 bytes; subsequent observed checks stayed below5GB (last shell check4,823,011,328). Source checks remained above4.6GB; no heavy body was launched. No original4 ran: there is no meaningful Agent semantic change, and the regular5,000,000,000-byte floor was not met. No six passing originals, native5 smoke replay, TEN/95/P4/core/full, body/profile/install/build/acquisition, service request or floor wait. No release/adoption or core425/REG14 deduction. The independent wholepath1405 final safe finding was consumed; no duplicate worker was dispatched.

Blocked on the authorized Runtime owner reviewing/correcting the exact step-input/command-input mismatch described in root-cause.md. Original scalar/compound allocation and grouped-birth inverse private pairs remain UNKNOWN and are not attributed from this smaller reproducer. Farm core and independent security/core review remain downstream gates.
