# D124 validation

Disposition: bounded source candidate, held for genuine Runtime42aad nodes and FARM core. No source-only GREEN or historical-count reduction is claimed.

## Offline RED to corrected source

The first seven source-owned checks failed on the reviewed donor baseline: two successor-input cases, one ABI1 effect-pin case, three single-inverse endpoint cases, and one patch numeric-encoding case. The separate mirror consumer check failed at lookup._parent_clip_list with divergent clips/config.clips. Both were behavioral failures; the preliminary missing-platform and incorrect test import setup attempts are not behavioral evidence.

After repair, the eight source-owned checks passed. Independent review found a shared-root regression in initial single-stage eligibility; that was corrected to require exclusive paired turnovers with singleton ownership and preserved shot ID. All four unchanged shared restoration controls remain passing.

## Final exact commands and results

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-369ffa7c /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_d124_shared_custody.py tests/sdk/test_timeline_commit_provider.py::test_restore_inverse_proof_representations_allow_preview_and_redo tests/editing_conformance/test_doc_patch_mirrors.py::test_initial_contradictory_mirrors_still_refuse tests/editing_conformance/test_doc_patch_mirrors.py::test_sequential_clip_mirrors_execute_provider_history_and_inverse tests/editing_conformance/test_step_undo_v2.py::test_aba_tail_refuses_even_when_the_current_guard_matches tests/editing_conformance/test_step_undo_v2.py::test_missing_or_corrupt_authority_never_authorizes_partial_inverse tests/sdk/test_timeline_inverse_fork_guard.py::test_fork_materializations_require_complete_unique_authenticated_edges tests/sdk/test_timeline_inverse_fork_guard.py::test_equal_payload_sibling_cannot_supply_fork_source_authority tests/sdk/test_timeline_commit_provider_document.py::test_malformed_complete_closure_fails_closed --tb=short
```

53 passed in 13.09s (8 new offline checks + 4 unchanged shared restore/inverse controls + 41 targeted neighboring owner/pin/image/no-write/ABA controls). The existing dependency-only runtime_abi/DetachedRealm supplies no Runtime guard authority. The retained369 parent path supplies the pytest platform import only, never replacement acceptance for42aad.

```bash
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=$TMPDIR/ruff-cache /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
```

PASS: Ruff findings current=2143 baseline=2143.

```bash
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=$TMPDIR/mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
```

PASS: Python3.11 mypy findings current=1902 baseline=1902, using venv-agent-typecheck-v2.

```bash
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=$TMPDIR/ruff-cache /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/_commit_patch.py astrid/sdk/timeline/_doc_patch_materialize.py astrid/sdk/timeline/_recording.py tests/sdk/test_d124_shared_custody.py
```

PASS: all checks passed (also before the reviewed eligibility refinement; final repository baseline above covers the refinement).

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-typecheck-v2/bin/python - <<'PY'
import os,py_compile,subprocess
from pathlib import Path
changed=subprocess.check_output(['git','diff','--name-only'],text=True).splitlines()+['tests/sdk/test_d124_shared_custody.py']
output=Path(os.environ['TMPDIR'])/'compiled';output.mkdir(exist_ok=True)
for index,path in enumerate(changed):
 if path.endswith('.py'):py_compile.compile(path,cfile=str(output/f'{index}.pyc'),doraise=True)
print('Python 3.11 compile PASS:',len(changed),'files; outputs',output)
PY
git diff --check
```

PASS: 8 files compiled under own TMPDIR, diff check exit0. No shared dependency/cache writes.

## Independent core/security review

One independent review, core_security_review_fresh, completed with no remaining blocking finding after its shared-root correction. Its exact independent pytest command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-369ffa7c /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_d124_shared_custody.py tests/sdk/test_timeline_commit_provider.py::test_restore_inverse_proof_representations_allow_preview_and_redo
```

12 passed in6.27s. A first forked launch failed with an orchestration thread-store error; the fresh session completed the same single review. Review changed no files.

The reviewer also installed the unchanged original word_binding_recipe.install hook over the tiny synthetic offline producer. Both phrase and frame-offset choices passed production compilation, original recipe compilation, exact canonical mirror equality, and ordered native+derived before-value replay. Control script SHA256231d016df1a79e7c104c8e8d0a65abe6e7ca9d470b34f6fec6f94a4ee78dce7d. These are not the original genuine Runtime recipe nodes.

## Prepared original recipe2 service run — NOT SUBMITTED

Required unchanged nodes:

- tests/editing_conformance/test_word_binding_recipe.py::test_phrase_records_all_consecutive_main_word_ids
- tests/editing_conformance/test_word_binding_recipe.py::test_raw_canonical_bundle_compiles_in_fresh_process_without_history

When normal admission is at least5GB and the test-service environment is verified at exact Runtime42aad0e92f6da8ea83dd0a382a87e3acd12651b0/tree085a5be70b56353deb41ae7d743336a4ccb7f29c with genuine registered astrid provider, request only these original node IDs through the central service:

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-D124-shared-custody-sol-1247 targeted --files "tests/editing_conformance/test_word_binding_recipe.py::test_phrase_records_all_consecutive_main_word_ids tests/editing_conformance/test_word_binding_recipe.py::test_raw_canonical_bundle_compiles_in_fresh_process_without_history") && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test $R
```

This command is a prepared recipe, not evidence of submission or environment qualification. The named42aad checkout was absent at handoff; no source/environment copy or silent retarget was made. Free disk observed4.4–4.5GB. Genuine own-node targets then include original occurrence2, scalar3 and numeric3, retaining all original assertions and using the normal qualified provider environment. FARM owns the next core batch. No full,95,TEN,P4,broad-case,observer,collector or Farm batch was run/submitted.

