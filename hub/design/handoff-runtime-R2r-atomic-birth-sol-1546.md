# R2r atomic native birth authentication — completed author handoff

Ready for independent review and serial merge; no integrated P2/P3 acceptance is claimed.

## Source and correction

Worker `rt-R2r-atomic-birth-sol-1546` continues saved WIP `b11f390a22404a8d330a800501c32b88aa78bf17` from `tl/rt-R2r-atomic-birth-1543`, based on integration `9ce4242bc01f100bab9efc51032a73985cefb2b2`. Final prospective tree: `3bd06dc517f347976541ae4dde3caf3d29d03419`, independently equal to the central service snapshot tree. Current Agent head throughout these runs: `d682c5977e0d5a7627ca04852980a2d65ca899d4`; this is distinct from Proof1536's earlier `58316fd6` pin.

The original atomic scan resolves captures for all commands against `images(source)`, where the occurrence created earlier in this request does not exist. Proof1536's exact portable four-case test is preserved byte-for-byte at `evidence/test_native_birth_boundary.py`. Old 9ce production source reproduces fields 2 PASS / atomic 2 FAIL (grouped and separate steps); both atomic traces reach `native_site -> site`, refusing `provider occurrence alias is outside its boundary`. Corrected production source passes all four unchanged cases. Commands remain authentic public occurrence.create -> track.create -> occurrence.add-media, with an initially empty occurrence list and the original managed media/opaque payload. No fixture rewrite, fields substitution, extra publication or bootstrap bypass.

Production changes only `runtime_protocol/timeline_commit_auth.py::validate`: accumulate touched scopes using each command's sequentially reconstructed input image; then require the complete batch union in EVERY step after boundary authentication. Decision: move the complete-union guard to the end rather than retain the saved WIP's incomplete union check on earlier steps. This preserves the original all-steps/all-scopes condition, including timeline fallback, without using future aliases against the initial source. Failures still occur before persistence. No birth-scope exception or private authority added. Initial contradiction, unique owner/physical allocation, created/source/foreign/forged/alias/ABA/membership/order guards, inverse-stage helpers, history verifier, store and private port are unchanged.

The bounded new tests retain the saved four-case WIP and add fourteen atomic refusals: foreign binding source, ambiguous birth, forged foreign/future/wrong-owner allocation, outside read, and missing scope, each grouped/separate. Refusals assert exact expected invalid_records/identity_collision reason and unchanged full database, history and source.

## Commands and results

Unless noted otherwise, cwd `/home/user/work/wt/rt-R2r-atomic-birth-sol-1546`. Scratch `/tmp/w-ea32d4ad2a`; the worker `tmpdir` is a pointer file and was not treated as a directory. All pytest runs use the shared interpreter read-only and disable bytecode/cacheprovider.

1. Portable old source, cwd `/tmp/w-ea32d4ad2a`:

```bash
ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=/tmp/w-ea32d4ad2a/old:/home/user/work/wt/rt-R2r-atomic-birth-sol-1546:/home/user/work/wt/rt-R2r-atomic-birth-sol-1546/tests:/home/user/work/wt/rt-R2r-atomic-birth-sol-1546/packages/python:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -s -o addopts= -p no:cacheprovider /tmp/w-ea32d4ad2a/test_native_birth_boundary.py --basetemp=/tmp/w-ea32d4ad2a/pytest-old-exact
```

Exit 1: **2 failed, 2 passed, 9 warnings in 4.23s**. `evidence/portable-old-exact.log`. Private old package copied from the saved WIP with auth restored byte-for-byte via `git show 9ce4242bc:runtime_protocol/timeline_commit_auth.py`; every other production package file is unchanged from 9ce. An earlier attempt from the worktree cwd accidentally used current code because cwd preceded PYTHONPATH; `portable-old.log` is retained but excluded from old-source evidence.

2. Portable corrected source:

```bash
ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:tests:packages/python:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -s -o addopts= -p no:cacheprovider /tmp/w-ea32d4ad2a/test_native_birth_boundary.py --basetemp=/tmp/w-ea32d4ad2a/pytest-new-exact
```

Exit 0: **4 passed, 9 warnings in 4.07s**. Warnings are integration marker registration from running the portable file outside the repo's conftest tree; no skips/xfails. `evidence/portable-new-exact.log`.

3. Explicit integration-marked new cases:

```bash
ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/test_timeline_commit_authentication.py::test_created_child_public_sequential_birth_aliases_accept_fields_and_atomic tests/test_timeline_commit_authentication.py::test_created_child_public_atomic_keeps_birth_tamper_refusals --basetemp=/tmp/w-ea32d4ad2a/pytest-regression
```

Exit 0: **18 passed in 9.71s**. `evidence/regression.log`. Subsequent changes only underscore the two unused positive-test variables; final central suite includes the final bytes of all eighteen cases.

4. Central targeted service (the read-basis test needs HTTP):

```bash
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-R2r-atomic-birth-sol-1546 v2-auth-current-integration
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test rt-R2r-atomic-birth-sol-1546-v2-auth-current-integration-1023155001-1211
```

One request only. Exit 0: **338 passed in 93.35s** on final tree `3bd06dc517f347976541ae4dde3caf3d29d03419`. Actual command:

```bash
env PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:$PWD/packages/python:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py tests/test_timeline_commit_inputs.py tests/test_timeline_commit_port.py tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_source_duplicate_authority.py tests/test_timeline_source_document_boundary.py tests/test_timeline_raw_capture.py
```

`created_child_public` is a fixture in the authentication file; no separate `test_timeline_created_child_public.py` exists. All requested actual files and integration-marked cases are included. Central result directory above; durable copy `evidence/central-v2-auth.log`.

5. Required all44 sequential security controls and honest limitation:

`tests/test_timeline_commit_sequential_verifier.py` and `validate_sequential_capture` are absent from this assigned 9ce/b11 ancestry. The exact test source from separate `85b2feeb58bc54174ac7b89fda4805883865d3b2` is preserved in evidence; against this worker's current source the following exits 2 during collection with missing `validate_sequential_capture`, not a passing 44-case claim:

```bash
ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:tests:packages/python:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-atomic-birth-sol-1546/evidence/test_timeline_commit_sequential_verifier.py
```

For compatibility only, `git archive 85b2feeb5` was extracted into private scratch `/tmp/w-ea32d4ad2a/compat-85b2`, and only this narrow validate correction was transplanted there. No files from that branch were imported into this worktree, no branch changed, and no inverse-stage/private-store implementation was authored. Cwd private compatibility snapshot:

```bash
ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:tests:packages/python:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_sequential_verifier.py --basetemp=/tmp/w-ea32d4ad2a/pytest-security44
```

Exit 0: **44 passed in 11.21s**. Includes original forged/outside/ambiguous, replay correspondence, malformed capture and lifecycle refusals without weakening. `evidence/security44-compat.log`, exact test source, original retained fixture and private transplant patch are durable. This is supplementary branch compatibility evidence. Exact integrated all44 must run after the sequential owner/serial merge resolves the separate prerequisite; it is not qualification of 9ce's absent verifier.

6. Static and preservation checks:

```bash
/root/.local/bin/ruff check runtime_protocol/timeline_commit_auth.py tests/test_timeline_commit_authentication.py
/root/.local/bin/pyright --outputjson runtime_protocol/timeline_commit_auth.py
/root/.local/bin/pyright --outputjson /tmp/w-ea32d4ad2a/old/runtime_protocol/timeline_commit_auth.py
git diff --check
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-atomic-birth-sol-1546/evidence/audit.py
```

All exit 0. Ruff clean; Pyright old/current both zero diagnostics, zero added diagnostic identities. Audit: all **30** original auth top-level definitions (including decorators and fixture) AST-identical; **281** other test files byte-identical; **77/77** frozen files and **63/63** frozen34e schema/client/generator files identical; edit-command digest remains `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`. No test expectations deleted, weakened, skipped or xfailed. Initial Ruff found two unused WIP variables and they were corrected; no implementation diagnostics concealed.

Final SHA-256:

- auth: `02bc94cd0a41e3ec3fd6d3011d03509588fdb50d459517932d43ce72533f9d15`
- auth tests: `10f4f9b53e9a39afa735e26543c29cdb620c776a364b61e0009591212059ad6e`

## Contract, limits and next steps

No wire/schema/generated/client/pin changes. Existing commitTimeline/provider private port/store callers and full v2 request/reply/receipt/history/undo carriers remain unchanged by this validate-only correction. The 338-case result provides targeted evidence; this report does not independently requalify every accepted/merged/historical/preview/conflict variant. No full/native14/40/281/58/browser/journey/bench/provision/host/daemon suite or P2/P3 body was requested or run by this worker; the bounded central targeted suite owns its HTTP test. No deletion, Git mutations or shared dependency writes. No relitigation of PLAN/C0 decisions.

Implementation is complete for review; missing current-branch sequential verifier is the only qualification dependency. Recommended: independent review of final tree and deferred all-step union guard; serial Runtime merge coordinated with separate sequential-history and inverse authors; rerun all44 on the actual integrated source and the original normal-harness full-fixture seed before releasing P2/P3 bodies. Keep this atomic-native-birth author/change separate from historical85b2 and nested-inverse authors.
