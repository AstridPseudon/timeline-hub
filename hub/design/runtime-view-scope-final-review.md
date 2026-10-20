# Persisted-view authority final review

**REJECT `9db719c2f8bc24308c2506c3b61d4620bb1c6b2e` relative to `642eef7`: one P2 client-generator defect must be corrected.** The bounded server/service authority correction and retained-view behavior passed this review. This verdict does not authorize integration, publication, pin changes, or the current final tuple.

Reviewed exact candidate tree `b7993c7d87913874ad28683a961adaa2ff6aa780`, matching the implementation worker's central test tree. Read PLAN, COMMON, Runtime manager STATUS and INBOX (especially approved 09:38Z decision), the worker Report.md, dedicated runtime-view-write-scope-handoff.md, and runtime-current-tuple.md. No settled decision was changed.

## Ranked finding

### P2 — normal TypeScript conformance generation still produces a keyless persisted-view client

**Scenario:** Generate the second TypeScript client normally, then use its advertised `createTimelineView` with write authority. The generated method cannot accept a key in TypeScript and never sends one. Every such call reaches the corrected server without `Idempotency-Key` and is refused with 400.

**Exact source proof at the reviewed SHA:**
- `tools/generate_typescript_conformance.mjs:359–360` still defines `createTimelineView(projectId, timelineId, options = {})` and sends only Content-Type.
- Its normal output `conformance/typescript/generated.ts:196–197` has that same signature/header omission.
- In contrast, `packages/typescript/src/generated.ts:185` requires the fourth `idempotencyKey` and forwards it; `generators/python_client_template.py` and its Python output require the keyword key.
- The candidate changed the conformance output's digest stamp, but left this method and its generator unchanged.

**Independent reproduction:** private transport-only probe passed for the package TypeScript client and failed for the conformance client: expected header `view-key`, actual `undefined`. Private compile probe reported both TS2578 (missing-key call wrongly accepted, making the expectation directive unused) and TS2554 (keyed four-argument call rejected). No socket, browser or shared-cache write was involved.

**Required correction:** update the normal conformance generator method to require/forward the key, regenerate its output normally, and add meaningful transport and missing-key type coverage for this second client. Preserve the plain response. Re-run the narrow checks on the corrected source and have the final release composer include it. Do not patch just the generated output. All three generator/hash checks passed on this defective candidate, so those checks alone cannot close this finding.

## Source behavior accepted within scope

| Requirement / concrete scenario | Review result and source proof |
|---|---|
| Reader attempts artifact persistence, with or without a key | `runtime_protocol/server.py:585–587` authenticates projects:write before options/key/service execution. Private actual-handler/CredentialStore probes refused readers and left SQLite dump, total_changes, CAS and staging identical; ingest was a fail-fast trap. Existing central actual HTTP negatives were inspected, not rerun. |
| Writer omits, empties or corrupts key | Same handler validates key before entering service; `service.py:2556` additionally requires it before project lookup/inspection/ingestion. Private handler negatives passed with no persistence. The durable service decorator opens a transaction before the method; the HTTP boundary rejects before that call. |
| Reader uses inspect | `server.py:582–584`, `service.py:2547–2551`: read authority, no key, pure closure inspection. Successful private control left the same complete snapshot unchanged. |
| Changed request reuses a timeline/key | `service.py:2558–2561` hashes canonical project ID, timeline and raw options; `service.py:1887–1916` checks the hash before inspection/render/ingest. Changed-format probe conflicted without writes. Omitted options and {} intentionally identify the same request. |
| Wrong project / stale key cannot replay another project's view | Canonical project ID participates in the hash; wrong project with the old timeline/key conflicts rather than replaying; a fresh key reaches `timeline_inspection.py:554`'s project/timeline ownership SELECT and returns not_found. Both private controls made no writes. |
| Cross-project collisions | Timelines have globally unique IDs: `service.py:1656–1675` checks ID existence without project and inserts the globally keyed row. Thus two valid projects cannot share one timeline aggregate. Equal caller keys on distinct valid timeline IDs are separate aggregate namespaces, consistent with the existing command replay seam; no cross-project response substitution occurs. This is not a promise of globally single-use keys. |
| Actor binding / credential downgrade | The handler reauthenticates write scope before every replay. Actor is deliberately absent from view request identity; CredentialStore scopes are workspace-wide (`auth.py:239–243`), and views use ordinary aggregate/key replay, not commit publisher attribution. Another write-authorized actor can replay the same request; a reader cannot. No actor-private or project-bound credential guarantee is claimed. |
| Lost ACK, head advance, restart, exact retry | Service replay precedes inspection. Independent combined scenario saved MD+PNG, advanced parent-1 to parent-2, reopened RuntimeService and retried the original request: original result/bytes returned, no ingest or SQL/CAS changes. Existing result-equality comparison deliberately uses decoded response semantics; raw HTTP JSON byte ordering was not separately tested. |
| 24-hour replay window, retained bytes | Existing `_command_replay_state` passes the view timestamp to `idempotency.command_result`; 24-hour policy is unchanged. Private expired-row probe raised IdempotencyWindowExpired without re-execution or writes; both artifact bytes and verified project custody remained readable. No new table/journal was added. Existing generic CAS publication recovery is reused. |
| Cross-key dedup/custody | Artifact-key derivation and ingestion body are unchanged (`service.py:2576–2586`). Re-ran main-suite MD/PNG custody/dedup test: same view under another key retains the same objects and exact renderer bytes; restart reads remain verified. |
| Restored compatibility publication docs | OpenAPI description matches `service.py:2735–2780`: valid successful retry first, otherwise tracked head requires commands; untracked head must match expected_head; headless/fresh null-head publication must pass timeline_scope_is_empty, including legacy project documents. Stable reasons timeline_commit_required/stale_head/headless_content_not_empty are accurate. Eligibility remains subject to all existing shape, scope, closure and occupancy guards. |
| Main owner-token refresh cannot bypass new scope gate | Candidate diff does not touch daemon/auth/door. Review worktree HEAD `a5a4f6b` includes main refresh: `daemon.py` removes worker_token=owner-token alias, rotates/provisions real worker credentials, and WORKER_SCOPES omits projects:write. The view handler requires projects:write/admin and has no worker exception. Candidate's older fixture convenience is not a change to port back. Final composed source still needs verification; no composed runtime/socket claim is made. |
| Python/package TS/OpenAPI generation and all manifest hashes | Required-key signatures agree for Python and package TS with OpenAPI. Normal generate.py --check, conformance generator --check, and artifact_manifest.py --check all exited 0; all 74 manifest artifacts matched. Repository convention treats package TypeScript source as its authoritative generator input; this review does not introduce another template. The separate conformance generator defect above remains. |

## Caller inventory checked against current production source

Read-only integration snapshots during this review: Agent `ba5f2756f50a84f570aa9699ef621873f7521abc`; App `7bb885b638838588a0dff81b64b7c34960ac07f3`. The handoff's older snapshots were not treated as current readiness evidence. Re-searched production sources for Python/TS method names, raw /views routes and .visualize invocations.

The dedicated handoff remains complete for the searched production source:
- Agent `astrid_runtime_client/generated.py:932–934`: copied old keyless client.
- Agent `astrid/sdk/workspace_client.py:555–564`: old facade has no key; `_call_generated` allow-list at :243 includes it.
- Agent `astrid/sdk/remote.py:327–330,382`: view remains in reads, suppressing generic key allocation, and its dispatch forwards no key.
- Agent public `RemoteTimelines.visualize` at :796, native inputs dispatch :1013: no explicit view retry key.
- Agent CLI `astrid/packs/timeline/cli_visualize.py:271,291,888`: the same three visualization calls. Comparison auto/composed captures do not directly invoke persisted views; shared inputs fallback must receive the corrected dispatch.
- App `src/integrations/runtime/generated.ts:181`: old optional-options/no-key method. No production endpoint invocation beyond this method was found. `client.ts` constructs the generated client; requested scopes already include projects:write. Editor createTimelineViewStore/createTimelineViewportStore calls are local state factories.
- Browser door `runtime_protocol/door.py:157–165` still allow-lists inspect/commit/publication, with no views route. No new door capability was inferred.

**Agent caller port readiness is not established and current inspected callers are still keyless.** Their owner must port generated copy, facade, read classification, mutation dispatch and stable logical-request retry identity together; then qualify native SDK/CLI behavior. App owns its generated-copy/pin/typecheck update. No other repository or pin was edited.

## Evidence, limitations and disposition

Independent results: four selected main-suite cases passed; three private service/handler scenarios passed (two existing imported integration-marker warnings); TypeScript transport comparison was 1 pass/1 reproducible failure; compile probe produced the two expected defect diagnostics. Exact commands are in the worker DetailedReport.md and the probe files.

Inspected prior central summaries on this exact candidate tree: targeted run 1657 passed/58 fixture setup errors, corrected configured fixture run 58 passed, commit integration 9 passed, package TS build/typecheck/18 tests passed. These are bounded unit/integration evidence. They neither test the missing second-client key nor qualify the refreshed/composed current tuple.

No broad repeat, full suite, live socket/browser run, central request, merge request, publication or pin edit occurred. No product source was modified. The independent review result is complete, so DONE is appropriate; the finding and external caller/release prerequisites are not a blocker to completing this assigned review.

**Next:** correct the P2 normal-generator gap, obtain a narrow successor review, and wait for qualified Agent caller readiness before composing/publishing the one final new release with F1/F2, main refresh and the other reviewed release changes. Staging 0.2.11/0.2.12/0.2.13 and old central counts are not final publication approval. Earlier public 0.2.9/0.2.10 remain affected as already recorded.

