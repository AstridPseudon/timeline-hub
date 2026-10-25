# D136a finite boundary inventory

Static citation identity correction only. SAME2159 remains immutable. The 45 rows, nine selectors, six groups, 30 condition labels and 31 AST blocks are retained. Exact FunctionDef and Call spans are in table.json; call-site regions are explicitly distinguished from definitions.

| Group | AST-derived helper windows | Rows |
|---|---|---|
| MGC-01 | `astrid/core/timeline/authoring_bundle.py:185-244, 541-772, 775-820, 823-887, 948-997` | B005, B006, B007 |
| MGC-02 | `astrid/sdk/timeline/authoring_commit.py:190-325` | B008 |
| MGC-03 | `astrid/sdk/timeline/commit.py:1206-1398` | B014, B015 |
| MGC-04 | `runtime_protocol/timeline_commit_auth.py:18-264, 608-795, 1833-2335` | B021, B022, B023, B024, B025, B029, B032 |
| MGC-05 | `runtime_protocol/timeline_commit_auth.py:2338-2560` | B020, B026, B027, B028 |
| MGC-06 | `runtime_protocol/timeline_commit_store.py:1491-1565, 1567-1597, 1599-1761, 1764-1787, 1790-1829, 1832-1915` | B018, B019, B034 |

MGC-02/03/05 condition facts and MGC-03/05 primary windows remain unchanged; MGC-02 ends at actual EOF 325, not 335. MGC-03 contains call-site slices. Separate caller records use full AST definitions. command_output is 2189-2335, with the retained refusal at 2209.

| Boundary | Purpose | Actual status | Source windows |
|---|---|---|---|
| B001 | Collect the exact original9 and construct the same real saved closure for each case. | reached | `tests/sdk/test_timeline_capture_projection.py:280-441; tests/sdk/test_capture_source_runtime.py:155-301` |
| B002 | Ensure source commits use the registered provider and a real timeline rather than a synthetic fixture. | reached before current refusal | `tests/sdk/test_capture_source_runtime.py:216-217; runtime_protocol/timeline_commit_provider.py:55-67; runtime_protocol/timeline_commit_provider.py:70-93` |
| B003 | Establish real canonical records and closure used by saved_closure. | reached before current refusal | `tests/sdk/test_capture_source_runtime.py:251-301` |
| B004 | Create the physical authored source that later intermediate commands must observe. | reached before current refusal | `tests/sdk/test_timeline_capture_projection.py:301-353` |
| B005 | Reject malformed or cross-scope candidates before a Runtime commit request is emitted. | reached before current refusal | `astrid/core/timeline/authoring_bundle.py:1000-1031`; helpers MGC-01 |
| B006 | Compile only candidates with supported placement, source, shot, media and selection relationships. | reached statically; exact branch outcomes not separately recorded | `astrid/core/timeline/authoring_bundle.py:1033-1165`; helpers MGC-01 |
| B007 | Produce a self-consistent compiled candidate and final parent/manifest digest. | reached before current refusal | `astrid/core/timeline/authoring_bundle.py:1166-1404`; helpers MGC-01 |
| B008 | Read the exact base and emit canonical C0 commands, steps, merge, source and rationale. | reached before current refusal | `astrid/sdk/timeline/authoring_commit.py:24-81; astrid/sdk/timeline/authoring_commit.py:84-187`; helpers MGC-02 |
| B009 | Use the registered Runtime commit service and canonical invocation path. | entered, did not return accepted/merged | `tests/sdk/test_timeline_capture_projection.py:254-255; tests/sdk/test_timeline_capture_projection.py:257-260; tests/sdk/test_timeline_capture_projection.py:262-265; tests/sdk/test_timeline_capture_projection.py:267-268; tests/sdk/test_timeline_capture_projection.py:270-276; astrid/core/timeline/authoring_bundle.py:1833-1914` |
| B010 | Validate request shape, route identity, publisher, idempotency and authorization before coordination. | reached before current refusal | `runtime_protocol/service.py:2469-2483; runtime_protocol/service.py:2486-2559` |
| B011 | Resolve and validate the provider ABI before execution. | reached before current refusal | `runtime_protocol/timeline_commit_provider.py:55-67; runtime_protocol/timeline_commit_provider.py:70-93` |
| B012 | Coordinate one deterministic commit and reject mismatched duplicate/idempotency state. | reached before current refusal | `runtime_protocol/timeline_commit_execution.py:375-431` |
| B013 | Reauthorize and validate producer, dependency, captured closure, media and source inputs. | not dynamically reached after provider refusal | `runtime_protocol/timeline_commit_port.py:182-209; runtime_protocol/timeline_commit_port.py:530-618; runtime_protocol/timeline_commit_port.py:620-639` |
| B014 | Validate command semantics and obtain original/landing candidate records. | entered statically; exact internal return not separately recorded | `astrid/sdk/timeline/commit.py:1160-1205`; helpers MGC-03 |
| B015 | Require final candidate validity before sequential proof capture and port accept/preview. | not dynamically established for this request | `astrid/sdk/timeline/commit.py:1399-1444`; helpers MGC-03 |
| B016 | Create a private sequential proof only when required capture is available. | not dynamically reached after refusal | `astrid/sdk/timeline/_commit_preview.py:25-90` |
| B017 | Retain a shape/context-bound proof for later validation and clear it after operation. | not reached after current refusal | `runtime_protocol/timeline_commit_port.py:182-209` |
| B018 | Ensure destination/head and authorization are still valid before store validation. | not dynamically reached | `runtime_protocol/timeline_commit_store.py:1790-1808; runtime_protocol/timeline_commit_store.py:1832-1885`; helpers MGC-06 |
| B019 | Validate the whole request before durable preview/accept. | not dynamically reached | `runtime_protocol/timeline_commit_store.py:1491-1565`; helpers MGC-06 |
| B020 | Bind each provider command to a complete original-to-landing chain. | not dynamically reached to completion | `runtime_protocol/timeline_commit_auth.py:2563-2629`; helpers MGC-05 |
| B021 | Prepare authenticated physical observation before projecting command output. | reached before refusal | `runtime_protocol/timeline_commit_auth.py:2189-2207`; helpers MGC-04 |
| B022 | Require a physical observation at the authenticated ref before projecting an intermediate command. | refused | `runtime_protocol/timeline_commit_auth.py:2209-2209`; helpers MGC-04 |
| B023 | Require the input observation to equal the captured before image and project the result with matching mirror/digest. | not dynamically reached | `runtime_protocol/timeline_commit_auth.py:2213-2221`; helpers MGC-04 |
| B024 | Prevent ambiguous aliasing and require unique revision/parent/identity ownership during promotion. | not dynamically reached | `runtime_protocol/timeline_commit_auth.py:2222-2255`; helpers MGC-04 |
| B025 | Require exactly-one ownership and parent/manifest allocations before accepting the projected command output. | not dynamically reached | `runtime_protocol/timeline_commit_auth.py:2259-2335`; helpers MGC-04 |
| B026 | Validate the complete sequential envelope after individual command observations. | not dynamically reached | `runtime_protocol/timeline_commit_auth.py:2563-2629`; helpers MGC-05 |
| B027 | Require claims and bindings to correspond exactly and uniquely to source and landing images. | not dynamically reached | `runtime_protocol/timeline_commit_auth.py:2631-2699`; helpers MGC-05 |
| B028 | Prove replayable attribution, owner/image/destination/terminal/cross-history consistency. | not dynamically reached | `runtime_protocol/timeline_commit_auth.py:2701-2867`; helpers MGC-05 |
| B029 | Validate submitted C0 steps and their relationship to the captured sequential execution. | not dynamically reached | `runtime_protocol/timeline_commit_auth.py:2873-2947`; helpers MGC-04 |
| B030 | Require each step's effects and submitted patch to be covered by validated bindings. | not dynamically reached | `runtime_protocol/timeline_commit_auth.py:2943-2961; runtime_protocol/timeline_commit_auth.py:798-871` |
| B031 | Validate each step's declared reads, dependencies, effects and commands. | not dynamically reached | `runtime_protocol/timeline_commit_auth.py:382-487` |
| B032 | Validate exact binding identity and successor materialization for every effect. | not dynamically reached | `runtime_protocol/timeline_commit_auth.py:490-588`; helpers MGC-04 |
| B033 | Final C0 predicate: all provider step effects must reach the accepted closure. | not dynamically reached | `runtime_protocol/timeline_commit_auth.py:2962-2975` |
| B034 | Complete preview/accept and return canonical/base/landing/merge/receipt/records/bindings/effects/dependencies/history/undo fields. | not dynamically reached | `runtime_protocol/timeline_commit_store.py:1491-1565; runtime_protocol/timeline_commit_store.py:1790-1808; runtime_protocol/timeline_commit_store.py:1832-1885; runtime_protocol/timeline_commit_execution.py:375-431`; helpers MGC-06 |
| B035 | Reject any non-accepted/merged status and extract canonical document/head/manifest for projection. | not dynamically reached | `astrid/core/timeline/authoring_bundle.py:1883-1914` |
| B036 | Exercise the later exact saved-image transformations used by the original9 fixture. | not dynamically reached | `tests/sdk/test_timeline_capture_projection.py:407-441` |
| B-FINAL-001 | Require config, registry and full pin projection to equal the saved golden. | not dynamically reached | `tests/sdk/test_timeline_capture_projection.py:445-463` |
| B-FINAL-002 | Require entire expansion output to equal the saved golden. | not dynamically reached | `tests/sdk/test_timeline_capture_projection.py:467-477` |
| B-FINAL-003 | Require authored fields, pins, ordering and read rows to survive canonical projection. | not dynamically reached | `tests/sdk/test_timeline_capture_projection.py:481-529` |
| B-FINAL-004 | Require parent candidate projection to match SDK opener exactly. | not dynamically reached | `tests/sdk/test_timeline_capture_projection.py:534-569` |
| B-FINAL-005 | Require child candidate projection to match SDK opener exactly. | not dynamically reached | `tests/sdk/test_timeline_capture_projection.py:534-569` |
| B-FINAL-006 | Require new_shot candidate projection to match SDK opener exactly. | not dynamically reached | `tests/sdk/test_timeline_capture_projection.py:534-569` |
| B-FINAL-007 | Require duplicate candidate projection to match SDK opener exactly. | not dynamically reached | `tests/sdk/test_timeline_capture_projection.py:534-569` |
| B-FINAL-008 | Require remove candidate projection to match SDK opener exactly. | not dynamically reached | `tests/sdk/test_timeline_capture_projection.py:534-569` |
| B-FINAL-009 | Require sdk_bundle candidate projection to match SDK opener exactly. | not dynamically reached | `tests/sdk/test_timeline_capture_projection.py:534-569` |

**B022:** observed current Runtime fail-closed refusal; regression/causal owner UNKNOWN; setup failure/D54a REG NOT_PROVED. No guard relaxation or product fix is authorized. B023-B036 and all nine final predicates remain UNKNOWN/unreached.

Original2136: nine collected, nine setup ERROR, zero passes/failures/skips, exit 1. Independent2144 source custody PASS is retained, together with its overall NO_GO. Pristine886a absence is source absence only. All D130 holds remain. ONE final independent static check remains before the manager sends the controlling list to Runtime/App leads.
