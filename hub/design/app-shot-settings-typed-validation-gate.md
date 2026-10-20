# ShotSettings typed-validation gate — PASS

2026-10-20. Worker `app-m2-shot-settings-typed-validation-gate`; source base `7d8292a48`.

## Change

The newly authored malformed referenced-shot negative now expects the Runtime's
typed validation response: HTTP `422`, `code: "validation_error"`, and
`message: "shot revision payload cannot be projected losslessly"`. The fixture
still binds the selected occurrence to the malformed shot revision with
`metadata: []`, and still requires the unchanged head/closure assertions.

No Runtime, guard, or product code changed. The malformed negative remains
strict; no broad 4xx/range expectation was added.

## Evidence

Local controls passed:

- 4 neighboring Vitest files: 73 tests passed.
- ESLint on `tests/integration/runtimeRestore.test.ts` passed.
- Runtime-restore Vitest listing found both integration tests.
- `git diff --check` passed.
- The three product files remained byte-identical to `c07be0d4d`.

The required central run was requested once, without `--files`, using the
cache-free historical Agent/Runtime runner:

```text
app-m2-shot-settings-typed-validation-gate-restore-shot-safety-cachefree-m1-compat-integration-1020083703-16622
```

It passed: 1 file, 2 tests, exit 0. This covers the original restore, all five
raw settings roots, the referenced malformed-shot refusal, tracked Agent
moves, settings/name 409 draft preservation, and the full raw HTTP closure.

Earlier attempts `13713` (rejected before execution due to an invalid file
argument) and `9869` (the stale 400 expectation) remain historical records and
are not treated as evidence for this corrected source.
