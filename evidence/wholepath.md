# D134 root-008 corrected whole-path source trace

Status: **CORRECTED EVIDENCE / UNKNOWN_UNAPPLIED / NOTRUN**.

The retained original review remains immutable and remains a FAIL on evidence quality. This derivative corrects only F-001 and F-002. It does not assert that the missing historical ABI-1 record exists.

## Public caller

The public Agent timeline API is `astrid/sdk/_remote_timeline.py:225-251`. It resolves the project/timeline scope, checks body identity, and submits the unchanged commit body through the typed `commit_timeline` operation. The generated-facing Agent client is `astrid/sdk/workspace_client.py:485-500`. The local `tests/editing_conformance/test_doc_patch_v2.py:45-50` helper is a detached provider harness, not the production public caller.

The Runtime public caller is `/home/user/work/runtime/runtime_protocol/server.py:300-340`. It authenticates the publisher, reads the request body and idempotency key, and calls `RuntimeService.commit_timeline`. `service.py:2468-2483` validates the canonical operation/body scope and enters `_execute_timeline_commit`.

## Runtime registration and invocation

Startup loads the selected provider at `/home/user/work/runtime/runtime_protocol/daemon.py:239-257`. `/home/user/work/runtime/runtime_protocol/timeline_commit_provider.py:70-93` imports the fixed Agent factory and validates the provider ABI. `/home/user/work/runtime/runtime_protocol/service.py:2412-2432` validates and installs that provider exactly once before serving requests.

`/home/user/work/runtime/runtime_protocol/service.py:2528-2559` builds the invocation context, selects the registered provider, and calls `CommitExecutionCoordinator.execute`. The private invocation boundary is `/home/user/work/runtime/runtime_protocol/timeline_commit_execution.py:365-401`, where the coordinator constructs a request-scoped port and invokes `provider.commit(provider_context, port)`. The port is `/home/user/work/runtime/runtime_protocol/timeline_commit_port.py:106-180`; its provider context is a detached copy, while its history/head/closure methods remain Runtime-owned.

## Agent capture, binding, and history

The Agent provider entry is `astrid/sdk/timeline/commit.py:1160-1190`. It validates the commands, captures producer/media inputs through the Runtime port, and loads the exact base/history boundaries. Native binding capture is `astrid/sdk/timeline/_recording.py:89-115`. `CommitPatch` selects v2 only when `doc.patch` or v2 controls are present at `astrid/sdk/timeline/_commit_patch.py:277-295`; physical binding enrichment occurs only in v2 at `:493-501`.

The history guard is `astrid/sdk/timeline/commit.py:770-922,997-1022`. It consumes the authenticated history entry supplied by the Runtime port, derives `recorder_abi` from that entry, and accepts the complete native four-binding ABI-1 shape only when the authenticated ABI is not 2. It fails closed for malformed ABI values and mixed/partial physical bindings. The private provider guard is called from `astrid/sdk/timeline/commit.py:1395-1398`.

The current source comparator at `tests/editing_conformance/test_provider_occurrence_fork.py:23-45` explicitly supplies v2 controls (`label`, `merge`, `reads`, `steps`, source, rationale, group) and asserts physical binding output. The root-008 ABI-1 cases intentionally omit those controls at `tests/editing_conformance/test_fork_abi1_binding_set.py:95-96`. Adding comparator controls would change the request ABI and authenticated history predicate; it is not a faithful correction.

## Runtime verified acceptance authority

Runtime validates the provider-produced records and physical-binding prerequisites at `/home/user/work/runtime/runtime_protocol/timeline_commit_store.py:1491-1540`. In `accept` at `:1832-1853`, after authorization, request/base/head checks, and validation of the exact returned records, Runtime derives `recorder_abi` from whether the accepted bindings contain physical references. It does not accept caller annotations as that authority.

The accepted result is assembled and passed to `_publish` at `:1878-1896`. `_publish` at `:2058-2089` writes the accepted event, request hash, recorder ABI, records digest, metadata, receipt, and immutable history edge in the acceptance transaction. Accepted history is independently checked at `:709-795`, including the records-to-document identity and authenticated recorder ABI fields.

## Finite conclusion

The current public caller and registered provider path is present and source-proved. Therefore the prior conclusion must not say that a missing retained historical payload proves an absent supported current caller. The smallest proved owner remains **Agent provider / Runtime producer-history custody seam**, classification **UNKNOWN_UNAPPLIED**. No product fault, behavior credit, legacy retirement, retry, alternate qualification, or historical-record reconstruction is supported.
