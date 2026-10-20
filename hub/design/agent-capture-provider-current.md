# Current Agent capture provider

Source ready on worker `agt-m3-capture-provider-current`; current capture corpus centrally green, broad named lane red only at the required development-pin/current-Runtime handshake. Renderer propagation and Runtime independent 20-case pairing remain unqualified.
Base commit: `efb96034fc7c80a6e73900bfc57dac53260beb3c`.
Final source tree SHA: `525bdabe863a42bc177f5ff331560133f77ce634` (both central requests snapshot this tree).
Branch: `tl/agt-m3-capture-provider-current`. The harness assigns its commit on worker exit; resolve that branch and verify its tree equals the SHA above before freezing the Runtime pair.

The approved additive hook is on the existing startup-loaded `RuntimeCommitService`, with provider ID/interface unchanged:

```python
capture_candidate_inputs(document, *, candidate) -> {
    "base": bundle_from_document(document),
    "preview": preview_authoring_candidate(candidate),
}
```

It deep-copies inputs and outputs, uses only those existing pure functions, and adds no IO, DTO, endpoint, attestation, renderer import or ABI major. Runtime owns optional-hook absence refusal and all independent certification comparisons. The existing Agent `project_capture` verifier is UNCHANGED and must remain until Runtime's independent comparisons pass the real pair.

Ported from reviewed `d977b59a6a2fc403c57ee76764dd3bd81523045c`: exact `core/rendering/verified_source.py`, the four missing host handoff hunks (the complete resulting generic_host file is byte-equal to that reviewed source), full saved expansion spread in `_open_current_input_closure`, and the early prepare_filmstrip reserved-source-key guard. Current scene-source map/final-Root callback/fresh-only behavior and public12/Runtime94114269 pins are unchanged. Current managed_timeline canonical-image conversion already matches the reviewed conversion; no edit needed. No producer/automatic/element changes, old snapshot writes, launcher dependency, second projector, source factory or colon-ID parsing.

SHA256 of current source:

| Path | SHA256 |
| --- | --- |
| astrid/core/rendering/verified_source.py | c6d9665a453fab9b5cc7fab644d7b684370a61d65937ee010159806bd3003b71 |
| astrid/core/execution/generic_host.py | 596bcefdee9ee30fd8cef752f3194eabe0dfaae170135401ef8b58a8e9af5457 |
| astrid/sdk/timeline/commit.py | 485f7ac0d904feb40882bf9ac2e58d000268243a528a89f55d5e3e4138e26560 |
| astrid/sdk/timeline_filmstrip.py | 2f4557f1134b7b5d9998b0aa32fa0f9aa5acf6184f030e723e0a085985bb1569 |
| astrid/packs/rendering/actions/render/managed_timeline.py (unchanged) | fde15d771bf2ad51a74416fbeedc05a7679fdc82659a83232f92d337d5225494 |

## Direct checks

Commands run from this worker, using read-only shared dependencies:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_capture_projection.py -m 'not integration'
# 34 passed, 9 deselected in 2.14s. Exact hook golden, detached mutation, IO/import fences and retained verifier negatives.

ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/sdk/test_timeline_capture_projection.py
# 9 passed, 34 deselected in 8.99s. Entire saved projection exact equality and six candidate goldens.
# Fixture explicitly archives Runtime 4bb1d0f7: these are pure current Agent projector goldens on legacy saved reads, not current-Runtime qualification. In-process SQLite/CAS only, no daemon/socket/browser.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/rendering/test_verified_source.py
# 33 passed in 4.91s. Real host command subprocess receives its binding; reserved keys, caller replacements, forged authority, JSON numeric identity, file/binding changes fail closed.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_filmstrip.py tests/core/execution/test_generic_host_contract.py tests/test_generic_host.py::test_input_materialization_rejects_traversal_names tests/test_generic_host.py::test_input_materialization_preserves_exact_length_ordinary_path tests/test_generic_host.py::test_input_materialization_rejects_foreign_nested_digest tests/test_generic_host.py::test_materialize_inputs_fetches_media_id_only_registry_entry
# 80 passed in 27.11s.

/home/user/work/venv-agent/bin/ruff check --no-cache --output-format concise astrid/core/rendering/verified_source.py tests/packs/rendering/test_verified_source.py tests/sdk/test_timeline_capture_projection.py tests/sdk/test_capture_closure_source.py tests/sdk/test_capture_source_runtime.py
git diff --check
# Both pass.
```

Full repository lint baseline check exits 1 because 2212 findings is eight BELOW the checked-in 2220 shrink-only baseline; no baseline edited. Per-file Ruff JSON comparison against `git show HEAD:PATH` found zero added/removed findings in each of the three modified existing product files; new module and touched tests lint clean. Import-cycles gate reports rendering↔timeline against its checked-in baseline, but a private `git archive HEAD astrid/core` AST comparison proves exactly the same seven cycle pairs before/after. Structure gate passes: current14/new0/fixed0. Mypy baseline check cannot complete (missing YAML stubs; installed NumPy pyi uses newer syntax than the configured Python3.11 target); no dependency mutation or type-check green claim. No full suite or make check/browser parity requested.

## Central requests and remaining pair

- `agt-m3-capture-provider-current-commit-integration-1020095215-3997`: existing named commit-integration plus tests/sdk/test_capture_source_runtime.py. Current Agent snapshot + actual current Runtime; four new host-only genuine saved/working-copy inline/ref positives, whole saved expansion equality, original twelve config/registry/shot-digest forgery cases, uncertified/native and duplicate-reference controls. **23 passed / 4 existing xfailed capture cases; 2 default M1 failures**, total 24.01s (service28s), exit1. Both default M1 nodes fail health contract negotiation before edits: current Runtime reports schema `3e5e78d0…`, task-required Agent94114269 client expects `8d7f2987…`. No repin attempted (explicit task constraint). Service external Runtime was `c0dcd3871d78c405184506eb6735565592498c77` when launched; its queue metadata also records earlier `642eef74` attempts. Current capture cases use actual RuntimeService and passed; this is not a whole transport/current-release qualification.
- `agt-m3-capture-provider-current-remotion-0012-nodes-1020095251-15088`: tests/packs/rendering/test_scene_source_carry.py + tests/sdk/test_timeline_filmstrip_invocation.py, pinned public12 environment. **53 passed / 19 setup errors** in30.11s, service46s, exit1. Every error is missing provisioned React peer: the fixture reads ASTRID_TEST_NODE_MODULES or checkout remotion/node_modules, whereas this lane only sets ASTRID_REMOTION_PROJECT_DIR. No assertion failure. A direct targeted rerun supplies the fixture's existing ASTRID_TEST_NODE_MODULES override, pointing read-only at agent-remotion-0012/node_modules; all links/builds stay in its private tmp_path fixture.
- Earlier two remotion-0012-nodes requests `1020094959-19766` / `1020095013-22509` were rejected before running because the service disallows `-m=integration` in --files. No result claimed. No standalone golden lane is needed now that the in-process fixture has been inspected and run directly.

Runtime manager must pair the independent 20-case candidate comparisons against this exact Agent tree after harness commit; it is not this worker's Runtime edit. Keep the Agent duplicate verifier until paired green. No current-tuple release claim: task preserves Runtime94114269 development pin and the separate F1/F2 republish hold.

## Existing unmet consumer requirements retained

- The original four real-capture positives also require RenderRequest.verified_source propagation. Current RenderRequest has no such field. They remain strict xfail with unchanged assertions, now naming that remaining requirement. New current-Runtime host-only positives test the approved host scope without claiming renderer propagation. Runtime's existing renderer-tail positives will likewise still need the separately owned renderer carry.
- The existing three SDK invocation reserved-key negatives retain strict xfail and their original assertions. Reviewed d977 had a seven-line early reject_source_keys/error-mapping block in sdk/invocation.py after request_inputs; current invocation lacks it. Direct host and prepare_filmstrip guards are green; invocation currently raises raw ValueError for two keys and the older unsupported-product-input error for timeline_source. No invocation.py edit was made because the task allowed a narrow host port. Manager can authorize that exact guard port separately.
- Existing two SDK publication-double xfails stay: the double has no Runtime admission publisher. No assertion was weakened, skipped, deleted, or rewritten to bless missing behavior.

Initial diagnostic (superseded): three-file direct run produced 4 failures/88 pass/9 skipped/2 xfail. One was this worker's new equality test omitting the already-contractual parent_content_digest augmentation; corrected to compare the whole expected mapping. The other three exposed the pre-existing SDK invocation requirement above and its original strict-xfail markers were retained. Final closure file rerun: **23 passed / 5 retained strict xfailed in248.30s**, command `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_capture_closure_source.py`. Entire saved expansion and direct reserved-key guards pass. The two publication-double and three early-invocation requirements remain explicit strict xfails.

Exact central commands:

```bash
$ORCH/bin/request-test agt-m3-capture-provider-current commit-integration --files 'tests/sdk/test_capture_source_runtime.py'
$ORCH/bin/wait-test agt-m3-capture-provider-current-commit-integration-1020095215-3997 1
# Exit1: 2 default M1 contract-handshake failures, 23 capture passes, 4 retained renderer xfails.

$ORCH/bin/request-test agt-m3-capture-provider-current remotion-0012-nodes --files 'tests/packs/rendering/test_scene_source_carry.py tests/sdk/test_timeline_filmstrip_invocation.py'
$ORCH/bin/wait-test agt-m3-capture-provider-current-remotion-0012-nodes-1020095251-15088 1
# Initial waits exit124 while queued/running; do not resubmit.
```

Final scene-source verification (no renderer, browser or sockets; fixture builds and peer links are private):

```bash
ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0012/node_modules ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0012 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/rendering/test_scene_source_carry.py
# 59 passed in 48.99s, including every native node that the central lane could not set up.
```

The approved source unit is complete. Harness commit message and DONE are written; no Git/index/branch mutation or integration/shared-dependency write by this worker. Next: resolve the harness commit/tree, pair Runtime's independent 20-case comparison suite, and only then consider deleting the Agent duplicate verifier. Renderer carry, early SDK invocation guard and safe coordinated client repin remain separate owner work; none is claimed here.
