# Render-task error diagnostic packet

## Result

Applied a small App test-only patch on the assigned worktree. The existing
viewing-parity render comparison now stops its normal task polling immediately
when the admitted task is terminal `failed` or `cancelled`.

The failure line contains only bounded `task_id`, `attempt_id`,
`error_type`, `error_location`, and `code` fields. It never copies
`result.error.message`, stderr, input bodies, paths, secrets, or arbitrary
exception text. Invalid or absent structured fields become `unknown`; the
terminal-state fallback code is `task_failed` or `task_cancelled`.

The retained 15923 task result was inspected from the existing trace. Its
supported failure payload had `result.error.message` and `retryable: false`,
but no structured `error_type`, `error_location`, or `code`. The new test
therefore explicitly proves that this shape produces only the bounded fallback
line. The existing App production diagnostic formatter was not changed or
used because it intentionally includes a sanitized message, which is outside
this packet's stricter output boundary.

## Exact patch

- `tests/e2e/timeline/viewing-parity/cases.ts`: replace the 240-second
  success predicate wait with a bounded polling loop that throws the safe
  terminal diagnostic immediately; successful task/download behavior and all
  following authority, output, provenance, source-version, page-diagnostic,
  and cleanup checks are unchanged.
- `tests/e2e/timeline/viewing-parity/compare.ts`: add the pure test-harness
  formatter and scalar allowlists.
- `tests/e2e/timeline/viewing-parity/compare.test.ts`: add one planted failure
  control (including a malicious free-form message and retained 15923-shaped
  fallback) and one success control; existing pixel tests remain intact.

No product source, public API, Runtime, frozen App0d43 packet, real task,
retry, token, socket, dependency, or browser artifact was changed.

## Evidence

- `node --import tsx --test tests/e2e/timeline/viewing-parity/compare.test.ts`
  — pass, 5 tests.
- `npx eslint tests/e2e/timeline/viewing-parity/compare.ts tests/e2e/timeline/viewing-parity/compare.test.ts tests/e2e/timeline/viewing-parity/cases.ts --report-unused-disable-directives --max-warnings 0`
  — pass.
- `git diff --check` — pass.
- No full, central, browser, Runtime, helper, socket, install, or production
  run was performed.

## Decision / next step

No decision beyond the settled plan was needed. Manager should read this
packet and the worker report before requesting merge. A future authorized
physical run can verify the new prompt failure against a real task; that run
was intentionally not requested here.
