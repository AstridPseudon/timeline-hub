# Agent capture-current owner review

**Verdict: APPROVE the bounded Agent source port `92427b3af0bfaba2ff604791cf3e5165125b6d54`, tree `525bdabe863a42bc177f5ff331560133f77ce634`. This is not a complete capture-certification, renderer, current-release or Gate 1/7 approval.** No product or test edits were made during this review. Keep `project_capture` intact until the Runtime owner qualifies the corrected independent verifier against this exact source, including the additional 09:58 counterexamples and genuine positive controls.

Reviewed against PLAN, repository AGENTS.md, `agent-capture-provider-current.md`, Agent INBOX 09:42/09:58 and `runtime-capture-authority-review.md`. The approved base is `efb96034fc7c80a6e73900bfc57dac53260beb3c`; the older reviewed port source is `d977b59a6a2fc403c57ee76764dd3bd81523045c`. No decision was changed.

## Source findings

- `astrid/sdk/timeline/commit.py:636`: the optional method deep-copies the input tuple and returns a deep copy of exactly `{base: bundle_from_document(document), preview: preview_authoring_candidate(candidate)}`. Its only calls are the two constructors and two `copy.deepcopy` calls. The existing constructors validate/compile detached data; there is no client, Runtime import, IO, renderer, save or attestation dependency. The IO/import-fence tests pass. Provider ID `astrid-v1` and interface version 1 remain unchanged.
- `project_capture` is AST-identical to the parent. It still uses the one `project_runtime_parent_composition` projector. Its retained-source checks still have the membership gaps identified at 09:58: extra/unused source rows, removed placements and renamed authoring shot keys are not all authenticated. This review does not reinterpret the new pure hook as a verifier or claim these holes are closed. Runtime owns those independent comparisons; deletion of the Agent verifier stays held.
- `astrid/sdk/timeline_filmstrip.py:340`: spreading the complete detached managed expansion before adding the existing parent/pin fields preserves `outputs`, `graph`, internal input images and unknown expansion data. Config/registry still come from the exact immutable opener. The whole-expansion golden compares equality, with no graph/output ignore list. Canonical-image tests preserve authored payload `created_at` and opaque `dependency_manifest` fields while removing only the read-envelope wrappers; shot/internal pin identities, digests and first-occurrence order survive. Mutation checks leave original read rows/document unchanged. Current `managed_timeline.py` is untouched.
- `astrid/core/execution/generic_host.py:6505,6722,6997,8052` and `core/rendering/verified_source.py`: both complete files are byte-identical to reviewed `d977b59a`. The host rejects reserved source keys at the input-spec, params, inputs and per-backend config boundaries; rejects caller replacement of timeline, registry and inline snapshot for a certified ref; checks differing duplicate refs and capture snapshots; fetches only task-authorized CAS digests and verifies their bytes. Ref project/timeline/revision and revision/working-copy digests must match the admitted authority. Source metadata alone on a CAS capture does not mint authority.
- The authority crosses the process boundary as `PreparedTimelineInputs.timeline_source`, outside public dict keys. The inherited anchor hashes an attempt-local binding containing the ref, authority, exact original snapshot and final prepared timeline/registry paths+byte digests. Paths must resolve inside the attempt. The command runner clears ambient `ASTRID_VERIFIED_TIMELINE_SOURCE` after assembling command env, validates the same pair and supplies only its host-owned anchor. The real command subprocess test consumes this binding; path substitution, byte substitution, binding mutation, direct typed construction and JSON numeric substitution are refused.
- This host trusts the Runtime claim and authorized object list. It does not independently authenticate history or cure a falsely certified Runtime ref. The claim double in the host unit tests is explicitly a double; existing exact-tree central actual-Runtime controls provide additional host evidence, not the independent verifier proof.
- Stored snapshots/history are not rewritten by these Agent changes: the provider methods copy data, filmstrip creates a new projection, and the host writes derived files only inside its attempt. The port adds no migration or retroactive recertification. New saved capture bytes/cache identities intentionally include the complete expansion. An old reduced/forged snapshot must not acquire certification by filling in missing graph/output fields or recomputing hashes. Actual historical-admission downgrade/certification, stored-spec immutability and retry evidence remain the Runtime pair owner's responsibility; they were not independently qualified here.
- Existing scene mapping, opaque clip IDs, final staged Root callback and successful-fresh-frame labels survive. `composed_frame.py` and `filmstrip_execution.py` are byte-identical to the parent; filmstrip's only edits are the expansion spread and early reserved-key guard. All 59 scene-source tests pass against the read-only public12 environment. Runtime pin `94114269d1ce23ab3224d7eca5a85138ce2b5fed`, public `@banodoco/timeline-composition` 0.0.12 artifact, both Remotion package files, theme schema, invocation and managed-timeline files are unchanged. The three current-main commits already in the base are retained; no wholesale old-branch revival occurred.

## Expected current conflicts and unmet requirements

| Boundary | Classification and required next step |
| --- | --- |
| Current integration source overlap | At inspection `/home/user/work/agent` was `df2739f903edac02bd36b4446deeea847524c040`. `git diff --name-only efb96034 HEAD --` all eight capture-port paths there was empty. No observed overlap on these paths; this is not a merge execution or qualification of later integration changes. |
| Independent Runtime verifier | Still open. The 09:58 false-base/source cases are also missed by unchanged Agent checks. Pair the corrected Runtime source with exact Agent 92427b3a; keep both existing verification paths until all negatives and supported new/clone/rename/delete positives pass. This reviewer did not duplicate the assigned Runtime 20-case run. |
| Current Runtime/client handshake | Expected separate development-pin conflict. Existing central run on this Agent tree has Runtime schema `3e5e78d0…` versus pinned client's `8d7f2987…`; two M1 tests fail before edits at health negotiation. Preserve the pin as instructed; move once to the reviewed post-F1/F2 tuple with App. No current-release claim. |
| Four RenderRequest propagation cases | Existing strict xfails remain with original assertions. Host source now exists, but `RenderRequest` still has no `verified_source` propagation. Its contracts implementation is unchanged by this source. These remain renderer-consumer requirements, not passing host tests or completed M3 behavior. |
| Three SDK invocation reserved-key cases | Existing strict xfails remain with original structured-error/no-admission expectations. `prepare_filmstrip` now rejects reserved keys, but invocation lacks reviewed d977's early `reject_source_keys` + `CapabilityValidationError` mapping. Two keys now expose an uncaught `ValueError`; `timeline_source` hits the older unsupported-product-input path. This is a changed error surface within a previously unmet requirement, not evidence of complete SDK validation. No previously passing requirement was rewritten to bless it. Authorize/port the bounded invocation guard separately. |
| Two SDK publication-double cases | Existing strict xfails unchanged: the double has no Runtime admission publisher. They are not actual current-Runtime positives. They were excluded explicitly from this review's closure smoke; the source owner's full closure run recorded 23 pass/5 strict xfail. |
| Old stored admissions / legacy aliases | No backfill/recertification in Agent. Runtime's corrected outer/inner-context handling, all aliases and per-carrier comparisons remain required, with immutable stored bytes and exact retries. New graph-complete projections must not mask missing historical proof. |
| Earlier public12 central setup | Same-tree central remotion lane had 53 pass/19 missing-React setup errors. The direct scene-source command below supplies the existing fixture override; builds and peer links stay in private pytest tmp directories. It passes all 59 scene nodes, without mutating shared dependencies. |

## Independent smoke commands and results

Commands ran from `/home/user/work/wt/agt-review-capture-current`. Shared venv/node_modules were read-only; no full suite, browser, socket suite, central request or Runtime independent verifier run was launched by this review.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-capture-current/review_source.py
# PASS, exit 0: exact source/tree; reviewed-file byte equality; unchanged project_capture AST;
# hook call census; preserved scene consumers, public12 and Runtime pin.

git show --stat 92427b3a
git diff 92427b3a^ 92427b3a -- astrid/core/execution/generic_host.py astrid/core/rendering/verified_source.py astrid/sdk/timeline/commit.py astrid/sdk/timeline_filmstrip.py
git diff 92427b3a^ 92427b3a -- tests/sdk/test_capture_source_runtime.py tests/sdk/test_capture_closure_source.py
# Read-only source/test review; eight changed paths, four product paths. Assertions preserved.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_capture_projection.py tests/packs/rendering/test_verified_source.py tests/sdk/test_timeline_filmstrip.py tests/core/execution/test_generic_host_contract.py -m 'not integration'
# 143 passed, 9 deselected in 30.58s; exit 0.

ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/sdk/test_timeline_capture_projection.py
# 9 passed, 34 deselected in 8.75s; exit 0.
# Fixture explicitly archives Runtime 4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136.
# In-process SQLite/CAS goldens only; not a current-Runtime/transport qualification.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_capture_closure_source.py -k 'not sdk_capture_reference_admission'
# 23 passed, 2 deselected, 3 strict xfailed in 278.06s; exit 0.
# Two publication-double nodes intentionally deselected; all three SDK guard requirements remain.

ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0012/node_modules ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0012 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/rendering/test_scene_source_carry.py
# 59 passed in 56.84s; exit 0. No renderer/browser/socket; fixture-owned builds only.

/home/user/work/venv-agent/bin/ruff check --no-cache --output-format concise astrid/core/rendering/verified_source.py tests/packs/rendering/test_verified_source.py tests/sdk/test_timeline_capture_projection.py tests/sdk/test_capture_closure_source.py tests/sdk/test_capture_source_runtime.py
# All checks passed; exit 0.
git diff --check
# Passed; exit 0.
```

## Existing central evidence inspected, not rerun

Read `snap`, `ext`, `summary`, `request` and `log.txt` for `agt-m3-capture-provider-current-commit-integration-1020095215-3997`. Its Agent snapshot is exactly tree `525bdabe…`. Exact runner command:

```bash
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_m1.py tests/sdk/test_capture_source_runtime.py
# 2 failed, 23 passed, 4 xfailed in 24.01s; exit 1.
```

Both failures are the health/schema mismatch above; 23 capture cases pass, including four genuine saved/working-copy inline/ref claim-to-host positives and twelve config/registry/shot-digest refusal controls. The four original renderer-carry assertions remain strict xfail. `ext` includes earlier Runtime `642eef74` attempts and the executed `c0dcd3871d78c405184506eb6735565592498c77` source. Because the external source is a live integration path and the independent verifier was not tested here, this is not a frozen corrected-pair certificate.

Also inspected `snap`, `exit` and log tail for `agt-m3-capture-provider-current-remotion-0012-nodes-1020095251-15088`: same Agent tree, 53 pass/19 setup errors in 30.11s, exit 1. The successful independent 59-node scene rerun above addresses the fixture environment, not all render/invocation qualification.

Review completion is unblocked. Next: Runtime owner freezes its corrected source and pairs the independent comparisons plus 09:58 cases; Agent manager can then assess verifier deletion. Renderer propagation, SDK error mapping, historical-claim proof and the coordinated safe repin remain explicit work. No full suite, pixel/audio parity, complete current transport, make check or full typecheck is claimed.

## Worker handoff

Only notes/report.md is added in this worktree. The flat review and reproducible
read-only source probe are under the task-authorized orchestrator design/worker
paths. No product/tests/shared dependencies/integration/ledger changes, Git
mutation, push or full-suite request occurred.

Decision made: approve only the explicitly authorized source unit, retaining all
seven required renderer/SDK xfail assertions and the duplicate Agent verifier.
This follows the 09:42 and 09:58 decisions; no new policy was selected. No blocker
prevents completion of the review. Runtime pairing and the listed consumer/release
requirements remain external follow-ups, with their evidence limits stated above.
