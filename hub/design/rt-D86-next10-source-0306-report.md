## Report

Implemented the F-D86 exact-new10 source-only packet at [evidence/fd86-next10-source-0306](/home/user/work/wt/rt-D86-next10-source-0306/evidence/fd86-next10-source-0306).

- Exact membership: inverse7 + D92 compound3; zero overlap with executed161, later102, or scheduled D91.
- Preserved original550, 23 NO_JUNIT_CASE, D87 ledger, held predicates, and excluded D92 atomic/ABA.
- Recorded current source hashes, ancestry, AST checks, C0 shape, and pending four-repo/preflight/body status.
- Packet size: 26,153 bytes.
- Commit message written; `DONE` created.

Checks passed:

- Static set/hash/AST/in-memory compile/JSON validation.
- `bash -n evidence/fd86-next10-source-0306/route/main-affected-batch-recipe.sh`
- `sha256sum -c inputs/selector-argv.sha256`
- `git diff --check`
- No trailing whitespace; no product/test/generated/schema/dependency changes.

Not run by design: pytest, collection, helpers, fixtures, services, browser/build/profile/checkouts, or body execution. Inverse7 MAIN7 and D92 compound3 MAIN3 remain open for the manager’s later qualification route.