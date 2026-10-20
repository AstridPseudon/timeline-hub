# AP2-M2 bootstrap transport assertion repair

## Deliverable

- Approved handoff patch applied privately: `handoff-ap2-m2-bootstrap-real-transport-consumer.patch`
- Approved handoff SHA256: `9c6e05abd9cb330edce41e7d717aad43189ce81bc87c3fb4da02ba291867c59`
- Approved handoff base commit: `05b6b488d1834650c459c5c565f2530d9bea20e9`
- Repair patch: `ap2-m2-bootstrap-transport-assertion-repair.patch`
- Repair patch SHA256: `f5ae641574b45b7e9733b2ef6ffd5955a27888c0b1c1d3467b4e0121cc8e0fd6`
- Repair patch base: approved handoff commit `07527161e8386d947dd88a33875fbc9b8fb31987` (the tree produced by the approved handoff patch)
- Repair scope: `src/integrations/runtime/createDefaultTimeline.test.ts` only; 113 additions, 13 deletions

The production files in the private worktree are byte-identical to the approved handoff patch. The repair changes only the real-transport test.

## Repair

The native fixture now rejects malformed traffic at the transport boundary. It requires exact encoded project/timeline routes and methods; exact `Accept`, JSON content-type, and idempotency headers; body-free GETs; the complete handshake request; exact create fields; and the complete initialization `CommitRequest` (`api_version`, project/timeline identity, bootstrap base revision/publication, all three captured commands, and `source: { via: 'app' }`). It rejects legacy POST publication/document routes explicitly and still rejects every other unexpected route.

The lost-response assertion now checks one create, two equal commit calls, the exact commit route, full request identity/body guards, valid and stable commit idempotency identity, the exact retry create body, and absence of legacy traffic. Existing native fixture and outbox controls remain in use; no test matrix or production callback was added.

## Verification

```text
NODE_OPTIONS='--require=.../workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs' \
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/integrations/runtime/bootstrapInitialization.test.ts \
  src/tools/video-editor/commands/bootstrapCapture.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/integrations/runtime/createDefaultTimeline.test.ts
# 4 files, 127 tests passed

NODE_OPTIONS='--require=.../workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs' \
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts
# 2 files, 31 tests passed

node_modules/.bin/eslint src/integrations/runtime/createDefaultTimeline.test.ts --max-warnings 0
# passed

node_modules/.bin/eslint $(git diff --name-only HEAD -- '*.ts' '*.tsx') --max-warnings 0
# passed

git -C <private approved-handoff-tree> apply --check ap2-m2-bootstrap-transport-assertion-repair.patch
# passed
```

`git diff --check` also passed. No full, browser, localhost/socket, Runtime Door, normal014, or opaque-inverse suite was run.

## Original-to-new assertion mapping

The original strict transport test in the base handoff test is the checklist. Its transport and lost-response assertions map as follows:

| Original guard/assertion | New native guard/assertion |
| --- | --- |
| Capture every method/path/header/body request | `calls.push` remains; every native request is now validated before a response is returned. |
| Health route returns the accepted protocol/schema/runtime identity | Exact `GET /v1/health`, exact `Accept`, body-free request, and the same response identity fields. |
| Handshake route returns connector actor/realm/scopes/capability | Exact `POST /v1/handshake`, exact `Accept` + JSON headers, exact protocol/client/version/requested scopes body, and the same full actor/realm/scopes/capability response. |
| Realm route returns the selected realm | Exact `GET /v1/realm`, exact `Accept`, body-free request, and realm response; the client still checks handshake/realm equality. |
| Original project GET/PATCH/list route cases | The native sequence uses the existing native client/outbox controls for project/timeline selection; the equivalent native create, history, immutable revision, and commit routes are now exact and guarded. No arbitrary project/timeline response is echoed. |
| Lost response occurs only on the intended publication request | Lost response occurs only on the exact native init commit route; wrong commit routes fall through to rejection, and legacy publication/document POST routes are explicitly rejected. |
| Unexpected method/path throws | Exact route branches plus the final `unexpected method/path` rejection; legacy route branch gives a dedicated rejection. |
| Client pins expected actor, realm, and runtime instance | Existing `expectedIdentity` remains; handshake/health responses remain the exact expected identity, and the test asserts a handshake was made. |
| First invocation rejects the simulated lost response | Existing `rejects.toThrow('simulated lost response after init')` remains. |
| Restart/retry returns the same timeline | Existing second invocation resolves to the requested timeline ID. |
| Exactly two publication requests | Exactly one native create and two native `/commit` calls are asserted. |
| Two requests are byte-equivalent | `expect(commits[0]).toEqual(commits[1])` remains, including method/path/headers/body. The handler also compares the second parsed body to the first request. |
| Exact POST route | New assertion requires `/v1/projects/{project}/timelines/{timeline}/commit`; the handler uses equality, not `startsWith`/`endsWith`. |
| JSON content type and idempotency headers | Handler and retry assertion require exact `Accept`, `Content-Type`, and `Idempotency-Key` header sets; create headers are checked too. |
| Full old publication body | New exact init body check includes API version, project/timeline, base revision/publication, all captured commands, and App source; create body fields are also exact. |
| Stable parent/base identity | Exact `parent-0` / `bootstrap-p0` guards are enforced on every init retry. |
| Stable idempotency key after lost ACK | Both commit calls must carry the same valid key; create carries the exact caller key and occurs once. |
| Idempotency key format guard | Native handler enforces the accepted key grammar for create and commit. |
| No legacy timeline-document route | Handler explicitly rejects `/timeline-documents`; lost-response test asserts no such traffic. |
| No legacy composition-publication POST | Handler explicitly rejects POST `/composition-revisions`; lost-response test asserts none occurred. Immutable composition-revision GETs remain allowed for native closure verification. |
