Implemented D66 harness stabilization.

Changes:
- [d66-plain-stack.mjs](/home/user/work/wt/app-D66-stable-current-sources-1643/scripts/testing/d66-plain-stack.mjs) now requires detached, clean per-request Agent/Runtime checkouts matching current normal heads.
- Records selected HEADs/trees, source paths, and import readbacks.
- Refuses mutable homes, stale snapshots, dirty or attached checkouts.
- Added focused controls in [d66-plain-stack.test.mjs](/home/user/work/wt/app-D66-stable-current-sources-1643/scripts/testing/d66-plain-stack.test.mjs).

Tests:

- Node 20 syntax check: passed.
- Node 20 ESLint: passed.
- Node 20 focused tests: 4 passed.
- `git diff --check`: passed.
- Dry launch using mutable homes: correctly refused.

Current source heads requiring manager checkout preparation:

- Agent: `ef0363985e645481952448619f2cbb25e9d51a66`, tree `1be86f3b…`
- Runtime: `bc227de07262accb702eae8a44c4a666b568c08e`, tree `1d410a67…`

Required manager requests:

```text
request-checkout agent ef0363985e645481952448619f2cbb25e9d51a66 "D66 current Agent source"
request-checkout runtime bc227de07262accb702eae8a44c4a666b568c08e "D66 current Runtime source"
```

No browser, original journey, full suite, or service run was performed. Commit message and `DONE` marker were written.