# Review report: vw-m3-task-diagnostics-security-review-1050

## Verdict

APPROVE after one concrete security correction applied in this review worktree: `SAFE_ERROR_CODE` no longer permits `/`. Before the correction, a value such as `C:/secret` was copied into the diagnostic despite the requirement that paths be excluded.

## Scope and exact base/meta evidence

- Repository: App; worktree: `/home/user/work/wt/vw-m3-task-diagnostics-security-review-1050`.
- Requested base branch exists: `tl/vw-m3-render-task-error-diagnostic-packet-1042`.
- Base and review HEAD are identical at `4174e87296d13294bd8bb7680a6af4616ce99ba9`; therefore the branch-to-branch diff is empty and the owner delta is not a NOOP: the packet is the commit `4174e87296d13294bd8bb7680a6af4616ce99ba9` versus parent `5ff11809e8100a6670acdb55eb19588ea168a80c`.
- Packet metadata: `test: surface safe terminal render failures`, authored/committed by Claude on 2026-10-21 10:43:11 UTC.
- Exact packet diff is limited to the requested three files: `cases.ts` 18 insertions/7 deletions, `compare.test.ts` 30/1, `compare.ts` 36/0.
- Review correction delta from packet HEAD: `compare.test.ts` 13/4 and `compare.ts` 1/1. No `cases.ts` change.
- No live callers beyond the requested path: `formatTerminalTaskFailure` is used by `cases.ts` and covered by `compare.test.ts`.

## Review findings

- The render poll now reads the admitted task and calls the formatter before blocker text or success/download checks, so `failed` and `cancelled` task states fail promptly with bounded output.
- The formatter emits only task ID, attempt ID, error type, error location, and code. IDs and all three diagnostic fields are length-bounded and character-allowlisted; invalid values become fixed fallbacks.
- `result.error` and `task.result` are inspected only as direct records. Free-form `message`, `stderr`, `path`, `inputs`, `input_body`, and unknown nested data are not copied.
- The planted direct malicious-task test now covers free-form message/stderr/paths/inputs, malformed IDs, path-shaped code/location, and nested unknown data. A cancelled-task case confirms the terminal cancellation fallback.
- Existing success, download, provenance/postflight, authority, legacy-write, frame/audio, and cleanup assertions in `cases.ts` remain retained. The prior comparator positive and negative assertions remain retained.

## Tests and checks

Passed (exit 0):

- `node --import tsx/esm --test tests/e2e/timeline/viewing-parity/compare.test.ts tests/e2e/timeline/viewing-parity/admission.test.ts tests/e2e/timeline/viewing-parity/diagnostics.test.ts tests/e2e/timeline/viewing-parity/download.test.ts` — 4 targeted TAP files passed, 0 failures.
- `node_modules/.bin/eslint tests/e2e/timeline/viewing-parity/cases.ts tests/e2e/timeline/viewing-parity/compare.ts tests/e2e/timeline/viewing-parity/compare.test.ts --report-unused-disable-directives --max-warnings 0`.
- `git diff --check`.

Not run by instruction: full suite, browser/live E2E, Runtime/socket suites, helper/physical/install/graph copies, or any broad merge.

## Handoff

The harness should commit the two-file review correction using the supplied commit message. No build output or temporary files were left in the worktree.
