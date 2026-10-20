# App M2 ordinary enabled-fixture central run

Date: 2026-10-20 UTC  
Worker: `ap2-m2-ordinary-enabled-fixture-final-run-source`  
Repo: App  
Worktree: `/home/user/work/wt/ap2-m2-ordinary-enabled-fixture-final-run-source`

## Result

The requested one central actual ordinary run was started from a clean,
committed standalone-authoring-enabled fixture at
`ebb762a774bd997b836947cbecc0828f797cbcfe` (tree
`c79b342f648d415ce2ff284e5903e16626aa00ad`). The run did not reach browser
interaction or the ordinary assertions. No App source change was made.

The first environment trace was Chromium smoke launch failure:

```text
setsockopt: Operation not permitted (1)
process did exit: exitCode=null, signal=SIGTRAP
browserType.launch: Target page, context or browser has been closed
```

The runner's nested shell continued to the build and test. The hosted build
passed, and the E2E test then failed at harness port preflight before any
page interaction:

```text
Error: door port 17340 is not free (EPERM); stop whatever uses it or set ASTRID_APP_DIRECT_DOOR_PORT
```

This is an environment/harness availability failure, not a product assertion
failure. Per the brief, there was no blind rerun and no dirty-source request.

## Exact commands and evidence

Preflight/clean commit verification:

```text
git status --porcelain=v1 --untracked-files=all
test -z "$(git status --porcelain=v1 --untracked-files=all)"
git rev-parse HEAD
git rev-parse 'HEAD^{tree}'
test "$(git rev-parse HEAD)" = ebb762a77f9e22ce7ef6f31ab8bca42de0d4d7ec
```

Result: PASS. The full commit is
`ebb762a774bd997b836947cbecc0828f797cbcfe`; the abbreviated expected value
was checked against the full resolved commit. The worktree was clean before
queueing and remains clean afterward. The runner removed
`.m2-ordinary-central-run` on exit.

Central actual:

```text
bash scripts/testing/run-central-m2-ordinary.sh \
  /home/user/work/wt/ap2-m2-ordinary-enabled-fixture-final-run-source
```

Runner preflight passed for the requested immutable graph and native setup:

- private node graph: `packages=532 bins=34`;
- Agent commit/tree: `8130a401bf44a518d5a40ae274d398b8c560be55` /
  `236c3e57e0265c52b81ba8085de3193026176bff`;
- Runtime commit/tree: `2c4ac180c2220bdad966bc01e95ad230e99ce26a` /
  `7ab412cc4bcbe517efcfa806e092336390312e18`;
- source tuple printed by the test matched App `ebb762a774bd997b836947cbecc0828f797cbcfe`,
  Agent `8130a401...`, and Runtime `2c4ac180...`.

Build result: PASS (`npm run build:hosted`, Vite built in 58.35s; `dist/index.html`
was present). Chromium smoke: FAIL before page interaction with the SIGTRAP
trace above. Ordinary E2E: FAIL at `tests/e2e/local/three-products.spec.ts:1206`
with `EPERM` while checking door port `17340`; 1 test ran, 0 product assertions
were reached.

## Scope/decision record

- Used the existing `e2e-m2-ordinary-integration` path and the exact pinned
  Agent/Runtime heads required by the brief.
- Did not change product guards, add features, alter dependencies, use public
  pins, run a full suite, or run a local browser/socket workaround.
- Did not attempt a second central run because the first trace established an
  environment failure and the subsequent E2E preflight independently failed
  with `EPERM` before interaction.
- No source fixture/producer fix was justified: there was no fixture or
  producer assertion failure to repair.

## Recommended next step

The central test service/host should provide a Chromium-capable execution
context and a permitted/free `17340` door port (or an approved harness port
override) before this fixture is requalified. Re-run the exact command only
after that environment condition is corrected.

