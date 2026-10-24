Implemented D73 in only:

- [d66-plain-stack.mjs](/home/user/work/wt/app-P-D73-launch-return-1713/scripts/testing/d66-plain-stack.mjs)
- [d66-plain-stack.test.mjs](/home/user/work/wt/app-P-D73-launch-return-1713/scripts/testing/d66-plain-stack.test.mjs)

Key fixes: actual env path lookup, four-repository immutable pin validation, genuine receipt parsing, submit recipe/dispatch output, and temp local-Git preflight coverage.

Tests:

- Node 20 syntax + focused tests: 9/9 passed.
- Collection counts: p1 2, p2 8, p2-element 1, p3 1.
- Scoped ESLint and `git diff --check`: passed.
- Protected spec hashes: unchanged.
- Strict TypeScript: baseline failure from missing generated `@astrid/packs`/virtual modules; no diagnostics involve changed files.

Positive fixture preflight ran under `/tmp/w-1ad4e5c80d/d73-preflight-iIk34w` and exercised four normal repos, detached checkouts, both real receipt formats, wrong-path, and missing-pin negatives. No service/browser/full run or invented service receipt was used.

Commit message and `DONE` marker created.