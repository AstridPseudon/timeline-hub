# AP2 M2 selected approved real-scope one-case report

## Result

One and only one central selected DEV case was submitted from App commit
`8e9975005d18c6278000ab4c8cc8b18291d03e12`, tree
`87d2350417a876e14b81c58b64da29f1a30b35b6`, using the existing durable
selected driver and named suite `ap2-m2-selected-real-p1-history-fixture-fix`.
The case is **not qualified**.

Central result:

- Result ID:
  `ap2-m2-selected-approved-real-scope-one-case-0342-ap2-m2-selected-real-p1-history-fixture-fix-1021034300-18585`
- Exit: `1` (`fail`), 1 failed test, 112 seconds.
- Build: passed; 5,583 modules transformed, 53.63 seconds.
- Collection: exactly 1 test in 1 file.
- Browser case: 1 failed at the first startup assertion.

## First actual failure and evidence

The first failure was the unchanged original 20-second mount assertion in
`tests/e2e/local/three-products.selected-param-dev.spec.ts:30`, called from
line 59:

```text
expect(page.locator('#root > *').first()).toBeAttached({ timeout: 20000 })
Error: element(s) not found
```

The page snapshot shows the App shell and a `Select project` control stuck at
`Loading project`, while `main` is empty. The retained network trace records
`GET /runtime-config/v1/workspace.json` returning HTTP 404. This is recorded as
observed context only; no repair or causal workaround was attempted.

Retained first-result evidence:

- Result log and summary: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-selected-approved-real-scope-one-case-0342-ap2-m2-selected-real-p1-history-fixture-fix-1021034300-18585/log.txt`
- Error context: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace/three-products.selected-pa-e0e73-fusal-retry-reload-and-undo/error-context.md`
- Playwright trace: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace/three-products.selected-pa-e0e73-fusal-retry-reload-and-undo/trace.zip`
- Driver stderr: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace/driver.stderr`

No selected `/v1` commit packet, response, idempotency key, refusal body,
lost-ACK packet, or undo packet was produced before this failure.

## Assertion scope

Executed: the selected worker fixture setup, DEV server startup, page
navigation, and the first `expectAppMounted` assertion.

Not executed: `openSeededTimeline`, exact project/timeline URL identity, clip
selection, first P1 amount-8 commit, P2 admission, authored-source removal,
reload/readback, P1-schema refusal and dirty-draft preservation, lost-ACK
capture, restart/recovery, exact retry body and key, inverse undo, and the
zero-legacy-POST assertion. These remain unverified.

No live caller or product source was changed. The only selected live caller
remains `tests/e2e/local/three-products.selected-param-dev.spec.ts`; the
durable driver remained unchanged.

## Preflight commands and results

The final combined preflight passed before submission:

- Candidate and clean-tree identity checks for App `8e997500…` / tree
  `87d23504…` — passed.
- Frozen Agent `8130a401…` / tree `236c3e57…` and Runtime `2c4ac180…` / tree
  `7ab412cc…` checks — passed.
- Locked public13 graph, archive SHA256 `895c628a…`, Composition tarball
  SHA256 `9412ae25…`, Runtime all-75 artifact count, and Composition all-77
  member count — passed.
- Effective shared Node/Vite/Playwright/tsx/Composition graph resolution —
  passed (`node v22.22.0`, Vite `5.4.21`).
- `node --import tsx --test tests/e2e/local/support/selected-param-credential.test.ts`
  — passed (1 file-level test; 4 subtests in the file).
- Vitest selected controls with `--no-cache`, one worker, and six selected
  files — passed: 6 files, 71 tests.
- `node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'local DEV selected PARAM uses admitted P1 through P2 removal, refusal, retry, reload and undo' --list`
  — passed: exactly 1 test in 1 file.
- `sh -n` on the existing durable selected driver — passed.
- `SELECTED_WORKSPACE_PREFLIGHT_ONLY=1 sh .../run-central-selected-p1.sh "$PWD"`
  — passed: private workspace preflight ready.

The first two local attempts at the preflight harness itself exposed only
checker-loader mistakes (package-export lookup and direct ESM import of the
repository's CommonJS `__dirname` config); neither ran a central case. The
final checks used public package entrypoint resolution and the repository Vite
CLI loader.

## Submission and limits

The exact submission was:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-selected-approved-real-scope-one-case-0342 ap2-m2-selected-real-p1-history-fixture-fix --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

There was no retry, second submission, source edit, new wrapper, timeout or
navigation workaround, local browser/socket run, install, or full suite.
The worktree remains clean and has no build residue. The next step is an
orchestrator-owned diagnosis of the observed startup/workspace-config failure;
this worker does not claim any P1/P2 or downstream journey qualification.
