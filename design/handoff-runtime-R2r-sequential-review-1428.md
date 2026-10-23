# Runtime R2r/R1 sequential verifier review (1428)

## Verdict

**FAIL.** The actual Agent producer/Runtime consumer qualification did not accept any of the four real sequential positives. The five strict refusal controls passed, but the positive proof is not qualified.

## Exact joined evidence

- Runtime candidate: `c8c9094e37f3b723dae58337d672bbf9095e6dcf`.
- Agent checkout: `/home/user/work/wt/agt-pin-2dcae8d5`, `2dcae8d598201270a127ee865989d6af5c783fcc`.
- Exact command: `PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=$PWD ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-2dcae8d5 PYTHONPATH=/home/user/work/wt/agt-pin-2dcae8d5:$PWD:$PWD/packages/python /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider /home/user/work/wt/agt-pin-2dcae8d5/tests/editing_conformance/test_doc_patch_sequential_rebase.py`.
- Result: **4 failed, 5 passed in 8.72s**. The four failures are all real positives: declared/no-read × moved/current-head.
- Every positive failed with `provider alias is outside its authenticated boundary`, from `validate_sequential_capture` to original-side `validate` to `validate_step`/`site` (`timeline_commit_auth.py:1673`, `:351`, `:172`). The failure occurs before acceptance.
- The test's `finally` checks passed for every case: the saved SQLite dump and document remained unchanged. No write occurred.
- Module origins were the intended private pair: Agent `/home/user/work/wt/agt-pin-2dcae8d5/astrid/sdk/timeline/_commit_patch.py`; Runtime `/home/user/work/wt/rt-R2r-sequential-review-1428/runtime_protocol/timeline_commit_port.py`.
- Prior packet: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R1-private-sequential-packet-59e329b65a9b83c3.json`, SHA-256 `59e329b65a9b83c38f257ae5b87157072e30d71e63e0506b8b6908aa89231619`. It is producer-side evidence from a different Agent source snapshot, not substituted for the failed current join. The conformance test does not persist its in-memory PreparedCommit/capture after the consumer refusal, so no claim is made that this older packet is the exact failed candidate.

## Concrete findings

1. **Original-side positive path is broken.** `validate_sequential_capture` builds `original_prepared` and calls the general validator against the authenticated base. In `validate_step`, the submitted step patch/effect projection at `timeline_commit_auth.py:351-353` is normalized against the step's outer `boundary`, while binding assertions use each command's `command_inputs`. For the second sequential command, the producer's source-bound staged alias is valid only at the preceding command output; resolving the step patch through the outer boundary reaches `site()` and refuses it as outside the authenticated closure. The exact joined positives demonstrate this is not merely an attack-control result.

2. **Replay ordinal validation is incomplete.** At `timeline_commit_auth.py:1736-1739`, `change_ordinal < len(changes)` has no lower-bound check, so `-1` can select the final submitted change. The read branch at `:1743-1749` checks type but never checks `0 <= command_ordinal < len(records)`, so negative ordinals can index the last command and out-of-range values can escape as an uncaught `IndexError`. This violates required negative/OOB/bool structured-refusal behavior.

3. **Replay source proof is only structural/terminal.** `_capture_source_chain` (`:1548-1562`) validates shape/cycles and returns terminal strings. Its caller (`:1759-1770`) only checks terminal presence in the original input image and optionally compares owners when a binding candidate exists. It does not authenticate each nested transition to the preceding command's actual output/effect, enforce source step ordering, or prove terminal physical identity against the corresponding binding when candidates are absent. This is insufficient for prior-step/effects lineage and foreign/stale/ABA/order rejection.

4. **Physical-binding correspondence is incomplete.** `_capture_binding_identity` intentionally omits physical fields, and the source-to-landing loop (`:1681-1721`) only requires every landing physical binding to find a logical source match. It never requires every original physical binding to be consumed (`len(used) == len(originals)`), so an omitted source binding/map entry is not independently rejected.

## Other acceptance evidence

Author acceptance command: `PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py tests/test_timeline_commit_inputs.py tests/test_timeline_commit_port.py tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_source_duplicate_authority.py tests/test_timeline_source_document_boundary.py tests/test_timeline_raw_capture.py tests/test_timeline_commit_sequential_verifier.py`.

Result: **314 passed in 76.24s**. This includes synthetic/private carrier controls; it does not override the failed real Agent join.

`git diff --check` passed. Only the five allowed paths changed. Direct Ruff reported 22 diagnostics and Pyright 80 errors; exact-baseline comparison against `cfa0af0d476e6954df041c08d7ef378fd6782932` found equal diagnostic identities, with no additions/removals. No full suite, browser, socket, or duplicate nine-case run was performed.

## Disposition

Do not merge or publish this candidate. Correct original-side command-boundary projection first, then add controls for negative/OOB replay ordinals, complete source-chain lineage/order/physical binding, and omitted original map entries. Re-run the exact nine-case join once on the corrected candidate and exact Agent checkout; persist the full provider capture before consumer validation so a later refusal can be audited without repeating a known-failed body.
