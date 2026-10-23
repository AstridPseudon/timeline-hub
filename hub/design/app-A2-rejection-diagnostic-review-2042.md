# A2 finite local rejection diagnostic — independent review

## Verdict: PASS

Reviewed tl/app-A2-local-rejection-diagnostic-sol-2031 commit
6eccf152b1e04ef5666311866a35239ac9f024f, tree
86b5de4fc39d1144b30ca9f67dbd46e005fedfc2, against parent
ba8583b8292790e9d5651504f755762e35c74dab (parent tree
6b702ef409f216af31f34f982a3393efedb19370). The review is limited to the
finite local rejection tagging and preservation of existing save/error
behavior. It does not claim the actual17985 rejecting guard, a product repair,
P1 GO, or any new body/e2e qualification.

## Scope and source findings

The diff is exactly these six authorized files:

~~~text
M src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts
M src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts
M src/tools/video-editor/hooks/useTimelineSave.test.tsx
M src/tools/video-editor/hooks/useTimelineSave.ts
M src/tools/video-editor/lib/timeline-diagnostics.save.test.ts
M src/tools/video-editor/lib/timeline-diagnostics.ts
~~~

The private WeakMap is populated only by explicit markTimelineSaveRejection
calls while window.__timelineSaveDiagnosticsEnabled === true. It stores only
the fixed code and fixed class, returns the exact input exception, and never
reads or mutates exception properties. Only capture-rejected, basis-error,
and owner-error consult the tag. Foreign, forged, cloned, accessor,
hostile-proxy, revoked-proxy, string, and untagged errors remain generic
operation-rejected/UNKNOWN and do not throw or leak. The source does not
dispatch the raw error, message, stack, cause, source, dataRef, path, auth, or
other application object.

All 38 source-authored rejection codes, in source order, are:

~~~json
["original-head-unavailable","capture-source-head-unavailable","capture-input-head-unavailable","source-parent-unavailable","source-parent-mismatch","source-clip-identity","source-track-identity","source-bundle-mismatch","original-read-unavailable","authored-collection-unavailable","authored-binding-ambiguous","authored-identity-unavailable","display-container-unbound","trim-binding-mismatch","explicit-clear-unavailable","display-value-unbound","child-ownership-unavailable","local-document-changed","parent-mirror-mismatch","gesture-basis-mismatch","gesture-clips-unavailable","gesture-clip-ambiguous","gesture-registry-unavailable","registry-mirror-mismatch","split-time-unavailable","move-track-mismatch","move-tracks-unavailable","move-track-ambiguous","move-routing-unavailable","trim-operands-unavailable","capture-owner-unavailable","capture-owner-replaced","owner-original-read-invalidated","owner-identity-invalidated","owner-retirement-invalidated","owner-claim-invalidated","owner-recovery-ambiguous","owner-history-invalidated"]
~~~

The two source-supplied classes are exactly
TimelineVersionConflictError and Error. The compact JSON consisting of the
code list plus class list, followed by one LF, hashes to
5f7d9e8f3da6f39c4b4b96a14908b9b9b5f36d33f5940275b6a511fa0ff6b897.

Actual source sample (not an actual17985 observation):

~~~ts
if (!isCurrent()) throw markTimelineSaveRejection(
  new Error('Local save session replaced during history read'),
  'owner-history-invalidated', 'Error');

errorCode: rejection?.code ?? (rejected ? 'operation-rejected' : UNKNOWN),
errorClass: rejection?.errorClass ?? UNKNOWN,
~~~

The combined head predicate is tagged at its existing guard boundary; the
review does not claim which individual OR operand caused it. Existing event
version 1, 21 phases, keys, numeric-state projection, owner aliases,
UNKNOWN behavior, control flow, awaits, Promise rejection identity, wrapping,
owner/lifecycle guards, disposal, outbox, transport, request/reply handling,
and persistence remain unchanged. The existing generic refusals not assigned
one of the 38 authentic source reasons remain generic.

Current-file SHA-256 values:

~~~text
0793024b13484ea19313199d9c888f77d55bf5428841449dc158fb0f27e2c21f  src/tools/video-editor/lib/timeline-diagnostics.ts
d9b16544f7f32b738e2c88144471ca0765dfe13717decdf9a8c5790807bf8fb4  src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts
60a04791247c189cd57e040dfb13ced99bbcb83b41688021643c8e0862c485b3  src/tools/video-editor/hooks/useTimelineSave.ts
5012c9f022897a8ea113773390f98872934200f08ef799f3981856fcb87f6101  src/tools/video-editor/lib/timeline-diagnostics.save.test.ts
b022f44fc9a4c8d6eb410c29612ffd032f6bac49e7322e668d70cd43495b6a93  src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts
152c1f38dfbf0c2503317373d62ccca0f79a55adb5a106f31ee5eafcbddd8797  src/tools/video-editor/hooks/useTimelineSave.test.tsx
~~~

The author’s protected original artifacts remain reported as exact: P1 first
4b04ad7ef74b8106244d87c23d12c7a18da251dd8f5a746f42d3221a72ea8b7f, P1
second 2f7501184477c8aec38d3cd289dd13c0d011fa8f69ecd43378f24f6c3100a2f7,
and Gate 5 37caf28577d42fbe98afd2320dffa3c72e6e74b1. No semantic fixture,
guard, assertion, executor, endpoint, schema, authority, auth, pin, generated
file, or product consumer was changed.

## Tests and checks

Shared dependency realpath was checked as /home/user/work/app/node_modules;
no dependency or cache files were changed.

Exact affected-file cohort:

~~~text
node --import 'data:text/javascript,globalThis.__dirname=process.cwd()+"/config/testing"' node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/lib/timeline-diagnostics.save.test.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/useTimelinePersistence.test.tsx
~~~

PASS — 4 files, 164 tests, 12.94 seconds.

Independent typecheck commands, each with the app lock and 4096 MB heap,
passed with exit 0 and no diagnostics:

~~~text
flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit --pretty false
flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit --pretty false
flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node node_modules/typescript/bin/tsc -p tsconfig.json --noEmit --pretty false
~~~

Scoped lint passed with zero warnings, and the exact normal diff check passed:

~~~text
node node_modules/eslint/bin/eslint.js src/tools/video-editor/lib/timeline-diagnostics.ts src/tools/video-editor/lib/timeline-diagnostics.save.test.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/hooks/useTimelineSave.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx --max-warnings 0 --report-unused-disable-directives
git diff --check ba8583b8292790e9d5651504f755762e35c74dab..6eccf152b1e04ef5666311866a35239ac9f024f
~~~

The author packet disclosed an initial unchanged mounted Undo ABA timing
failure and its later isolated/final cohort pass; my independent final cohort
run passed without source changes. I did not rerun or replace the stopped
optional Node AST/spawnSync-git check, and make no AST-equivalence claim.
No full suite, browser, body, HTTP, live socket, seed, preflight, benchmark,
service, or bin run was performed.

## Proof handoff and residual limits

The current Proof adapter forces errorClass to UNKNOWN. Its typed follow-up
must preserve the existing v1 event contract while accepting this exact source
extension:

~~~ts
type TimelineSaveRejectionCode =
  | 'original-head-unavailable'
  | 'capture-source-head-unavailable'
  | 'capture-input-head-unavailable'
  | 'source-parent-unavailable'
  | 'source-parent-mismatch'
  | 'source-clip-identity'
  | 'source-track-identity'
  | 'source-bundle-mismatch'
  | 'original-read-unavailable'
  | 'authored-collection-unavailable'
  | 'authored-binding-ambiguous'
  | 'authored-identity-unavailable'
  | 'display-container-unbound'
  | 'trim-binding-mismatch'
  | 'explicit-clear-unavailable'
  | 'display-value-unbound'
  | 'child-ownership-unavailable'
  | 'local-document-changed'
  | 'parent-mirror-mismatch'
  | 'gesture-basis-mismatch'
  | 'gesture-clips-unavailable'
  | 'gesture-clip-ambiguous'
  | 'gesture-registry-unavailable'
  | 'registry-mirror-mismatch'
  | 'split-time-unavailable'
  | 'move-track-mismatch'
  | 'move-tracks-unavailable'
  | 'move-track-ambiguous'
  | 'move-routing-unavailable'
  | 'trim-operands-unavailable'
  | 'capture-owner-unavailable'
  | 'capture-owner-replaced'
  | 'owner-original-read-invalidated'
  | 'owner-identity-invalidated'
  | 'owner-retirement-invalidated'
  | 'owner-claim-invalidated'
  | 'owner-recovery-ambiguous'
  | 'owner-history-invalidated';
type TimelineSaveRejectionClass = 'TimelineVersionConflictError' | 'Error';
type TimelineSaveDiagnosticErrorCode = TimelineSaveRejectionCode | 'operation-rejected' | 'UNKNOWN';
type TimelineSaveDiagnosticErrorClass = TimelineSaveRejectionClass | 'UNKNOWN';
~~~

The adapter must retain operation-rejected/UNKNOWN for untagged or foreign
errors and must not infer an OR operand or the actual17985 cause. This source
donor is eligible for a future stack after independent review of the author’s
three test blobs (including reviewed 669); no composition qualification is
implied beyond a later conflict-free qualification. Recommended next step is
the normal independent merge review, followed by the smallest Proof adapter
allowlist update; no product repair or new body is authorized by this report.

