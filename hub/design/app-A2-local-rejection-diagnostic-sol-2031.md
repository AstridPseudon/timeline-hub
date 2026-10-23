# A2 finite local rejection diagnostic — app-A2-local-rejection-diagnostic-sol-2031

Base App `ba8583b8292790e9d5651504f755762e35c74dab` (`tl/integration`). Instrumentation only. No actual17985 cause claim, product/oracle repair or new body/run. PLAN §3 A2, contract 1–5 and D24–D26 constraints retained. Consumed actual-cause2017, original1945 interface/report and Proof2012 return.

Only the three authorized production files and their three existing test files changed. A private WeakMap associates a fixed code/class with the exact exception allocated at an existing guard. Tagging returns that exception; it never reads or mutates its message, stack, cause, properties or prototype. Existing capture wrapping, Promise.reject, rethrow, awaits, lifecycle/owner/disposal guards, dependencies, outbox, transport, request/reply handling and persistence remain as before. In particular the existing handoff catch still wraps its formerly wrapped foreign errors: this change does not replace or reclassify those wrappers.

The flag remains `window.__timelineSaveDiagnosticsEnabled === true`, event `timeline:save-diagnostic`. Version 1, all keys, the 21 phases, numericState/ownerAlias/UNKNOWN meanings, bounded projection and prior DEV/URL log policy are unchanged. Tags are recorded only with the explicit flag enabled. Tagging and projection/dispatch failures are swallowed. Weak keys do not retain errors; the stored values contain two finite strings only. No error-derived string or object is dispatched. Disabled extraction stays disabled.

## Prospective typed extension for Proof

The exact new `errorCode` values (38) are below, in source order. `TimelineSaveRejectionCode` is the literal union derived from this source-authored list. New `errorClass` values are exactly `TimelineVersionConflictError` and `Error`. Existing `operation-rejected` and `UNKNOWN` remain valid. Class is supplied by the authentic constructor call site, never inferred from an external error's name/type/message.

```json
{"errorCode":["original-head-unavailable","capture-source-head-unavailable","capture-input-head-unavailable","source-parent-unavailable","source-parent-mismatch","source-clip-identity","source-track-identity","source-bundle-mismatch","original-read-unavailable","authored-collection-unavailable","authored-binding-ambiguous","authored-identity-unavailable","display-container-unbound","trim-binding-mismatch","explicit-clear-unavailable","display-value-unbound","child-ownership-unavailable","local-document-changed","parent-mirror-mismatch","gesture-basis-mismatch","gesture-clips-unavailable","gesture-clip-ambiguous","gesture-registry-unavailable","registry-mirror-mismatch","split-time-unavailable","move-track-mismatch","move-tracks-unavailable","move-track-ambiguous","move-routing-unavailable","trim-operands-unavailable","capture-owner-unavailable","capture-owner-replaced","owner-original-read-invalidated","owner-identity-invalidated","owner-retirement-invalidated","owner-claim-invalidated","owner-recovery-ambiguous","owner-history-invalidated"],"errorClass":["TimelineVersionConflictError","Error"]}
```

Finite-list SHA-256 (the above compact JSON encoded UTF-8 followed by one LF): `5f7d9e8f3da6f39c4b4b96a14908b9b9b5f36d33f5940275b6a511fa0ff6b897`.

These values are prospective enum extensions. Proof's published2012 adapter currently forces errorClass to UNKNOWN and must explicitly accept this list to retain the new classifications; this worker did not change its three owned e2e/collector/safety files. No integrated adapter-to-artifact or live qualification is claimed. Publish this interface to that owner before a future eventful body. The previous producer/adapter qualification remains separate from this extension.

## Actual emitting boundaries

Only existing `capture-rejected`, `basis-error` and `owner-error` events consult the private tag. Other phases retain UNKNOWN error fields. `errorStage` retains capture/basis-read/owner-init from the existing phase and is not a cause inference. Tags propagate only by exact exception identity through existing catch/rethrow paths; no matching by values, heads, numerics, messages or DOM occurs.

In `timelineLocalSaveHandoff.ts`, all tagged refusals allocate the existing TimelineVersionConflictError:

| Code | Actual existing guard |
| --- | --- |
| original-head-unavailable | checkHead's existing combined verified head predicate during original read or handoff creation |
| capture-source-head-unavailable | same checkHead predicate on the handoff's current stored source in capture |
| capture-input-head-unavailable | same checkHead predicate on the actual cloned next input in capture |
| source-parent-unavailable | checkSource: parent config or registry is not an object |
| source-parent-mismatch | checkSource: source config/registry differs from allowed raw/load projection |
| source-clip-identity / source-track-identity | checkSource's existing named collection identity predicate, selected by its fixed clips/tracks loop |
| source-bundle-mismatch | checkSource: supplied original bundle differs |
| original-read-unavailable | readTimelineOriginalSaveBasis: loader missing or supplied timeline differs |
| authored-collection-unavailable | changes: raw clips/tracks collection is not an array |
| authored-binding-ambiguous | changes: existing duplicate/missing row binding predicate |
| authored-identity-unavailable | changes: next row has no valid identity |
| display-container-unbound | changes: changed display object lacks raw object |
| trim-binding-mismatch | changes: omitted astrid for/until has no exact raw previous binding |
| explicit-clear-unavailable | changes: explicit undefined outside supported transition clearing |
| display-value-unbound | changes: changed array/object lacks exact previous raw binding |
| child-ownership-unavailable | capture: child/internal/occurrence ownership predicate |
| local-document-changed | capture: session document differs from retained document |
| parent-mirror-mismatch | capture: existing clips/tracks mirror differs from config |
| gesture-basis-mismatch | capture: unsupported gesture kind or config/registry differs from authoring input |
| gesture-clips-unavailable | capture: authored gesture clips is not an array |
| gesture-clip-ambiguous | capture: selected gesture clip has other than one binding |
| gesture-registry-unavailable | assetRead: parent registry is not an object |
| registry-mirror-mismatch | assetRead: existing registry mirror predicate |
| split-time-unavailable | capture split: time is not finite |
| move-track-mismatch | capture move: selected track differs from original |
| move-tracks-unavailable | capture move: tracks is not an array |
| move-track-ambiguous | capture move: track has other than one binding |
| move-routing-unavailable | capture move: sibling routing row is not an object |
| trim-operands-unavailable | capture trim: empty patch or unsupported key |

In `useTimelineSave.ts`:

| Code | Actual existing guard | Fixed class |
| --- | --- | --- |
| capture-owner-unavailable | capture: owner closed or ready promise absent | TimelineVersionConflictError |
| capture-owner-replaced | capture: owner closed after ready resolves | TimelineVersionConflictError |
| owner-original-read-invalidated | ready: cancelled/closed/edit sequence changed after originalRead | TimelineVersionConflictError |
| owner-identity-invalidated | ready: cancelled/closed after identity read | Error |
| owner-retirement-invalidated | ready: not current after previousDisposal | Error |
| owner-claim-invalidated | ready: not current after session creation, after its existing disposal | Error |
| owner-recovery-ambiguous | ready: multiple recoverable owners | TimelineVersionConflictError |
| owner-history-invalidated | ready: not current after history path | Error |

A combined existing predicate identifies its authentic guard statement, not which OR operand was true. A dynamic clips/tracks mirror or authored path is intentionally not exported. Basis-origin exceptions can appear in basis-error, owner-error and capture-rejected when the same rejected originalRead propagates; this is identity correlation, not three separate failures. Mapping refusals tag only when their existing call executes. No new events, promises, catches, await, retries, disposal or state clearing were added.

## Sample and limits

Synthetic complete version-1 detail for the capture input-head guard; not an actual17985 observation:

```json
{
  "version": 1,
  "sequence": 4,
  "time": 12.5,
  "phase": "capture-rejected",
  "projectId": "project-commit",
  "timelineId": "timeline-1",
  "clipId": "diagnostic-clip",
  "ownerAlias": 1,
  "generation": 0,
  "sessionPresent": true,
  "closed": false,
  "current": "UNKNOWN",
  "identityPresent": "UNKNOWN",
  "scopeMatched": "UNKNOWN",
  "mountedHead": {
    "revisionId": "UNKNOWN",
    "publicationId": "UNKNOWN"
  },
  "originalHead": {
    "revisionId": "UNKNOWN",
    "publicationId": "UNKNOWN"
  },
  "basisStatus": "UNKNOWN",
  "gestureKind": "trim",
  "patch": {
    "from": 3,
    "fromState": "present",
    "to": "UNKNOWN",
    "toState": "absent",
    "at": "UNKNOWN",
    "atState": "absent",
    "hold": "UNKNOWN",
    "holdState": "absent",
    "speed": "UNKNOWN",
    "speedState": "absent"
  },
  "mountedClip": {
    "from": "UNKNOWN",
    "fromState": "UNKNOWN",
    "to": "UNKNOWN",
    "toState": "UNKNOWN",
    "at": "UNKNOWN",
    "atState": "UNKNOWN",
    "hold": "UNKNOWN",
    "holdState": "UNKNOWN",
    "speed": "UNKNOWN",
    "speedState": "UNKNOWN"
  },
  "sourceClip": {
    "from": 3,
    "fromState": "present",
    "to": 8,
    "toState": "present",
    "at": 0,
    "atState": "present",
    "hold": 8,
    "holdState": "present",
    "speed": 1,
    "speedState": "present"
  },
  "gestureClip": {
    "from": 0,
    "fromState": "present",
    "to": 8,
    "toState": "present",
    "at": 0,
    "atState": "present",
    "hold": 8,
    "holdState": "present",
    "speed": 1,
    "speedState": "present"
  },
  "originalClip": {
    "from": "UNKNOWN",
    "fromState": "UNKNOWN",
    "to": "UNKNOWN",
    "toState": "UNKNOWN",
    "at": "UNKNOWN",
    "atState": "UNKNOWN",
    "hold": "UNKNOWN",
    "holdState": "UNKNOWN",
    "speed": "UNKNOWN",
    "speedState": "UNKNOWN"
  },
  "status": "UNKNOWN",
  "ownerPresent": "UNKNOWN",
  "recoverableOwnerCount": "UNKNOWN",
  "intentsPendingCount": "UNKNOWN",
  "errorStage": "capture",
  "errorCode": "capture-input-head-unavailable",
  "errorClass": "TimelineVersionConflictError"
}
```

Sample SHA-256 (compact JSON with the displayed key order, UTF-8 plus one LF): `65f6da1ba4d07bcd68cfb1ed5d521ddef7c5628909d542a9dc21ef002e6cc553`.

Foreign/provider errors, unreadable/revoked proxies, untagged clone/normalization/encoder/JSON errors, and existing foreign-error wrappers retain operation-rejected / UNKNOWN. The out-of-scope encoder's nonfinite-JSON rejection is explicitly tested as generic; no string matching was added to guess its cause. An asynchronous append rejection is not intercepted or rewrapped. No guard identity can be recovered retrospectively or when its exception was created while opt-out was active. No individual OR operand or unobserved owner transition is asserted. The actual17985 rejecting guard therefore remains UNKNOWN. This is the exact residual limitation; no guessed semantic fix is justified.

## Verification

Node v22.22.0; Vitest reported v4.1.5. Shared dependency realpath checked first: /home/user/work/app/node_modules. No install, shared package/cache write or dependency version change. Test caches disabled; runner uses owned worktree dirname preload. All scratch and initial logs are in TMPDIR /tmp/w-1d1617a12f. No full suite, browser, HTTP, live socket, test service, seed, preflight or benchmark was run.

Exact final cohort command:

```sh
node --import 'data:text/javascript,globalThis.__dirname=process.cwd()+"/config/testing"' node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/lib/timeline-diagnostics.save.test.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/useTimelinePersistence.test.tsx
```

PASS: 4 files / 164 tests, 13.05s. New coverage: eight real handoff guard/generic failures with enabled/disabled behavior parity, identical Promise.reject error identity/class/message, unchanged error descriptors (including stack), no transport or intents/document mutation; three real mounted head/gesture/closed-owner capture refusals across disabled/enabled/throwing-dispatch states, preserving original exception identity and unchanged saved head/state; pre-read mounted owner rejection code; foreign/forged/getter/hostile/revoked error security and immutable-error identity tests. Original save/handoff/persistence behavior expectations retained; only an existing diagnostic-only generic code expectation was updated to its now-authentic owner reason.

The first identical cohort run had 163 passes and one failure in unchanged mounted Undo ABA (canUndo true at line589); new tests all passed. Isolated recheck passed (1 selected, 40 filtered) using:

```sh
node --import 'data:text/javascript,globalThis.__dirname=process.cwd()+"/config/testing"' node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/hooks/useTimelineSave.test.tsx --testNamePattern='mounted Undo uses the public client, authoritative history and reload \(aba_write\)'
```

The same complete affected cohort then passed without changes. Initial run emitted React act warnings in retained Undo tests; no tests were weakened, disabled, skipped or rewritten to lose behavior. The cause of that transient failure was not independently established.

```sh
flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit --pretty false
flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit --pretty false
flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node node_modules/typescript/bin/tsc -p tsconfig.json --noEmit --pretty false
```

TYPECHECK_RESULTS_PENDING

```sh
node node_modules/eslint/bin/eslint.js src/tools/video-editor/lib/timeline-diagnostics.ts src/tools/video-editor/lib/timeline-diagnostics.save.test.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/hooks/useTimelineSave.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx --max-warnings 0 --report-unused-disable-directives
git diff --check
```

Scoped lint PASS, zero warnings; diff PASS. Python stdlib read-only scope/hash checks verified exactly the six authorized changed files, full P1/Gate5 byte equality to HEAD, first P1 SHA-256 `4b04ad7ef74b8106244d87c23d12c7a18da251dd8f5a746f42d3221a72ea8b7f`, second `2f7501184477c8aec38d3cd289dd13c0d011fa8f69ecd43378f24f6c3100a2f7`, whole Gate5 Git blob `37caf28577d42fbe98afd2320dffa3c72e6e74b1`. No e2e/adapter, golden, executor, endpoint, schema, authority, auth, pin, generated file or Git mutation; no deletion.

## Handoff

No implementation blocker. Independent Luna review is required after this worker's terminal; not claimed here and not spawned concurrently. Orchestrator should dispatch that review, then coordinate Proof's exact finite-enum extension against this published packet before any future body. Existing firstreturn2012 qualification remains independent. Neither green unit tests nor this source packet establish whole P1 GO or actual17985 cause.
