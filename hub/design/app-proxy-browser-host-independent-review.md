# Independent browser operation host review

**APPROVE the inactive, same-origin browser-host unit at `be27b45066947e920cda8da67991976b432ccb33`. Activation remains HOLD.** No blocking defect found within the agreed immediate-fetch/local-lifetime boundary. Native capture, actual proxy/socket behavior and real Runtime acceptance/replay remain open; neither the historical nor reproduced 244-test pass activates anything.

Reviewed PLAN first, `runtime-app-proxy-operation-agreement.md`, `app-proxy-lifetime-proposal-review.md`, browser implementation design, and the implementation worker's actual `Report.md` (`workerReport.md` was absent). Runtime's 10:11 agreement supersedes the earlier proposal review's agreement hold. No settled decision was changed.

## Exact source and scope

- Target: `tl/app-m2-proxy-operation-browser-host`, commit **`be27b45066947e920cda8da67991976b432ccb33`**, tree `64f32e9cb608bbf6a861c5c7b6fbbd9d8823caab`; implementation base `35dbb0eb12d75dc2c1becf7a9d8ac914758c05c7`.
- Assigned review worktree HEAD: `7bb885b638838588a0dff81b64b7c34960ac07f3`. It does not contain the new host. Read target with git show/diff and tested its exact git-archive snapshot under this review worker's own `source/`. Twelve relevant source/test files were subsequently verified byte-equal to target. No product file in either worktree was edited.
- Target changes exactly three files: `operationHost.ts`, its test, and `dataProvider.ts`. Existing client/generated/config/proxy/outbox and seven neighboring test files are unchanged against implementation base (empty git diff).
- Context only: existing requester `a103f3ca2e8e66f2837a85c0ddd007962eca66ac`, separately snapshotted without edits for three interface-refusal probes. This is not integrated requester/native qualification.

## Findings by source line

Line references below are against the pinned target, relative to `src/integrations/runtime/`.

| Area | Assessment |
| --- | --- |
| Launch policy | **Pass.** `operationHost.ts:65–113` retires the predecessor synchronously before the first await and uses existing page launch/config identity. Missing policy refuses before POST. Private policy copies persist across rebind. Acquire metadata is compared against that policy at `:126–133`; it never establishes its own expected instance. Hosted origin refuses before acquisition. |
| Authenticated negotiation | **Pass.** `:139–168,182–195` parses and validates actual received bytes synchronously after body consumption, before returning bytes to generated parsing/public handshake assignment or another await. Used protocol/status/digest/instance/actor/realm fields have exact string/equality checks; scopes must be an all-string array with exact membership and count, capabilities an all-string array containing the targeted capability. Forbidden actors, accepted digests, matching health/handshake digest and realm agreement remain enforced. Only private scalar copies establish authority. Independent forged-grant repair and alias-mutation probes confirm mutable generated results cannot establish forged identity. |
| Local lifetime | **Pass within owned boundaries.** `:88–103,169–205` clears identity, aborts data work and fences final fetch invocation, fetch/body completion and successful public result publication. Every callback closes over its original client/handle/binding. The `this.current !== binding` comparison at `:99` is an ownership check; old callbacks never obtain a replacement client or identity from host.current. `:118–131` cleans late acquisition responses/bodies without installing them. Existing tests cover acquire, negotiation, pre-write health, rebind/failure, disposal and late ACK; independent probes cover every retired callback plus task/object/HEAD/commit/identity propagation intervals. |
| One client and transport | **Pass.** `:191,219–225,238–244` constructs one private actual AstridRuntimeClient and uses the same guarded transport for negotiation, admission, task/managed-output/media/object reads, pre-write health and exact commit. Independent client-instance instrumentation observes one client. No client/session/handshake/objectContentUrl is exposed; no discovery/cache/playback fallback or provider client is used for raw transmission. |
| Fetch policy | **Pass for operation control/data/cleanup.** `:77–85,114–117,177–178` uses same-origin, no-store, omitted cookies, redirect:error and owned AbortSignals; cleanup gets a fresh signal. Handle remains a local header and generated authorization/handle injection is refused at `:173–175`. Existing launch-config reading remains the pre-existing policy seam, outside operation control/data requests. Server admission/stripping cannot be established by browser code. |
| Exact retry | **Pass for browser bytes.** `:226–250` copies saved request/scope before awaiting, checks actor/realm and exact project/timeline path/body, refuses dry-run, checks the existing expected instance and transmits original UTF-8 bytes and key without JSON reconstruction. Existing late-A/equal-identity-B test verifies different handles, equal body/key and no old ACK. This proves transmission, not Runtime receipt replay. |
| Errors and draft | **Pass within this unit.** `:181,189,202–204` retires on 401/403/410/5xx or transport/body failure and leaves unknown-outcome errors without permanent-refusal HTTP status. Normal semantic 409/422 at `:247–248` remain ApiErrors; independent probes preserve classification, live binding and unchanged saved draft/request. This host does not mutate an outbox; storage preservation still requires requester composition. |
| Shared decoder extraction | **Pass.** `dataProvider.ts:734–753,1547–1572` moves the original acceptance checks into one pure function; provider retains the original cache/registry update and late-ACK guard. Accepted/rebased status, receipt project/kind/publication identity, digest shape, canonical closure and identity-map checks are preserved. Old commit/provider tests pass unchanged. Independent accepted/rebased comparisons match ordinary provider and raw-host results, preserve original decoder response/receipt references, and verify `result.receipt === result.response.receipt`. No second client or acceptance model is introduced. |
| Lifecycle interface | **Pass, context only.** Host `:207–217` supplies a synchronous boolean check and private identity copies. Existing requester `a103...:130–146` requires strict `=== true` and catches failures. Three independent probes invoke that real requester with absent, Promise-returning and throwing lifecycle functions; all refuse before network/capture/build/transmit/reservation effects. A cached generated handshake alone remains unsupported. |

No newly weakened product-role, schema, expected-instance, canonical-closure or receipt guard was found. No old positive tests were changed, skipped, loosened or reclassified.

## Explicit limits and ordinary counterexamples

The host explicitly excludes delayed forwarding wrappers (`operationHost.ts:42–45`). An independent wrapper holds before its hidden primitive, retirement aborts the signal, then the wrapper ignores that signal and invokes its hidden primitive. This late hidden invocation is reproducible; the host still rejects its result. That counterexample prevents claiming a fence over arbitrary injected wrappers. Production qualification must use the actual immediate browser fetch and separately owned final Node dispatch.

A silent remote expiry/revocation cannot synchronously change this browser boolean: the independent remote-expiry probe remains current until a received 410, then irreversibly retires. This is local negotiated ownership, not proof of remote registry validity.

The Runtime ACK and implementation design explicitly preserve the two-process boundary: an HTTP request already handed off by the browser can reach an active server entry before DELETE/replacement reaches it, and Runtime may accept it. Browser retirement stops later browser invocation; server retirement stops later Node invocation. The browser cannot undo acceptance and must ignore late ACKs while retaining uncertain exact work. Likewise a result already past its final synchronous owned fence requires the consumer's own current-lifetime/claim check before use; a promise cannot revoke an already-published value. No stronger guarantee is inferred from abort, cached identity, or the tests.

## Executed verification

All runs used read-only `/tmp/app-m2-coherent-deps8/node_modules` through a symlink created only in this worker's snapshot, a private `runner.cjs`, runner config loading, disabled caching and one worker. Independent config also sets cacheDir to this worker's private folder. No install or shared dependency/cache mutation.

Exact commands, from `W/source`, where:

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-proxy-browser-host-independent-review
cd "$W/source"
node --require ../runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/integrations/runtime/operationHost.test.ts src/integrations/runtime/timelineCommit.test.ts src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts src/integrations/runtime/client.runtimeOrigin.test.ts src/integrations/runtime/dataProvider.test.ts src/integrations/runtime/dataProvider.parity.test.ts src/integrations/runtime/workspaceRuntimeConfig.test.ts > ../targeted.log 2>&1
node --require ../runner.cjs node_modules/vitest/vitest.mjs run --config ../review.config.ts --configLoader=runner --no-cache --maxWorkers=1 > ../independent.log 2>&1
```

- Targeted existing tests: **8 files, 244 tests passed, exit 0**, 15.16s. Log: worker `targeted.log`.
- Final independent probes: **1 file, 25 tests passed, exit 0**, 2.87s, including 80 task/object/HEAD/commit/identity microtask intervals. Source: worker `independent.test.ts`; log `independent.log`. Real clients/decoder and requester interface guard, in-process fetch bytes; no substitute acceptance engine. An initial context-file extraction mistakenly ran git from the archive (which has no .git); corrected using the assigned repository, without source/test expectation changes. Earlier 22/25-test passes were superseded by final strengthened probes.
- `git diff --check`: **exit 0**. `git status --porcelain=v1 --untracked-files=all`: **empty** in the assigned review worktree. Read-only git diff confirmed unchanged original neighboring suites and client/generated/proxy/config/outbox paths. Byte comparison of twelve snapshot files against git show: **pass**.

No full/central suite, build, browser, socket/listener, project tsc, install, native capture, real Runtime acceptance/restart/receipt replay or storage/native integration was run. Fixtures are not activation evidence.

## Decision and next steps

No implementation blocker or design deviation within this inactive browser assignment. **APPROVE this exact browser-host source only; keep activation HOLD.** Compose the separately owned proxy/config implementation, qualify its real admission/stripping/expiry/dispatch/body behavior centrally, then qualify same-store requester/claim/native capture with real Runtime acceptance, lost ACK, exact receipt retry/restart and browser behavior on the frozen supported tuple. Hosted/paired automatic requesting remains unsupported. No product edit or KEEP is requested.
