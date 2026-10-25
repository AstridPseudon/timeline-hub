# D134 root-008 final independent check

Result: **PASS_FINITE_UNAPPLIED**. Behavior status: **NOTRUN**.

## F001 — resolved

The corrected predicate map has the authoritative root-008 full node IDs in both `cases` and `exact_member_index`. Independent comparison with `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agt-F-D134-root-clusters-2022-root-clusters.json` is an exact raw multiset match: 18 members, no duplicates, no omissions, no extras, and no normalization.

## F002 — resolved

The current caller/provider path is source-proved with concrete citations:

- Agent public caller: `astrid/sdk/_remote_timeline.py:225-251` and generated-facing `astrid/sdk/workspace_client.py:485-500`.
- Runtime public route and canonical invocation: `/home/user/work/runtime/runtime_protocol/server.py:300-340` and `service.py:2468-2483,2528-2559`.
- Startup provider load/registration: `/home/user/work/runtime/runtime_protocol/daemon.py:239-257`, `timeline_commit_provider.py:70-93`, and `service.py:2412-2432`.
- Provider boundary and request port: `/home/user/work/runtime/runtime_protocol/timeline_commit_execution.py:365-401` and `timeline_commit_port.py:106-180`.
- Agent capture, v2 binding enrichment, and authenticated history guard: `astrid/sdk/timeline/_recording.py:89-115`, `_commit_patch.py:277-295,493-501`, and `commit.py:770-922,997-1022,1160-1190,1395-1398`.
- Runtime verified acceptance and persistence authority: `/home/user/work/runtime/runtime_protocol/timeline_commit_store.py:1491-1540,1832-1853,1878-1896,2058-2089`.

The missing retained historical payload is not evidence that the current caller is unsupported. No historical record, receipt, binding, closure, or ABI was fabricated.

## Remaining finite conclusion

The retained failure still lacks the authenticated historical ABI-1 Runtime record, canonical predecessor/output closures, `records.commands[0].bindings`, `recorder_abi`, and exact history boundary fields needed to attribute the failure. The smallest proved seam remains **Agent provider / Runtime producer-history custody**. Classification is **UNKNOWN_UNAPPLIED**; there is no product-fault, behavior, or retirement credit.

## Conservation

Both owned test files are byte-identical to Agent base `96a6b2deea46eb33ba5184203a10e966cc5e9179`, and all function-body ASTs are identical. The ABI-1 request omission and original negative purposes remain unchanged. The Runtime trace used `cf0b82dd47452a7a34fc63eb233e9b1dc0532806`; every cited Runtime product file is byte-identical to immutable Runtime `ab1e4f6141987706132916e2da16477f5a019464`. The only `cf0b` deltas are the permitted helper/test-only files `tests/helpers/p2_commit_phase_capture.py` and `tests/test_p2_commit_phase_capture.py`.
