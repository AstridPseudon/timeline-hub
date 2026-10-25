# D127c findings

## F002 — closed for the intended controls

The permanent Sol 2033 packet provides a qualifying local execution under the exact supported Node20.19.4 binary. Its worker-owned CommonJS entry requires the installed `tsx/cjs/api` 4.21.0 API, verifies the original App test source SHA-256 before loading it, and calls `tsxRequire(source, __filename)`. The resulting events are from the original three named controls, not a wrapper or a rewritten predicate:

- source guard: PASS;
- reviewed-profiler validator: PASS;
- reviewed-new validator: PASS.

The independent event checker found 3 actual named passes, 0 failures, 0 intended skips, and 0 missing nodes. It counted no wrapper or filtered event as a pass. The whole-file TAP result is also preserved: 3 passes, 0 failures, and 4 ordinary nonmatching `test name does not match pattern` skips. Those four are expected targeted selection and are disclosed; no claim of literal global zero skips is made.

The entry logs the real Node20 executable, real shared `node_modules` origin, TSX/esbuild versions, and the unmodified `node:assert/strict` method names. Source inspection found no assertion-method monkeypatch or predicate transformation. The entry and reporter hashes are recorded in `source-manifest.json` and match the final execution record.

The outside service request `13179` is not success evidence: its 5GB snapshot guard stopped before original source load. It was not retried. Prior false zero-node results, the prior Node20 timeout, Runtime request `30318` (61 passed), and review2013 F001/static checks remain preserved and are not rewritten. This closes only review2013 F002 execution/source/privacy scope; it does not close D130 SWAP, WAL/recovery, full-tour, or the separately gated original profile/element/latency/core/ZIP outcomes.

## Source integrity

The current App worktree is exactly `fd586440a626fc49a35a9dd0ac7e838d5fe55a4b` / tree `6d2744e271f016206854ab33f57b3cfc737ad54d`; the reviewed source is SHA-256 `59a4d116683f88d415024b6d9236e578cf03c11e2c913b56278f9d57448b40ef`. Runtime `fb4addba…` and helper SHA-256 `095c252b…` were read-only hash checks. No repository, shared install, cache, hub, or upstream write was made.
