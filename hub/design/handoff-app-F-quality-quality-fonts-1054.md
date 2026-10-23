# App F quality/font handoff — PASS

Base `7e0af6c9cda5a81a89505b006fcd653d4a5fc770`; upstream policy `7c17cc9d9f9504b578862e2ffd27623fca08a04f`.

The App quality/font slice is complete. `package.json` now restores the `test:no-remote-hosts` script and runs both `typecheck:strict-islands` and `test:no-remote-hosts` from canonical `quality:check`. The stale remote-font default/switch assertion was replaced with the upstream self-hosted Inter proof in `src/app/main.bootstrap-order.test.tsx`; `config/vite/vite.config.ts` no longer reads or installs the obsolete remote-font switch/plugin.

Verification: the mandated focused Vitest run passed (2 files, 4 tests); serialized App `tsc` passed; scoped ESLint passed; `git diff --check` passed; the no-remote-host test passed (6/6 subtests). Baseline was 2 failures / 5 tests: the dropped quality gates and stale Google Fonts expectation. Full/browser/journey suites were not run.
