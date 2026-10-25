# Validation record

## Read-only checks performed

| Check | Result |
|---|---|
| PLAN.md and task constraints read | PASS |
| Runtime HEAD/tree compared with `fb4addba95ca4bae0482c93be94e5cae2770ca09` | PASS; exact HEAD/tree |
| App committed source `466c921f...` and equivalent `fd586440...` compared | PASS; exact tree `6d2744e...` and exact test blob |
| Source-only TypeScript AST parse of the App test file | PASS; 0 parse diagnostics, 7 top-level `test()` registrations |
| Bad selector evaluated against registered titles | PASS diagnosis; 0 matches |
| Correct full-title selectors evaluated against registered titles | PASS diagnosis; 2 matches |
| Node20 `--version` / `--help` | PASS; v20.19.4 and supported flags recorded |
| Node22 `--version` / `--help` | PASS; v22.22.0 and isolation flag recorded |
| `tsx` package/lock identity read | PASS; 4.21.0 |
| Runtime helper SHA-256 and Git blob identity read | PASS; exact `095c...` helper |
| Worktree status before/after inspection | PASS; this Runtime worktree clean |

## Intentionally not run

No actual test body, Node20 corrected proof, Node22 test, unit/pytest suite,
localhost/socket/service, registration, browser, profile, native, full suite,
tour, or Runtime rerun was executed. The central Runtime PASS61 evidence remains
reused and unchanged. This worker contributes diagnosis and a corrected command,
not PASS credit.

## Prior evidence used only as comparison

- Existing D127c Node22 controls: one named node each with full title selectors and
  `--experimental-test-isolation=none`.
- Existing exact-title Node20 profiler control: 1 passed / 5 skipped with
  `--test-reporter=spec`.
- Existing D127c source review: F001 fixed, F002 wrapper-only and unqualified.
