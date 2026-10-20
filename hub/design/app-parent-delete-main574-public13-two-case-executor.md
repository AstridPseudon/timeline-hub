# App MAIN574/public13 parent-delete two-case execution

## Disposition

**BLOCKED on a real product/browser failure.** The required current-source central run reached the actual browser journey, but the success case did not emit a commit request. Per the task boundary, the conflict case was not run after this terminal product failure.

No App product source, test assertion, dependency, lock, or integration worktree was changed. The wrapper and suite registration are ORCH-only execution setup.

## Exact source tuple

- App commit: `1981ce9801b661a9a335201b0ebd4fcdf1d8aad1`
- App tree: `a4cc5140cb19f6d4414150d22ac579bce90bb08a`
- Agent commit/tree: `8130a401bf44a518d5a40ae274d398b8c560be55` / `236c3e57e0265c52b81ba8085de3193026176bff`
- Runtime commit/tree: `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / `7ab412cc4bcbe517efcfa806e092336390312e18`
- public13 Composition archive: SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77 regular files
- Astrid public source digest: `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`
- Browser: Chromium `141.0.7390.37`, SHA-256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`

The declared App commit mapped to the fixed App tree, and the central snapshot was checked by tree identity rather than requiring its HEAD commit to equal the declaration.

## ORCH execution setup

- Suite: `e2e-parent-delete-main574-public13-two-case-a4cc5140-agent8130-runtime2c4-e2e-integration`
- Registration: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`
- Wrapper: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-main574-public13-two-case-executor/notes/run-parent-delete-public13.sh`
- Runner: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-main574-public13-two-case-executor/notes/parent-delete-public13-runner.mjs`
- Central request: `app-m2-parent-delete-main574-public13-two-case-executor-e2e-parent-delete-main574-public13-two-case-a4cc5140-agent8130-runtime2c4-e2e-integration-1020162631-16510`
- Result: exit 1, `1 failed`, 304 seconds

The wrapper reused the existing `playwright.clip-delete.config.ts` and the two existing parent-delete test names. Success and conflict were separate child `npm`/Playwright processes; the second child was correctly not launched after the first concrete product failure.

## Guard evidence

Preflight and postflight passed:

- public13 archive and installed package matched byte-for-byte across all 77 files; peer graph matched
- Astrid vendor source verification passed: 65 pinned source files, 155 browser vendor files, 20 public imports
- Runtime lock/vendor checks passed for App and Agent; Runtime all-75 artifact audit passed
- Agent and Runtime HEAD/tree/clean checks passed
- Chrome 141 identity, source identity, private node-module overlay, private cache, and short TMPDIR guards passed
- wrapper reported: `source/public13 postflight passed`

## Product failure

Test ID: `tests/e2e/local/clip-delete-command.spec.ts:177:1` — `M2 current013 real parent DELETE: lost ACK, reload, Runtime restart, exact retry and UI inverse restore raw opaque clip`.

At `clip-delete-command.spec.ts:208`, after the real UI selection and `Delete` keypress:

```text
Expected: 1
Received: 0
Timeout: 90000ms exceeded while waiting on the predicate
```

`wire.posts.length` remained `0`; therefore no actual commit request was observed and the success assertions could not proceed. The central service log is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-parent-delete-main574-public13-two-case-executor-e2e-parent-delete-main574-public13-two-case-a4cc5140-agent8130-runtime2c4-e2e-integration-1020162631-16510/log.txt`

The central wrapper cleaned its private browser-artifact directory after postflight; no product conclusion is drawn from the missing local trace archive. This is not claimed as a Runtime acceptance, deletion, undo, conflict, or legacy-writer pass.

## Limits and next step

The historical public12/tree06121 two-case pass remains historical and was not relabeled. No full suite, project typecheck, install, PCM/frame work, merge, or ledger deletion claim was made. The manager should diagnose why the current MAIN574/public13 UI Delete action produces no commit request, then rerun this exact two-case suite from the repaired committed tree; the conflict case still requires its own fresh process.
