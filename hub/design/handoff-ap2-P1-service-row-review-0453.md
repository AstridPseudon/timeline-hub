# Handoff: ap2-P1-service-row-review-0453

Status: **FAIL — do not request the P1 service body yet.**

The exact `app ap2-P1-chain-h6` command is syntactically valid, and the
selector-only run finds exactly the two original P1 cases. Static source,
resolver, durable-graph, pin, import, and clean-worktree checks pass. The
existing P3 row and every other existing suite row are unchanged.

The first exact-row failure is its App-base guard:

```sh
test "$(git rev-parse HEAD^)" = 8770aa1625198826778828173ef6e2c55a3c07f3
```

The assigned worktree is already at `HEAD=8770aa1625198826778828173ef6e2c55a3c07f3`,
whose parent is `HEAD^=6fdfd1ca2487718c3ee4565a916393693001cfef`. Thus the exact
row command exits before the reviewed D13/spec/resolver checks and before any
service or body execution. This is a row/base-pair defect; it was not changed
because this review is strictly readonly.

Evidence:

- shell syntax: PASS;
- exact row hash: `335a3103851b1daa455fe6501e1e37fa6065e25578252fba5f994ff5cce34bc9`;
- all rows excluding P1 hash: `81c9bd02376fccd395708954769b74511e6c2b94683e32968cbd727598a21310`;
- P3 row hash: `cca4082c94b29c408c9eb8db31066475800e4ba5688743f16fcd0d5b90108b9b`;
- selector-only `--list`: PASS, 2 tests in 1 file, both original titles;
- pinned Agent/Runtime and durable 0407 graph checks: PASS;
- source worktree status and diff check: PASS;
- readiness-0446 TypeScript/scoped-lint PASS evidence reused on the identical
  source tree.

No build/browser/socket/service/body/full suite was run. No repo or shared
dependency was modified. Manager/orchestrator disposition is required before
the body request.
