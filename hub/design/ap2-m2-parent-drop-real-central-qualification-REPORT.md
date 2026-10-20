# ap2-m2-parent-drop-real-central-qualification

## Result

The committed App candidate was sent through one central browser/e2e request
using the staged private014 parent-add cohort. The run reached the real mounted
`File`/`DataTransfer` gesture after exact source, artifact, schema, private
node-graph, collection, and hosted-build guards passed. It stopped at the
first causal assertion: the wrong verified media selection returned HTTP 422,
while the candidate assertion allows only 404 or 409.

This is not product qualification. The native ADD, selection equality,
lost-ACK/restart/retry/reload, undo, opaque preservation, no-duplicate, and
zero-legacy assertions after that point did not run. No rerun was made.

## Exact source and cohort

- App source: committed `e07d31f2608ed5c8c63e04f01946217974758700`, tree
  `3e3b71683d4a9fb582ddf965106b0adf4218b447`; worktree clean before request.
- Agent: `3c4f6de4fa777323b3386c01c7266b619b86af6d` / tree
  `aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c`.
- Runtime: `202074110717146fc7f08af2306a8dd7f695b0b1` / tree
  `ee39286bd0eb27d4075074cc4785d6d15e33f243`.
- Producer: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, artifact
  `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`.
- Shared schema: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`;
  wire digest `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
- Locked Composition graph: public13 archive SHA
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`,
  Composition tarball SHA
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

The private014 choice was based on the matched parent-add cohort evidence:
the normal014 parent-media acceptance and peer ACK use the 3c4/202/a0/f021/6ba
tuple. Public013 was not substituted or adopted.

## Central request

Exactly one request was made:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-drop-real-central-qualification ap2-m2-parent-drop-real-central-qualification --no-cache) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result: `ap2-m2-parent-drop-real-central-qualification-ap2-m2-parent-drop-real-central-qualification-1020204641-29674`, exit 1, 103s, one failed test. Log:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-parent-drop-real-central-qualification-ap2-m2-parent-drop-real-central-qualification-1020204641-29674/log.txt`

Central evidence before the failure:

- Exact Playwright collection under service context: **1 test**, the mounted
  manual-drop title, collected before `npm run build:hosted`.
- Hosted build: passed.
- Browser launch and real mounted gesture: reached.
- Failure: `three-products.spec.ts:1172`, expected `[404, 409]`, received `422`.

The Runtime 202 source maps malformed exact media-selection input to its
intentional `ValidationError`/422 response. The test changes `object_id` to
`sha256:wrong-selection`, which is not a syntactically valid digest. This is a
test/cohort contract mismatch to resolve, not evidence that refusal was absent;
the subsequent no-write assertions were not reached in this run.

## Local verification

```text
sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-drop-real-central-qualification/run-parent-manual-drop-central.sh
PASS

git status --porcelain=v1 --untracked-files=all
PASS (clean App worktree)
```

The producer and journey source checks were inherited from
`ap2-m2-parent-migrated-drop-mounted-source-REPORT.md` and the producer
`ec663e205a` report; they were not relabeled as browser evidence. No local
browser, localhost, live socket, full suite, dependency install, API/DTO/schema
change, pin adoption, or product edit was performed.

## Blocker and next step

Blocked on the settled decision for the private014 malformed-selection refusal
expectation. The owner should either make the test’s refusal assertion match
the established private014 422 contract, or change the injected wrong object
to a syntactically valid but wrong digest if the intended assertion is the
Runtime’s 409 conflict path. That decision requires a new committed candidate;
no assertion was changed and no blind central rerun was made here.
