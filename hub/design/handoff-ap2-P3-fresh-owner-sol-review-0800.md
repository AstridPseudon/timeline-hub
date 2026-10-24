# P3 review: FAIL

The cumulative Sol delta is not acceptable as-is.

Findings:

1. `gate5-reset-precondition.ts:148` and `:196` reject documented optional `rationale` and `group_id` fields. Runtime’s DTOs and contract allow these fields, and existing App tests verify their round-trip behavior. This violates the requirement that legitimate optional full DTO fields remain accepted.

2. `three-products.spec.ts:1267` snapshots prior owners only when the page is already at the harness origin. Gate5 calls `openCommandTimeline` before `openApp`, so a normal fresh Playwright page starts with `previous=[]`; historical owners are not actually excluded. The helper test does not cover this ordinary page lifecycle.

Evidence:

- Protected reset/tail remained byte-identical: `f7e7abd9233a332adfeea03155d78af05a5d631ffffbecd64691c7014936bb67`.
- Reverse-removal proof matched original C0: `0e69b561a0c750669f45e54259021179b355bde41a52e265b7ea198be7318f14`.
- Gate5 body hashes: original `48632c...`, base `f23dc2...`, final `c527a3...`.
- D50 is not in this base; ancestry check exited `1`.
- Worktree remained clean; no tracked edits were made.

Tests:

- Helper suite: 18/18 passed, exit 0. The prescribed worker TMPDIR was a regular file and produced `ENOTDIR`; rerun with private TMPDIR succeeded.
- TypeScript `tsconfig.json`: exit 0.
- TypeScript `tsconfig.app.json`: exit 0 after polling.
- TypeScript `tsconfig.node.json`: exit 0.
- Scoped ESLint with `--max-warnings 0`: exit 0.
- Playwright list-only: 15 tests listed, exit 0.
- `git diff --check`: exit 0.

No browser/backend/live Gate5 run or full suite was performed. Commit message and DONE marker were created as required.