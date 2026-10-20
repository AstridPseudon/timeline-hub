# Handoff: vw-m4-restore-main-makefile

## Change

- Added only the Composition root `Makefile`.
- It matches `git show 67b8aa3:Makefile` byte-for-byte:
  - `install` delegates to `npm install`.
  - `build` delegates to `npm run build`.
  - `test` delegates to `npm test`.
  - `clean` removes `typescript/dist` and `node_modules`.
- No package/version/artifact/build-output files changed.

## Verification

- `make -n install build test clean` — pass; emitted `npm install`, `npm run build`, `npm test`, and `rm -rf typescript/dist node_modules`.
- `cmp Makefile <(git show 67b8aa3:Makefile)` — pass.
- `git diff --check` and untracked-file diff check — pass.
- Worktree/archive guard — only `Makefile` is changed; no immutable archive path changed; no local `typescript/dist` exists.
- Direct `make build` / `make test` — not run: this worker has no `node_modules`; installing is prohibited by the task and shared dependencies are read-only.
- Central targeted request: `vw-m4-restore-main-makefile-targeted-1020084852-29968`.
  - Command: `node --import tsx --test typescript/tests/registries.test.ts typescript/tests/theme.test.ts scripts/gen-registry.test.mjs`
  - Result: 3 passed, 8 failed. Existing failures report `React is not defined` from `typescript/src/ThemeContext.tsx:104` during SSR. This Makefile-only change does not alter that code.
  - Result directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m4-restore-main-makefile-targeted-1020084852-29968/`.

## Manager-ledger handoff: original smoke tests

- Original `typescript/tests/scaffold.test.ts`: meaningful registry coverage is now represented by `scripts/gen-registry.test.mjs`, `typescript/tests/registries.test.ts`, and the generated-registry/export checks in `scripts/smoke-package.mjs`; its constant-tag self-equality assertion was literal-only coverage.
- Original `typescript/tests/theme-api-smoke.ts`: replacement coverage is the strict NodeNext consumer/type probe in `scripts/smoke-package.mjs` plus provider/public API behavior in `typescript/tests/theme.test.ts`.

## Decisions and next steps

- No plan decisions were changed or relitigated; the root wrapper was restored exactly from main.
- Manager should record the two original test paths and their replacement tests above in the deletion ledger.
- The existing `React is not defined` targeted-suite regression needs separate Composition-owner triage; it is outside this task.
