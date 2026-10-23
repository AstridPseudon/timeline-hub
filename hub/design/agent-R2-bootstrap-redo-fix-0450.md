# agt-R2-bootstrap-redo-fix-0450: PARTIAL / BLOCKED

## Identity and change

Agent base SHA `f677e9bab7def6bcff8cd4faed55f29827b8af30`, base tree `9f15e3e82d6b3e700b54d788739e8cd79a993497`. Exact tested candidate tree: `32ec2bda3bdcd608aacfdb68e78c43680fc1acd2`. All three changed file blobs match that test snapshot; the harness will assign the final commit SHA.

Runtime: private read-only-use archive `/tmp/w-cf9e59f8b0/runtime-62c454ac`, extracted with `git archive 62c454ac07fb46a1a67847d933f1ed5f53043e30`; source tree `b84e048c455916c3b44cd1964aa8b55a3f4d8088`. The requested ad823 worktree is absent. Shared integration advanced from 62c454ac to be5848e1 while this worker ran, so final qualification explicitly imports/asserts the private Runtime package before pytest collection. No shared Runtime/dependency files were modified.

Comparison Runtime SHA: `ad823e0a0f5be4a7acf1d3006df6f794709da63d`.

Verified equal ad823/62c454 Git blobs:

- `runtime_protocol/timeline_commit_auth.py`: `85325f86fca53c2c487dbd3b064382ec3aa76dec`
- `runtime_protocol/timeline_commit_execution.py`: `039f63d47ada5ce5f31d2570a0d9b317fe09d275`
- `runtime_protocol/timeline_commit_store.py`: `607012dd19b81b933da1c12d5b8011621b35037e`

Only production change: `_commit_patch.py` retains the first inverse-stage input closure from the actual evaluated command input, then uses each exact preceding output as the following stage input. It no longer recompiles input images through historical source preference. It also emits deterministic physical input pins for roots changed by the preceding command in the same step, including ABI-1 requests with synthesized v2 metadata.

Production wiring remains `RuntimeCommitService.commit` -> `commands.execute` -> `CommitPatch.before/after/finish` -> existing prepared records/Runtime acceptance. The new real Runtime regression exercises that caller for both implicit and explicit metadata. It verifies unchanged request bytes, full supplied metadata/step attribution, `{data, receipt}` equality, canonical output, exact retry, and unchanged accepted history on retry. A separate regression proves that equal historical bytes cannot replace the original input revision and that adjacent inverse stages share the exact output closure.

No request/reply adapter, schema, client, producer pin, provider/executor, Runtime authentication, history guard, inverse allocation fact, or original assertion was removed or changed. The existing `commit.py` replay delta owned by legacyreplay0442 is untouched.

## Acceptance blocker and audit correction

**FAIL: original three cases remain failing at redo.** They now all reach Runtime `invalid_records: provider executed a different command`. The 0412 pristine trace actually fails at original initialization (old line 73), before undo/redo: this corrects audit0446's grouping of that trace as an inverse-stage redo failure. The added input pins fix that earlier failure; crash/resume, undo, exact retry, retired-ID and changed-payload guards then execute successfully up to redo.

The remaining conflict is explicit in existing source: Runtime `timeline_commit_auth.validate_claims` compares submitted `created` (default `[]`) with `record.command.created`. Native inverse restoration correctly emits nonempty created facts, and Agent `commit._check_reservations` requires command-created IDs to equal authoritative `record.created` IDs. Existing behavior tests require restored IDs in redo replies, e.g. `test_timeline_clip_add_provider.py:48` and `test_timeline_commit_graph_roots.py:163,180`. The original Runtime callers submit raw inverse commands with no created claims. These requirements cannot all hold without another owner-approved change outside this bounded seam. A temporary exploration confirmed that stripping only command-created IDs immediately hits Agent's `invalid created identity scope` guard; that exploration was reverted and is absent from the candidate.

I preserved allocation facts and all passing expectations rather than weakening either authentication layer. No success-to-refusal assertions, skips or xfails were introduced. Recommended next step: independent review of this partial candidate, then orchestrator ownership of the request-versus-provider restoration-fact mismatch across Agent reservation validation and Runtime claim authentication. Do not claim R2 bootstrap redo acceptance or merge as a complete fix.

## Exact verification

For direct commands below, the exact environment was:

```sh
ASTRID_RUNTIME_CHECKOUT=/tmp/w-cf9e59f8b0/runtime-62c454ac
PYTHONDONTWRITEBYTECODE=1
PYTHONPATH=.:/tmp/w-cf9e59f8b0/runtime-62c454ac
```

- **PASS:** `/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_provider_step_undo_v2.py tests/sdk/test_timeline_inverse_binding.py tests/sdk/test_timeline_pristine_initialize_provider.py tests/sdk/test_timeline_clip_add_provider.py tests/sdk/test_timeline_semantic_reservations.py`: **92 passed in 8.91s**, final source. Includes physical continuation, missing/corrupt successor proofs, per-step selection/CAS, declared consumers, original allocation and identity-reservation guards.
- **PASS:** `/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_commit_provider.py -k aba`: **8 passed, 104 deselected in 4.00s**.
- **INHERITED FAIL:** `/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_commit_graph_roots.py tests/editing_conformance/test_recorded_graph_roots.py`: **77 passed, 1 failed in 3.32s**. Failure: `test_generic_net_zero_root_edges_inverse_redo_preserve_absence_and_created_facts`, expected coalesced absence observations versus pre-existing transient restoration observations. Replacing only `_commit_patch` in memory with exact `git show HEAD:astrid/sdk/timeline/_commit_patch.py` and rerunning that node gives **the same 1 failure**, proving inherited; original test untouched.
- **PASS:** the new strict Runtime sequential-input nodes, with `import runtime_protocol` before `pytest.main(['-q','-p','no:cacheprovider','-m','integration','tests/sdk/test_timeline_pristine_initialize_runtime.py::test_initialize_batch_authenticates_sequential_command_inputs'])`: **2 passed in 1.53s**. The same two nodes with the original `_commit_patch` loaded in memory fail **2/2** at intermediate-image authentication. The new stage-image unit regression also fails on original source (**1 failed**) and passes corrected (**1 passed**).

**Central original-case command and result:**

```sh
$ORCH/bin/request-test agt-R2-bootstrap-redo-fix-0450 agt-R2-bootstrap-redo-0450-exact62 --files 'tests/sdk/test_timeline_pristine_initialize_runtime.py tests/editing_conformance/test_commit_runtime_first_clip.py'
$ORCH/bin/wait-test agt-R2-bootstrap-redo-fix-0450-agt-R2-bootstrap-redo-0450-exact62-1023050226-24165
```

The worker-specific named entry at `tests/suites.conf:157` invokes `/home/user/work/venv-agent/bin/python` with the exact environment above and preloads/asserts the private Runtime package, then runs `pytest -q -p no:cacheprovider -m integration` on those two original files. **3 failed, 3 passed in 11.03s; service exit 1 in 13s.** All original pristine crash/resume/retry/undo/redo and both nullable-speed first-clip assertions remain intact. Passed: new implicit/explicit input cases and existing live create/reload/retry. Failed: original pristine redo and both original nullable-speed redo cases. Full log: `$ORCH/tests/agt-R2-bootstrap-redo-fix-0450-agt-R2-bootstrap-redo-0450-exact62-1023050226-24165/log.txt`.

Two initial service requests were rejected by its argument parser before any tests ran (absolute scratch path, then `-m` in `--files`). The worker-specific named entry resolves this infrastructure problem; it changes no existing suite command. No full, native14, crash24, browser, P4 HTTP, or farm run was requested.

Quality commands:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_commit_patch.py tests/sdk/test_timeline_pristine_initialize_runtime.py tests/editing_conformance/test_inverse_stage_images.py
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-cf9e59f8b0/mypy-scoped /tmp/astrid-u2-typecheck/bin/python -m mypy astrid/sdk/timeline/_commit_patch.py --follow-imports=skip --ignore-missing-imports
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/w-cf9e59f8b0/runtime-62c454ac make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=/tmp/w-cf9e59f8b0/mypy-ratchet /tmp/astrid-u2-typecheck/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/w-cf9e59f8b0/runtime-62c454ac /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/w-cf9e59f8b0/runtime-62c454ac /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

Scoped Ruff: **PASS**. Scoped mypy: **PASS**, no issues in one source file. Normal Ruff: **PASS**, 2149/2149. Normal mypy ratchet: **FAIL**, 1914 current versus 1915 baseline (improvement ratchet; no allowance increased and no baseline changed). Vendor lock, artifact manifest and diff: **PASS**. Full suites unverified by design.

Reports and commit message are in the assigned worker folder and flat design. `BLOCKED` is written; `DONE` is intentionally absent because acceptance is incomplete.

Baseline mypy attribution was verified with the normal comparator using mypy's read-only shadow-file option: load `scripts.reshape.compare_mypy_baseline`, append `['--shadow-file', 'astrid/sdk/timeline/_commit_patch.py', '/tmp/w-cf9e59f8b0/baseline_commit_patch.py']` to `COMMAND`, and call `main()`, with `baseline_commit_patch.py` containing exact `git show HEAD:astrid/sdk/timeline/_commit_patch.py`. It also reports **1914/1915, exit 1**, so the ratchet decrease is inherited rather than an improvement introduced by this patch. No baseline was rewritten.
