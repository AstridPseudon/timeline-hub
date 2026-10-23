# A2 mounted diagnostic seam — app-A2-mounted-diagnostic-seam-sol-1945

Base: App `2107e1870e51c650d59315f4cc1ab6af338f198c`, tree `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`. Diagnostic instrumentation only; no semantic fix or causal finding.

## Change and interface

Only three allowed production files changed: `lib/timeline-diagnostics.ts`, `hooks/useTimelineSave.ts`, and `hooks/useTimelinePersistence.ts`. Added `lib/timeline-diagnostics.save.test.ts` and appended tests to `hooks/useTimelineSave.test.tsx`; the original test bytes are untouched. `useTimelinePersistence.test.tsx` is unchanged and was run as a neighbor.

The exact browser interface is `window.__timelineSaveDiagnosticsEnabled === true` and `CustomEvent('timeline:save-diagnostic', { detail })`. Default disabled. The existing `isTimelineDiagnosticsEnabled()` DEV + `debugTimeline=1` policy and its logging behavior are unchanged. The new emitter does not log, serialize, retain event history, submit requests, claim owners, or consume observer return values. Proof remains sole collector/test-artifact author.

Every detail has version `1`, monotonic `sequence` and nondecreasing finite `time` from `performance.now()` (page/module lifetime), and a fixed allowlisted `phase`. All remaining keys are exactly those shown in the illustrative record below. Numeric projections contain only `from/to/at/hold/speed`, each paired with a `*State` of `present`, `absent`, `null`, or `UNKNOWN`. Explicit undefined/nonfinite/non-numeric values have UNKNOWN numeric state; unavailable containers and accessor properties are UNKNOWN. IDs are at most 160 characters and restricted to `[a-zA-Z0-9_.:-]`; URL-shaped or unavailable IDs become UNKNOWN. An actual null ID stays null. No arbitrary keys or data structures are copied.

Phases: `schedule`, `capture-called`, `capture-resolved`, `capture-rejected`, `owner-init`, `owner-closed`, `owner-retired`, `lifecycle-cancel`, `basis-read`, `basis-ready`, `basis-unavailable`, `basis-error`, `identity-read`, `session-created`, `session-recovered`, `session-changed`, `adoption-start`, `adoption-complete`, `adopted-read`, `handoff-ready`, `owner-error`.

`ownerAlias` is a non-auth integer assigned with a WeakMap to the actual hook owner. A read-only optional internal `diagnosticOwner` hook option joins schedule records to the existing save owner's capture/adoption records. It changes no capture callback argument or session ownership. Standalone persistence callers fall back to their existing session identity object.

Actual observations:

- `schedule`: actual `getDataRef().current`, callback `nextData`, selected/gesture clip ID, numeric gesture patch, gesture input config, and the actual supplied save-owner generation/closed/session presence (standalone persistence callers expose only their own generation).
- `capture-called`: actual capture source/gesture operands before cloning or awaiting; `capture-resolved` after the real handoff capture resolves; `capture-rejected` catches and rethrows the identical original error. No extra await is added.
- Basis reads emit at assembly read start and ready/unavailable/error boundaries. Original head pairs come from the verified basis's actual source, without refreshing or inventing a basis.
- Owner lifecycle/identity/session events read only already available owner fields, identity presence, and the provided changed-state status/owner-presence/recoverable-owner count. Identity values are never inspected or emitted.
- `adoption-start` and `adoption-complete` surround the actual prepared-display adoption. `adopted-read` marks the existing handoff adopted-source/receipt callback and returns exactly its prior values. `scopeMatched`, when observed at adoption-start, compares only project/timeline identity; it does not claim authenticated actor/realm matching.

The projection uses named own data properties; getters are not evaluated. Selected-clip scans inspect at most the first 256 clips per named input, never arbitrary nested data. Counts above 10,000 become UNKNOWN. Fresh projection objects and their nested head/numeric records are frozen; no App reference reaches a listener. Flag access, lazy extraction, projection and dispatch are guarded against exceptions. Disabled calls do not run extraction callbacks or project/copy/serialize state.

## Explicit limits and decisions

`intentsPendingCount` and `errorClass` remain UNKNOWN: the mounted hook's existing public session state does not expose a pending count or a safe classified error. `errorCode: operation-rejected` is a fixed diagnostic marker, never a provider failure classification; `errorStage` is only `capture`, `basis-read`, `owner-init`, or UNKNOWN. No error message, stack, request/reply, principal/actor/realm, auth scope, credential hash, token, header, cookie, bundle, registry, asset URL, or arbitrary metadata is emitted.

Capture's mounted/original head and basis status stay UNKNOWN where those values are not available inside its unchanged memo closure. Actual mounted dataRef is emitted at schedule; original basis head/status are emitted at the basis and handoff boundaries. Proof must correlate these observations by timeline/clip, ownerAlias, sequence and generation. No extra cached state, provider read, session API, or memo dependency was introduced to manufacture missing values. Original-basis selected numerics remain UNKNOWN when no clip ID is available at that read boundary. A clip beyond the 256-item scan limit is UNKNOWN. Flags enabled after initial reads cannot recover past observations; Proof should install its bounded listener and flag before App loads.

The existing effect cancellation/dependency behavior, including the conditional source1934 scenario, is retained. No retry/refusal/preview/serialization/body/key/reads/undo/recovery/transport change was made. LocalSaveSession, commitOutbox and timelineLocalSaveHandoff implementation bytes are unchanged. Event listeners have only detached diagnostic data; the emitter cannot suppress a browser's separate global reporting of exceptions thrown by native event listeners, but those exceptions do not reject the save operation.

## Illustrative allowed record

This is a synthetic complete capture-called detail showing available callback input and explicit unknown mounted/basis fields. It is not an observation from historical P1.

```json
{
  "version": 1,
  "sequence": 4,
  "time": 12.5,
  "phase": "capture-called",
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
  "errorStage": "UNKNOWN",
  "errorCode": "UNKNOWN",
  "errorClass": "UNKNOWN"
}
```

## Verification

Final targeted command (Node v22.22.0, shared dependency realpath checked first):

```sh
node --import 'data:text/javascript,globalThis.__dirname=process.cwd()+"/config/testing"' node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/lib/timeline-diagnostics.save.test.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/useTimelinePersistence.test.tsx
```

PASS: 3 files / 128 tests, 12.60s. Includes 122 retained existing tests, four projection tests, and two new real mounted inspector-callback cases. Those cases run `useClipEditing.handleSelectedClipChange({ from: 3 })` through the real `useTimelineSave` → `useTimelinePersistence` → handoff → LocalSaveSession/outbox chain. They verify capture start→resolve/reject, original basis readiness/unavailability, actual canonical adoption/adopted-read order, shared schedule/capture owner alias, unchanged raw `app.astrid.for: 8`, actual accepted head adoption or original refusal, and zero legacy writer calls. Accepted transport is mocked; no live/browser/P1 claim.

One initial new-test fixture failed because it supplied raw rather than mounted gesture config; the existing guard correctly rejected it. The new test was corrected to use the actual inspector callback. No old test or guard was changed. Later reruns were required by the alias-correlation and adopted-read additions; final results above are the final source.

Typecheck commands (each serialized under the requested lock, 4096MB):

```sh
flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit --pretty false
flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit --pretty false
flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node node_modules/typescript/bin/tsc -p tsconfig.json --noEmit --pretty false
```

App, Node and root PASS, exit 0; final App check completed after the final production change. Root is the requested root configuration check, not a claim of additional project coverage beyond App/Node.

```sh
node node_modules/eslint/bin/eslint.js src/tools/video-editor/lib/timeline-diagnostics.ts src/tools/video-editor/hooks/useTimelineSave.ts src/tools/video-editor/hooks/useTimelinePersistence.ts src/tools/video-editor/lib/timeline-diagnostics.save.test.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx --max-warnings 0 --report-unused-disable-directives
git diff --check
```

Both PASS, exit 0, scoped ESLint zero warnings. Read-only source checks verified the file allowlist; unchanged callback/effect dependency arrays; unchanged localSaveSession/commitOutbox/handoff; original useTimelineSave test byte-prefix SHA-256 `bd6adf9ad6b2cd9fcde594a41120e10d4c5c249274186b89a004b41d5a37af82`; shared node_modules realpath `/home/user/work/app/node_modules` and 427 top-level entry identities unchanged. This is a target/top-entry identity check, not a recursive content attestation. No install/shared-cache mutation was performed; Vitest used runner/no-cache.

Protected original P1 title-boundary hashes remain first `4b04ad7ef74b8106244d87c23d12c7a18da251dd8f5a746f42d3221a72ea8b7f`, second `2f7501184477c8aec38d3cd289dd13c0d011fa8f69ecd43378f24f6c3100a2f7`. Gate-5 blob remains `37caf28577d42fbe98afd2320dffa3c72e6e74b1`. Entire P1 and Gate-5 files equal base bytes; no collector/harness/e2e/config/env/kit/generated/schema/lock/pin/other-repo/Git modification, deletion, full/browser/live/HTTP/service/seed/preflight/body/benchmark run, or central test request.

Independent read-only Luna review found the initial alias-join gap, verified the correction, actual owner-generation/session-presence projection, and adopted-read addition, and returned no remaining blocker. Reviewer ran only source/diff checks, no tests.

## Historical evidence and next step

Directly read the exact safe packet: 19,853 bytes, SHA-256 `97b088b687ec4779eb85dfc94c9ebb43d03bae30ae5ba96d608544d540e0c1e8`. Retained collector policy is max 16,384 bytes/depth 8/40 keys/40 array items/500-character strings/4 priority items. Qualified lines 10 (3,818 bytes) and 11 (2,800 bytes) and the unparseable capped line-12/lost suffix retain their independent1920 limits. Full requests/success data+receipts/raw credentials are not copied. The historical packet cannot supply mounted observations retroactively.

D24 raw-for-8 preservation is retained. D25 historical triage stays INSUFFICIENT EVIDENCE: actual18607 first PASS27.4s / second FAIL1POST-vs2 plus test/afterEach timeouts; Agent move, Runtime409 refusal and App rollback were unreached. No cause or GO is claimed and no historical22122 reclassification is made.

No source blocker remains. After normal harness commit and App-owned queue, Proof should adapt its existing bounded listener/artifact collector to this exact opt-in interface; any original-body execution remains separately owned/authorized. This worker did not author the collector or request another run.

Retained small command logs: `targeted-final.log`, `lint-final.log`, `tsc-app-final.log`, `tsc-node.log`, and `tsc-root.log` in this worker folder. Empty lint/type logs correspond to the recorded exit-0 checks.
