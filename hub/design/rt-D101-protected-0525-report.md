## D101 protected review — FAIL (static gate only)

Semantic/source review passes:

- Protected MAIN six source is byte-identical: SHA256 `3138f2ac...`; baseline `ef6db3be`, current `6aefd117`.
- Six cases remain image/video × `anchor`, `fallback`, `lane-end`; all original inputs/assertions preserved.
- Runtime HEAD: `381178476`; auth blob `002c9af5`; new test blob `610dcc42`.
- Agent baseline: SHA256 `05a1ebc6...`, blob `b4206343`; candidate: SHA256 `76224a624...`, blob `f8e3bd95`.
- Protected `site`, `canonical_site`, `rebase_patch`, and `inverse_address_resolver` ASTs are unchanged.
- New tests use the genuine Runtime service/provider, cover raw/config mirror mutations, absence/null/type/value/member/order changes, ABA, explicit scopes, atomic fallback, and unrelated parent-clip positive merge/undo behavior.
- C0 shape remains lossless: raw `parent.registry`, config `parent.config.registry`, or tagged `parent.config` when malformed/absent. Caller `parent`/`timeline` scopes remain broad and unfiltered.
- Reused SECURITY evidence: `99`, `23`, and `14` targeted tests passed; no-write refusals and history conflicts were observed.

Checks run:

- AST/compile: passed.
- Scoped Ruff with Agent configuration: passed.
- `git diff --check`: passed.
- Agent baseline/candidate mypy: no issues.
- Runtime auth mypy: no issues.
- Added test mypy: failed with one new diagnostic at `tests/test_timeline_native_asset_union.py:171` (`Assignment to variable "error" outside except: block`).

No product or test files were changed. The required next step is for the author to resolve that mypy diagnostic, rerun the scoped checks, then perform the original six-case proof with the original 45-second timeout and full C0 shapes.