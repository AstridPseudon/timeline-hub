# D136a whole-path boundary map

This is a static trace of the exact original9 through selector initialization, the real saved-closure fixture, Agent authoring compilation, the registered Runtime caller, C0 validation, projection, acceptance, and each final predicate. The complete machine-readable rows, including original inputs, predicate purpose, conditions, evidence status, source comparison, classification, missing records, and owner, are in `table.json`.

The only dynamic evidence is the retained final20db run: 9 collected, 9 setup errors, 0 failures/passes/skips, exit 1. Every selector stopped at `runtime_protocol/timeline_commit_auth.py:2209` with `provider intermediate command lacks an authenticated physical observation`. Therefore rows after B022 are statically enumerated and explicitly marked unreached/UNKNOWN; they are not fabricated outcomes. No dynamic exhaustiveness claim is made.

| Path | IDs | Static boundary | Exact source | Existing evidence | Classification |
|---|---|---|---|---|---|
| P1 fixture | B001 | Selector collection, saved_closure construction | `tests/sdk/test_timeline_capture_projection.py:280-441`; `tests/sdk/test_capture_source_runtime.py:155-301` | Reached by prior exact run | setup prerequisite passed |
| P1 fixture | B002 | Registered provider and timeline | `tests/sdk/test_capture_source_runtime.py:216-217`; `runtime_protocol/timeline_commit_provider.py:55-93` | Reached | setup prerequisite passed |
| P1 fixture | B003 | Real setup C0 commits | `tests/sdk/test_capture_source_runtime.py:251-301` | Reached | setup prerequisite passed |
| P1 fixture | B004 | Physical source patch and canonical reload | `tests/sdk/test_timeline_capture_projection.py:301-353` | Reached | setup prerequisite passed |
| P2 compile | B005 | Candidate schema/scope/base/derived-occurrence guards | `astrid/core/timeline/authoring_bundle.py:1000-1031` | Reached | product guard passed for observed input |
| P2 compile | B006 | Placement/source/shot/media/selection guards | `astrid/core/timeline/authoring_bundle.py:1033-1165` | Source-known; branch result not separately recorded | UNKNOWN branch outcome |
| P2 compile | B007 | Child, identity, digest, placement, parent and manifest guards | `astrid/core/timeline/authoring_bundle.py:1166-1404` | Reached | product guard passed for observed input |
| P2 request | B008 | Base read, membership, media and C0 request construction | `astrid/sdk/timeline/authoring_commit.py:24-187` | Reached | product guard passed for observed input |
| P2 caller | B009 | Authoring writer and accepted/merged response shape | `tests/sdk/test_timeline_capture_projection.py:251-276`; `astrid/core/timeline/authoring_bundle.py:1833-1914` | Entered; refusal returned | downstream Runtime REG |
| P3 service | B010 | Detached body, route, publisher, idempotency and auth | `runtime_protocol/service.py:2469-2559` | Reached | guard passed for observed input |
| P3 provider | B011 | Provider ABI/load | `runtime_protocol/timeline_commit_provider.py:55-93` | Reached | guard passed for observed input |
| P3 coordinator | B012 | Context, hash, idempotency and response shape | `runtime_protocol/timeline_commit_execution.py:375-431` | Reached before later refusal | guard passed for observed input |
| P3 port | B013 | Auth, producer/dependency, captured closure/materializations | `runtime_protocol/timeline_commit_port.py:182-209, 530-639` | Static only | UNKNOWN downstream product boundary |
| P3 Agent execution | B014 | Command validation and provider capture | `astrid/sdk/timeline/commit.py:1160-1205` | Static/record incomplete | UNKNOWN internal boundary |
| P3 Agent execution | B015 | Final candidate and prepared execution | `astrid/sdk/timeline/commit.py:1399-1444` | Static only | UNKNOWN product boundary |
| P3 proof | B016 | Sequential proof availability and construction | `astrid/sdk/timeline/_commit_preview.py:25-90` | Static only | UNKNOWN product boundary |
| P3 port | B017 | Private capture shape/context | `runtime_protocol/timeline_commit_port.py:182-209` | Static only | UNKNOWN product boundary |
| P3 store | B018 | Store preview/accept preflight | `runtime_protocol/timeline_commit_store.py:1790-1808, 1831-1885` | Static only | UNKNOWN product boundary |
| P3 store | B019 | Canonical scope, records, steps, history and sequential proof | `runtime_protocol/timeline_commit_store.py:1491-1565` | Static only | UNKNOWN product boundary |
| P3 C0 | B020 | Sequential envelope, images and chain | `runtime_protocol/timeline_commit_auth.py:2563-2629` | Static only | UNKNOWN product boundary |
| P3 C0 | B021 | Manifest and created-root prelude | `runtime_protocol/timeline_commit_auth.py:2189-2207` | Reached | guard passed for observed input |
| P3 C0 | **B022** | **Authenticated physical observation** | **`runtime_protocol/timeline_commit_auth.py:2209`** | **Proven refusal for all nine** | **product REG; Runtime guard** |
| P3 C0 | B023 | Before-image equality, projection, mirror and digest | `runtime_protocol/timeline_commit_auth.py:2213-2221` | Static downstream | UNKNOWN |
| P3 C0 | B024 | Changed-image binding, alias, physical identity and identity scope | `runtime_protocol/timeline_commit_auth.py:2222-2255` | Static downstream | UNKNOWN |
| P3 C0 | B025 | Owner, parent pin, next-read, root and manifest allocation | `runtime_protocol/timeline_commit_auth.py:2259-2335` | Static downstream | UNKNOWN |
| P3 C0 | B026 | Original/landing envelope and exact chain | `runtime_protocol/timeline_commit_auth.py:2563-2629` | Static only | UNKNOWN |
| P3 C0 | B027 | Claims and binding correspondence | `runtime_protocol/timeline_commit_auth.py:2631-2699` | Static only | UNKNOWN |
| P3 C0 | B028 | Replay bindings, reads, source chain and ownership | `runtime_protocol/timeline_commit_auth.py:2701-2867` | Static only | UNKNOWN |
| P3 C0 | B029 | Batch reads, manifest evolution, atomic scope, sequential equality | `runtime_protocol/timeline_commit_auth.py:2873-2947` | Static only | UNKNOWN |
| P3 C0 | B030 | Step output, step validation and patch coverage | `runtime_protocol/timeline_commit_auth.py:2943-2961`; `:798-871` | Static only | UNKNOWN |
| P3 C0 | B031 | Reads, dependencies, special assertions and submitted patch | `runtime_protocol/timeline_commit_auth.py:382-487` | Static only | UNKNOWN |
| P3 C0 | B032 | Binding identity, aliases, images, owners and successors | `runtime_protocol/timeline_commit_auth.py:490-588` | Static only | UNKNOWN |
| P3 C0 | B033 | Provider effects reach accepted closure | `runtime_protocol/timeline_commit_auth.py:2962-2975` | Static only | UNKNOWN |
| P4 store | B034 | Projection, materialization, durable receipt/history/undo | `runtime_protocol/timeline_commit_store.py:1491-1565, 1790-1808, 1831-1885`; `runtime_protocol/timeline_commit_execution.py:375-431` | Static only | UNKNOWN |
| P4 caller | B035 | Accepted/merged response and canonical extraction | `astrid/core/timeline/authoring_bundle.py:1883-1914` | Static only; refusal instead | UNKNOWN |
| P4 fixture | B036 | Reload, duplicate/remove and final candidate publication | `tests/sdk/test_timeline_capture_projection.py:407-441` | Not reached | downstream fixture boundary, not proven setup failure |
| P4 final | B-FINAL-001 | Config/registry/full-pins golden | `tests/sdk/test_timeline_capture_projection.py:444-456` | Body not reached | UNKNOWN |
| P4 final | B-FINAL-002 | Entire expansion golden | `tests/sdk/test_timeline_capture_projection.py:459-468` | Body not reached | UNKNOWN |
| P4 final | B-FINAL-003 | Authored fields, pins, order and read rows | `tests/sdk/test_timeline_capture_projection.py:471-529` | Body not reached | UNKNOWN |
| P4 final | B-FINAL-004 | Exact opener: `[parent]` | `tests/sdk/test_timeline_capture_projection.py:532-569` | Body not reached | UNKNOWN |
| P4 final | B-FINAL-005 | Exact opener: `[child]` | `tests/sdk/test_timeline_capture_projection.py:532-569` | Body not reached | UNKNOWN |
| P4 final | B-FINAL-006 | Exact opener: `[new_shot]` | `tests/sdk/test_timeline_capture_projection.py:532-569` | Body not reached | UNKNOWN |
| P4 final | B-FINAL-007 | Exact opener: `[duplicate]` | `tests/sdk/test_timeline_capture_projection.py:532-569` | Body not reached | UNKNOWN |
| P4 final | B-FINAL-008 | Exact opener: `[remove]` | `tests/sdk/test_timeline_capture_projection.py:532-569` | Body not reached | UNKNOWN |
| P4 final | B-FINAL-009 | Exact opener: `[sdk_bundle]` | `tests/sdk/test_timeline_capture_projection.py:532-569` | Body not reached | UNKNOWN |

## Classification and handoff

Only B022 is a proven product REG: the immutable Runtime source actively refuses a missing authenticated physical observation. No setup failure is proved. The exact missing ref/path/ordinal/result record is withheld, so the upstream producer attribution remains UNKNOWN. The located D54a paired-cause qualification is not evidence for this path: it qualifies zero rows and preserves causes as open/unproven. Runtime should address every proved product item in one pass after this list is accepted; App does not change source or fixtures in this review.
