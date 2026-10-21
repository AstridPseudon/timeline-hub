# PRIVATE017 exact matched proof preflight

Date: 2026-10-21. Worker: rt-m2-private017-c964-complete-proof-preflight-0832.

## Result

The Runtime-owned ordered/RT03 proof is ready as a collection-verified,
exact-matched proposal. Both Runtime nodes collect exactly as intended. No
test body ran. Execution remains held until independent Agent review0824
approves the normal Agent pin c964f73cbae2e01cd6461891a966f4784a1e5b9a and
tree f5cf91780e5bd7d3b4b527bc75a178c1daf3b985. The normal pin is staged, not
approved; this is the explicit execution blocker.

## Exact source, pins, and cleanliness

Runtime worker/base:
  checkout /home/user/work/wt/rt-m2-private017-c964-complete-proof-preflight-0832
  commit aa0c26e0dafc6a749a1c8aae5ccfe971a1ce27d4
  tree 09699414ff8ca79f3e9146b44b5713a10b8ef132
  status clean

Runtime producer:
  checkout /home/user/work/wt/rt-pin-42a7203f
  commit 42a7203f49bb89f299ec854cfbf2b1444e815a7c
  tree 1f220b3d3a27e8eb061b15c944bad784c8fdb82e
  status clean

Agent normal consumer:
  checkout /home/user/work/wt/agt-pin-c964f73c
  commit c964f73cbae2e01cd6461891a966f4784a1e5b9a
  tree f5cf91780e5bd7d3b4b527bc75a178c1daf3b985
  status clean; staged, review pending

The worker base has only the expected compact ordered-test commit relative to
its parent: git diff --name-status HEAD^ HEAD reports
M tests/test_timeline_owned_reference_integration.py. No product, test,
generation, pin, schema, or suite file was changed by this preflight. No
frozen R4 reference branch was checked out or modified.

Frozen Agent schema provenance: commit ed5fd33c4a7fa9956178f9b24eb127415eaca9e,
tree f4a632e4f627499e0b15d8477db9aaab78ebb3d2, source
astrid/core/timeline/schema/edit-command.schema.json.

## Schema, artifacts, and locked bytes

Read-only schema preflight output:
  raw_sha256=6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16
  canonical_sha256=9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6
  definitions=65
  editcommand_clauses=37

Canonicalization is the Runtime convention: SHA-256 of
json.dumps(schema, ensure_ascii=False, indent=2) plus a final newline.

Exact producer/normal-consumer tuple:
  package 0.2.17
  health/schema sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd
  raw bundle sha256:e6fb80e7961b3e9eb34908b532a042a9f024e52b5178cd906d9c1d45a18a5f8f
  artifact version sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0
  artifact manifest file sha256:0c0e3379302f5ded0bef96d9a5c7d7e72a29962d83bbb5b1500c0cfd7344e06f
  component manifest sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5
  producer artifacts 76
  schema shape 65 definitions / 37 EditCommand clauses

Exact lock check command:
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B /home/user/work/wt/agt-pin-c964f73c/scripts/vendor_lock.py check /home/user/work/wt/agt-pin-c964f73c/runtime.lock.json --producer /home/user/work/wt/rt-pin-42a7203f

Result: ok runtime.lock.json (matches producer manifest).
All 15 normal lock entries matched their producer bytes. Exact hashes:
  astrid/core/timeline/schema/timeline-config.schema.json  f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1
  astrid_runtime_client/__init__.py                       7e602716931ca03930e1801596e098b83aa7344b7c54fe34b26e2308f82f15b2
  astrid_runtime_client/contract_metadata.py               e6d8286ca342bbb7a7d6554bb37357548b95bf2df123e7d46f60d6fce8fe53b1
  astrid_runtime_client/generated.py                       e58f0fbe652b2baf8a3cd113def468dde3b32d1522f946a733c2b2a3b8461350
  astrid_runtime_client/timeline_commit_types.py           af295393450db831c43e6559eb0aa8f645e6cd0e79f4beb078df949bdb58e0d3
  events_page_1_200.json                                   6aaaabe512589beddddd5ef64f2307c39d365a99565c5a3291a15933a114be0d
  events_page_2_200.json                                   d5bffdc93e9939779c92a18c047e70df21711f12e16c345f43f3cbdec5b27eb2
  invalid_cursor_400.json                                  16a1db399e06b8d059472f567a091b4bd579d13d8885595376f61835646bfbff
  managed_outputs_200.json                                 6bcef19aca4ad8d574c60d738b54ba57fce6a3a9d4e1481c6f8f088dd460858d
  not_found_404.json                                       4a40fedbeccd345f24944e4af368c50430593d976a923c12af93ba21af6
  publish_conflict_409.json                                19d664d035691202da03b22b858456c49983e253c7485a6347baa1cf350eea57
  task_admission_201.json                                  108559a92c9e681e3ade37fa6b567e1eaac3edce221665a07a81c2c2c06bb48c
  task_read_200.json                                       cc590c4f7d34820382b684d737f1cdb45eebeb20fbad2d5edda2dadac8ab2829
  validation_error_422.json                                2a02a9147bc0a8b74727d9c577803b0aca333bd0dd035602dafcf2503b00ff1a
  visual-boundary-v1.json                                  1fc778b42f7a5ef91a1fd8620fd92417131e44f97dd5c6a238c78f13bcabfc55

The optional carrier is exact: Runtime Python uses
AgentWrite insertion_order: NotRequired[list[str]]; TypeScript uses
insertion_order?: Array<string>. Absent is accepted; null and non-string
members are refused. Producer and normal Agent metadata agree on component
manifest sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5
and schema digest sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd.

## Imports, authoring profile, dependencies, and storage

Read-only imports from the normal Agent environment:
  astrid=/home/user/work/wt/agt-pin-c964f73c/astrid/__init__.py
  astrid.sdk.timeline=/home/user/work/wt/agt-pin-c964f73c/astrid/sdk/timeline/__init__.py
  astrid_runtime_client=/home/user/work/wt/agt-pin-c964f73c/astrid_runtime_client/__init__.py
  runtime_protocol=/home/user/work/wt/rt-m2-private017-c964-complete-proof-preflight-0832/runtime_protocol/__init__.py
  contract_version=0.2.17
  client_schema_digest=sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd

Supported authoring profile is astrid. Runtime declares jsonschema>=4.18 and
referencing>=0.30; Agent includes filelock, Pillow, jsonschema, referencing,
and PyYAML. The existing Runtime venv has pytest/jsonschema/referencing/yaml
but lacks filelock and PIL; the existing Agent venv has the provider
dependencies. The Agent venv is therefore required for truthful collection
and proposed execution. No shared venv was installed or modified.

Shared worktrees, venvs, and node_modules were read-only. realpath showed the
referenced worktrees and venvs are direct paths, not symlink aliases into a
shared install. Collection used PYTHONDONTWRITEBYTECODE=1 and
-p no:cacheprovider; no output or temp files remain in this worktree. Future
body execution must use pytest private tmp_path and the central test service.
Storage: df -h /home/user/work /tmp reported /dev/vda, 252G total, 29G used,
11G available, 74%, for both paths.

## Runtime nodes and collection

Only these original owned-raw reference and new ordered/remove/lost-ACK/
restart/exact-retry/inverse/redo nodes are in scope:
  1. tests/test_timeline_owned_reference_integration.py::test_actual_provider_preserves_original_owned_unplaced_reference_contract
  2. tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo

Collection-only command, run from the Runtime worker; no body:
env ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-c964f73c PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-c964f73c" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --collect-only -m integration tests/test_timeline_owned_reference_integration.py::test_actual_provider_preserves_original_owned_unplaced_reference_contract tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo

Result:
  tests/test_timeline_owned_reference_integration.py::test_actual_provider_preserves_original_owned_unplaced_reference_contract
  tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo
  2 tests collected in 0.42s

Node 1 accepts the original owned/unplaced raw reference through the normal
RuntimeService direct-provider commit door, then checks restart, changed same-key
refusal, foreign/occupied atomic refusal, and exact inverse removal. Node 2
removes ordered project data, checks exact app/order/writes, restarts, exact
retries with provider execution forbidden and unchanged SQL/history, then checks
inverse and inverse-of-inverse redo. Both are direct-provider acceptance, not
HTTP transport.

## Proposed Runtime manager command (not run)

After the independent pin verdict, repeat the collection guard and require
2 tests collected, then run exactly:
env ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-c964f73c PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-c964f73c" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_timeline_owned_reference_integration.py::test_actual_provider_preserves_original_owned_unplaced_reference_contract tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo

This command was not run here. No named suite was added to suites.conf.

## Existing Agent v2 lifecycle node for later qualification

The smallest existing real-provider v2 materialization node in exact Agent c964
is:
tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry[image-add]

Its existing parameter set is image-add, image-swap, video-add, video-swap;
only image-add is proposed. It covers real media selection, accepted v2
capture, created owner/asset, restart, exact same-key retry with execution
forbidden, undo, redo, identity collision, changed same-key refusal, and store
integrity. It does not explicitly assert the complete accepted v2 source/map/
owner boundary (no explicit id-map/source-map assertion), and is not HTTP
transport; it is a later candidate, not qualified here.

The requested HTTP example also exists separately:
tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_semantic_batch_original_pins_reload_inverse_redo[python].
Its four parameters use the real HTTP handler with in-memory MemorySocket,
not actual sockets; it checks pins, command equality, accepted state,
restart/reload, inverse/redo, but not v2 materialization source/map/owner or
lost-ACK retry. Do not conflate it with the direct-provider candidate.

Agent candidate collection command, no body:
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-42a7203f PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-pin-c964f73c:/home/user/work/wt/rt-pin-42a7203f /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --collect-only -m integration tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_semantic_batch_original_pins_reload_inverse_redo

Result: 8 collected (four direct-provider and four HTTP parameters); no bodies ran.

Separate Agent suite proposal, not run and held on the pin verdict:
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-42a7203f ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-c964f73c PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-pin-c964f73c:/home/user/work/wt/rt-pin-42a7203f /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry[image-add]

Preserve these mapped old-v1 refusal/current-v2 source tests:
  V01 refusal: tests/editing_conformance/test_recipe_m2_placement.py::test_private_carrier_placement_v1_refuses_without_refreshing_original_claims
  V01 v2: tests/editing_conformance/test_recipe_m2_placement.py::test_parent_and_occurrence_golden_capture_replay_reload_inverse_redo[fixture_path1]
  V02 refusal: tests/editing_conformance/test_recipe_occurrence_media.py::test_private_carrier_swap_v1_refuses_without_refreshing_original_claims
  V02 v2: tests/editing_conformance/test_recipe_occurrence_media.py::test_portable_goldens[swap-fixture_path2]
  V03 refusal: tests/editing_conformance/test_recipe_occurrence_media.py::test_obsolete_carrier_add_v1_refuses_original_claims_with_draft_kept
  V03 v2: tests/editing_conformance/test_recipe_occurrence_media.py::test_obsolete_carrier_add_equivalent_reauthored_v2_succeeds

Their collection-only selection returned 9 collected (parameterization accounts
for the count); no bodies ran. No new test or matrix was added and no old44/186
replay was performed.

## Blockers and handoff

- Independent Agent review0824 pin verdict is missing/active; c964 remains staged
  only. This is the execution blocker.
- Runtime venv lacks Agent provider filelock and PIL; use existing Agent venv.
  Do not install or modify shared dependencies.
- No Runtime/Agent semantic body, HTTP/socket/native/full/browser/render/
  install operation ran. Evidence is collection and provenance only.
- Manager must repeat the positive two-node collection guard and run the Runtime
  command only after pin approval. Keep the Agent candidate separate and
  preserve all three v1 refusal/current-v2 mappings.

