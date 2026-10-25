## Completed

Implemented bounded `p2-element-verify` D127d route:

- Preserves original element selector/body and private stdout/stderr retention.
- Omits capture sink, helper, watchdog, tracing bootstrap, and measurement env from Runtime children.
- Keeps default routes and source guards unchanged.
- Added launcher controls for valid/invalid route combinations.

## Validation

- Node 20.19.4 D66 suite: **30 passed, 0 failed**
- `node --check` assigned MJS files: **PASS**
- ESLint harness: **PASS**
- TypeScript node/app configs: **PASS**
- `git diff --check`: **PASS**
- Original element and bootstrap source diffs: **unchanged**

No Runtime candidate, service, browser, body, or full suite was run; candidate verification remains held pending Runtime qualification.

Evidence written under the required absolute worker evidence directory. `DONE` and commit message are present.