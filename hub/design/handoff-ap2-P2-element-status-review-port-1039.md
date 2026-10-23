# P2 element-status review/current port

PASS. Ported only `tests/e2e/local/three-products.p2-elements-assets.spec.ts` from donor `cde590d4ee0cb5ca2e5d426a175e03507ee266a7` onto current App base `0cdc76782833d594776452e07706acb406c51553`.

The working blob is exactly donor blob `836d144bc0e3bbd8f1677d23e96385bcd8127daa`. Donor parent `f2fd916061f73d02b1c6c9803350af880b7bf2e5` differs by only the required `historicalrebased` -> `rebased` literal at line 209. EOF is clean and the current worktree has no other changes. This preserves the inherited EOF-clean source, full v2 request/reply/history/type-limit assertions, original three core selectors, production caller, reload, intended-field proof, and guarded Undo.

Evidence: scoped ESLint PASS; Playwright `--list` PASS with exactly 3 tests; base-to-working and donor diff checks PASS. No browser/HTTP/body/service/full/typecheck/build run per scope.

