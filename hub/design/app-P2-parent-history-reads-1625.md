# Report

Implemented P2 parent-history read oracle fix.

- If request `reads` is submitted, history must equal it exactly.
- If omitted, history must omit `reads`.
- Added focused controls for exact, extra, omitted, and forged-read cases.
- No production or Runtime changes.

Evidence: C0 §1 (request/history read semantics), §4 (accepted envelope), §5 (ordinary undo), §7 (immutable authoritative history), plus D62/D66. Source citation: `/home/user/work/runtime/contract/commit-v2.md` §§1, 4, 5, 7.

Tests passed:

- Parent/transition/document Node controls: 3 files, 3 passed, 0 failed.
- Root/app/node TypeScript checks passed.
- Fake runtime TypeScript passed with `--types node,vite/client`.
- Scoped ESLint passed.
- `git diff --check` passed.

Protected original P2 case hashes were unchanged:

- Parent move: `be3db6...ba36`
- Transition single: `522c98...138c`
- Transition bulk: `df9558...010f1`

Whole-file hashes:

- `p2-tour.spec.ts`: `676624...c9cd0e0` → `07fe3d...ed2f3c`
- `p2-parent-oracle.test.mjs`: `225a4c...df47e90` → `98934e...d1d272`

Browser/original/full suites were not run per task instructions. Vitest semantic support-file execution remains unverified because the repository config excludes the `.mjs` oracle and runner loading fails on its existing `__dirname` usage.

Commit message written; `DONE` marker created.