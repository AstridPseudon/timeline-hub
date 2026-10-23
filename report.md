# agt-V2-D12-guard-audit-0612

**READONLY bounded-fix review: PASS on `b42b7d72a65cab305a4b953093963019aabc70b9`.** Luna0606's sole bounded-fix finding is **superseded** by approved D12/D12a and C0d. No tested newly introduced invalidity was accepted. Preserve the source. This is not an all-green delivery/native acceptance claim.

**Decision and scope.** Read PLAN §3, commit-v2 §§1–5 (particularly the final-validation paragraph at lines 1307–1315), BOARD-HEADER D12/D12a, author0553 and independent0606. D12 expressly permits an already-unresolvable declaration with unchanged targets; D12a applies that rule to every V2 check. A target absent in both baseline and candidate has not been removed by this commit. Thus the unchanged missing-track/asset examples are permitted retention, not evidence for deleting the exemptions. New references, modified reference fields, new clips, removed previously present targets, changed intervals/bounds and changed physical owners remain strict. No new policy, waiver, equivalence or permission wait was needed.

**Additional limitation: FAIL for universal child missing-asset retention.** An extra probe beyond Luna's accepted examples found an unchanged child clip with `asset: "already-missing"` is refused even for an unrelated parent name edit. `authoring_bundle._assert_internal_edit_supported` at line 684 calls `_clip_selected_media` at line 552, which refuses the dangling media selector before production final validation; direct final validation also reaches this compiler refusal at `_commit_timing_validation.py:314`. That owner was not changed by b42. This is a separate pre-existing over-refusal, not new invalidity passing or grounds to remove V2's retention clauses. The probe remains failing, with no skip/xfail or changed expectation. Broad child-retention claims require a narrow authoring-compiler owner follow-up; this review does not repair or waive that guard.

**Stale-window scope: pending, unchanged.** Reuse the author0553 original-three evidence: two passed, stale-window setup refused. The protected seed's existing legacy word declaration loses its unchanged search basis when `occurrence:occ/clip:voice.from` changes from 2 to 4. Current C0 correctly refuses that request. It needs a separate fixture/scope decision; it does not hold independently valid setup/speed fixes. No stale-window rerun, original-three all-green claim, 52/54 claim, or native14 run was made here.

**Production caller and exact arguments.** Runtime snapshot `85dafdf46742b02ae5e4a300656cd6f5d68f0d4d` uses `runtime_protocol/timeline_commit_provider.py:18,70`: `load_timeline_commit_provider("astrid")` loads `astrid.sdk.timeline.commit.create_runtime_commit_service`; `timeline_commit_execution.py:87` executes `provider.commit(provider_context, port)`. A fresh process actually loaded this provider and asserted its `RuntimeCommitService` type and `(context, port)` signature. Contract digest: `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`.

At Agent `commit.py:1117–1125`, after all commands/replay and reservations, the current production call is exactly:

```python
validate_final_candidate(
    plan.bundle,
    baseline=bundle if current == base else head_bundle,
    schema_inputs=schema_inputs,
    realm_id=context.get('realm_id'),
    source_bundles=inverse_sources,
)
```

The scratch probes call the real factory/service/commands/final validator through the existing `test_p1_doc_patch_provider._service_call` and `DetachedPort`. Python profiling observes one actual final-validator call for each production guard probe, with the real baseline, `schema_inputs=[]`, `realm_id="realm-1"`, `source_bundles=[]`. Storage is the main suite's in-memory scoped Runtime port; its `runtime_abi` fixture substitutes ABI exceptions/metadata only. These are real production-provider executions, not HTTP/daemon or storage integration qualification. The separate fresh-process mount check uses actual Runtime modules without that fixture.

Exact production test requests use `api_version=1`, `project_id="project-1"`, `timeline_id="film"`, `base_revision_id="parent-1"`, `base_publication_id="bootstrap"`, one `doc.patch` command with `schema_version=1`, `version="1"`, `select=null`, and guarded changes; `label="D12 guard audit"`, `merge="fields"`, `reads=[]`, `dry_run=false|true`, `source={"via":"python","detail":"guard-audit"}`, `rationale="D12/D12a unchanged-basis adjudication"`, `group_id="guard-audit"`. One step has `id="audit"`, `label="Audit"`, `intent="Guard verification"`, `tags=["audit"]`, `command_ordinals=[0]`, `patch` equal to the exact ordered command changes, and `reads=[]`. Context uses `idempotency_key="request-1"`, the existing digest of the complete invocation, `realm_id="realm-1"`, `publisher="actor-1"`. The full executable operands and before values are in `/tmp/w-70ce9f45ed/test_guard_adjudication.py`.

**Observed guards.**

| Check | Result |
| --- | --- |
| Unchanged parent missing track/asset; unrelated name edit | PASS: accepted and preview; clip JSON bytes unchanged, child images unchanged |
| Unchanged child missing track | PASS: accepted and preview; child images unchanged |
| Track/asset reference newly broken, modified from another missing target, new clip, previously present target removed | PASS: eight production refusals, HTTP 422 / invalid; head unchanged, no preparation/acceptance |
| Literal null speed newly authored | PASS: production accepted; canonical `speed` remains literal null |
| Speed true, false, string, array, object, zero, negative | PASS: seven production invalid refusals |
| Unsupported map with changed map/timing/declaration/source window/asset/used track | PASS: six production refusals; no complete-basis bypass |
| Unchanged unsupported map; unrelated unused track | PASS: original accepted/preview controls preserve exact child images |
| New/changed occurrence interval or bound; new/changed source interval or asset extent | PASS: original boundary controls |
| Changed physical owner with inherited occurrence overrun, asset overrun, unsupported map or missing track | PASS: four additional direct validator refusals; candidate bytes unchanged |
| Unchanged child missing asset | FAIL: existing authoring compiler rejects; separate limitation above |

The map return is reached only after compilation reports `unsupported explicit map` and `_timing_basis(candidate) == _timing_basis(baseline)`. That basis captures scope/parent owner, placements, physical source shots, pinned documents, shot payloads, clips/declarations, used tracks and timing/config inputs. Unused tracks and opaque params are deliberately excluded. Existing owner-change map control plus six production mutations exercise that boundary. Null speed arithmetic matches existing canonical `duration.py` and evaluator semantics; it does not normalize authored JSON.

**API preservation.** No product or main-suite test file changed, including request/reply/history/idempotency owners. The complete request remains `api_version/project_id/timeline_id/base_revision_id/base_publication_id/commands/label/steps(id,label,intent,tags,command_ordinals,patch,reads)/merge(fields|atomic)/reads/dry_run/source/rationale/group_id`, with stable idempotency. Existing full `{data,receipt}`, accepted/merged and authentic historical rebased, canonical document/head/revision/digests/records/effects/steps/dependencies/history/undo_steps, conflict reason/head and invalid code/path/hint/suggested command remain unchanged. Preview assertions require `would_status="accepted"`; merged preview's `accepted|merged` implementation remains at `_commit_preview.py:45`. Refusal output retains `details.code="invalid_document"`, `path=[]`, hint and suggested command, with the concrete failing path in the message. This audit is not an independent qualification of all DTO, merged/history replay or undo scenarios.

**Tested source and imports.** Agent HEAD is exactly b42 above; `git diff --numstat b42b7d72a -- astrid tests scripts runtime.lock.json artifacts.json` is empty. SHA256:

```text
dc47fc582f6320f78a5bfd0413e543c7fb0db33816c6d80aeba778b3bc2c5073  astrid/sdk/timeline/validation.py
5aa5bed99d020458a8e91952e3f6aaf53fc8f6d72dc5d62fe405f275403b6a16  astrid/sdk/timeline/_commit_timing_validation.py
651f32e8a6b88bf4267737a474039e5a1d39898b220ea6c6d1a739feea03cb53  tests/editing_conformance/test_commit_boundaries_d12.py
```

`astrid`, `commit`, both validation modules and `astrid_runtime_client` import from `/home/user/work/wt/agt-V2-D12-guard-audit-0612`; `banodoco_timeline_schema` imports from `/home/user/work/venv-agent/lib/python3.13/site-packages`. Actual Runtime/platform/provider-loader imports for the mount check resolve under `/tmp/w-70ce9f45ed/runtime-source/runtime_protocol`. Python is `/home/user/work/venv-agent/bin/python` 3.13.16; persistent private typechecker is `/home/user/work/venv-agent-typecheck-v2/bin/python` 3.11.17. Snapshot creation, after printing Runtime HEAD:

```sh
mkdir -p /tmp/w-70ce9f45ed/runtime-source
git -C /home/user/work/runtime archive HEAD | tar -x -C /tmp/w-70ce9f45ed/runtime-source
```

Shared dependencies and all integration worktrees were read-only. Worker `tmpdir` is a locator file containing `/tmp/w-70ce9f45ed`; all scratch, caches and logs are there.

**Exact commands and results.** Reuse independent0606's exact-b42 evidence: required matrix **133 passed**, fork/provider/recipe controls **93 passed**, scoped Ruff/mypy PASS, normal Ruff **2150/2150**, mypy **1915/1915**, lock/artifact/whitespace PASS. Its report supplies the counts; these two suites were not rerun here. Matching the three source hashes above confirms the reviewed source.

New targeted run:

```sh
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=.:/tmp/w-70ce9f45ed:/tmp/w-70ce9f45ed/runtime-source
export TMPDIR=/tmp/w-70ce9f45ed
/home/user/work/venv-agent/bin/python -m pytest -s -q -o addopts= -p no:cacheprovider /tmp/w-70ce9f45ed/test_guard_adjudication.py tests/editing_conformance/test_commit_boundaries_d12.py tests/editing_conformance/test_commit_legacy_text_reference.py
```

**73 passed, 1 failed in 4.43s; exit 1**, `guards-final.log`. All requested disputed production guards and original 43 selected controls passed. The one failed extra child missing-asset probe is retained and explained above. Initial scratch attempts needed Runtime's platform import, exact submitted step patches and the valid native `parent/clip:new-clip` created-ID spelling; only scratch helpers/operands were corrected. Earlier logs remain (`guards.log`, `guards-corrected.log`); no production source or existing test expectation was altered.

After adding four previously untested owner negatives, ran only those new cases:

```sh
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider /tmp/w-70ce9f45ed/test_guard_adjudication.py::test_changed_physical_owner_is_strict
```

**4 passed in 1.44s; exit 0**, `owners.log`. Scratch-only collection reports an unknown integration marker from an imported existing test module; no test was skipped or xfailed.

Quality commands (each exit 0, no baseline changes):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. RUFF_CACHE_DIR=/tmp/w-70ce9f45ed/ruff /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/validation.py astrid/sdk/timeline/_commit_timing_validation.py tests/editing_conformance/test_commit_boundaries_d12.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=/tmp/w-70ce9f45ed/mypy-scoped /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/validation.py astrid/sdk/timeline/_commit_timing_validation.py --follow-imports=skip
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. RUFF_CACHE_DIR=/tmp/w-70ce9f45ed/ruff make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=/tmp/w-70ce9f45ed/mypy-ratchet /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

Results: scoped Ruff clean; mypy no issues in two files; normal Ruff **2150/2150**; mypy ratchet **1915/1915**; runtime lock OK; artifacts current; whitespace clean. Logs: `scoped-ruff.log`, `scoped-mypy.log`, `ruff-ratchet.log`, `mypy-ratchet.log`; mount check and actual origins: `mount-origins.log`.

**Handoff.** Preserve b42's bounded fixes and supersede Luna0606's recommendation to remove them. No new-invalidity repair request is needed. Record the child compiler over-refusal separately for its owner; keep stale-window scope pending separately. No full/browser/socket/heavy/farm/native14/crash24/P4 HTTP-body execution, schema/pin/generated/test changes, shared dependency edits, git mutation, upstream action, deletion or new executor. Report-only changes and commit message complete this assigned readonly review; DONE means this audit is complete, not all-green acceptance.
