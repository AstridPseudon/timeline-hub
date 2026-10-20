# App committed parent Delete gate: marquee-owner fix

## Result

**Not qualified.** The new strict central wrapper reached the real first UI
case on the exact committed owner-scoped selection fix, but the success case
failed before any Runtime commit request was observed. The conflict case was
not launched after that terminal product failure. This is not a deletion,
undo, conflict, or legacy-writer qualification.

No App product source, tests, dependency files, lockfiles, or integration
worktrees were changed. The only execution setup was the new ORCH wrapper and
suite registration.

## Exact source and guard tuple

- App commit: `f732a73a4ee35cc9510f53b6f0e4f69dc8486702`
- App tree: `3d7ec25cb5f37b8c21647009e563fd6235facee4`
- Agent commit/tree: `8130a401bf44a518d5a40ae274d398b8c560be55` /
  `236c3e57e0265c52b81ba8085de3193026176bff`
- Runtime commit/tree: `2c4ac180c2220bdad966bc01e95ad230e99ce26a` /
  `7ab412cc4bcbe517efcfa806e092336390312e18`
- public13 archive SHA-256:
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
  with exactly 77 regular files
- Astrid public source SHA-256:
  `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`
- Runtime artifact manifest: 75 artifacts
- Chromium: `141.0.7390.37`, SHA-256
  `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`
- Cache ID was bound to the exact App SHA/tree, Agent/Runtime pair, public13
  archive, and Chromium SHA.

The wrapper passed the first guards:

```text
public13 archive/all77 files and peer graph verified; private node_modules overlay ready
Verified 65 pinned Astrid source files.
Verified 155 vendor/astrid-browser files from Astrid 680d1aa4f1f9576d65a603472f1dd7fc0ae9ccd1.
Verified 20 @astrid-public imports from src/pages/Home/astrid-public-host.tsx.
ok runtime.lock.json (matches pinned producer commit)
ok runtime.lock.json (matches producer manifest)
[marquee-owner public13 parent-delete candidate] source preflight passed for f732a73a4ee35cc9510f53b6f0e4f69dc8486702 / 3d7ec25cb5f37b8c21647009e563fd6235facee4
```

Postflight also passed, including source, public13/all77, Runtime all75,
peer, and cache checks:

```text
[marquee-owner public13 parent-delete candidate] source/public13 postflight passed
[marquee-owner public13 parent-delete candidate] all source, all75/all77, peer, cache and browser guards passed
```

## Central execution

- Suite: `e2e-parent-delete-marquee-owner-committed-tree3d7ec25c-appf732a73-agent8130-runtime2c4-public13-e2e-integration`
- Test ID: `app-m2-delete-marquee-owner-committed-gate-e2e-parent-delete-marquee-owner-committed-tree3d7ec25c-appf732a73-agent8130-runtime2c4-public13-e2e-integration-1020183936-2909`
- Command: `request-test app-m2-delete-marquee-owner-committed-gate e2e-parent-delete-marquee-owner-committed-tree3d7ec25c-appf732a73-agent8130-runtime2c4-public13-e2e-integration`, then `wait-test`
- Result: exit 1, one failed test, 196 seconds
- Build completed successfully in 1m17s.
- Discovery/execution used one real Playwright test worker.

## First real failure and trace

Test: `tests/e2e/local/clip-delete-command.spec.ts:192:1` — `M2 current013 real parent DELETE: lost ACK, reload, Runtime restart, exact retry and UI inverse restore raw opaque clip`.

After the real UI Delete keypress, the first product assertion timed out:

```text
Expected: 1
Received: 0
Timeout 90000ms exceeded while waiting on the predicate
clip-delete-command.spec.ts:222:55
await expect.poll(() => wire.posts.length, CEILING).toBe(1);
```

The preserved browser error context shows the connected timeline with the
`f2-app` overlay selected, the `f2-app.png` clip active, and the Delete clip
inspector visible. The captured Runtime post count remained zero. No guessed
readiness explanation is reported.

- Central log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-delete-marquee-owner-committed-gate-e2e-parent-delete-marquee-owner-committed-tree3d7ec25c-appf732a73-agent8130-runtime2c4-public13-e2e-integration-1020183936-2909/log.txt`
- Error context: `/tmp/tl-marquee-owner-parent-delete-run.0jjpib/browser-artifacts/clip-delete-command-M2-cur-9193a-rse-restore-raw-opaque-clip/error-context.md`
- Playwright trace: `/tmp/tl-marquee-owner-parent-delete-run.0jjpib/browser-artifacts/clip-delete-command-M2-cur-9193a-rse-restore-raw-opaque-clip/trace.zip`

The second real conflict case was correctly not run. Therefore raw absence,
opaque-field preservation, reload/undo, lost-ack/restart, exact request
receipt, same-property 409 draft retention, and zero-legacy assertions remain
unverified by this run. Existing assertions and group261 were left unchanged.

## Other commands and limits

- `git status --short --branch` after the run: clean App worktree.
- No full suite, TypeScript check, install, local browser run, or shared
  dependency/cache write was performed.

## Next step

Diagnose the concrete zero-POST behavior from the preserved trace and real UI
source, then repeat this exact two-case strict wrapper from the repaired
committed App tree. Do not treat this run as qualification or run only the
conflict case.
