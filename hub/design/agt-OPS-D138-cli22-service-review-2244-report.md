# D138 Review Report — FAIL

Updated only `ops-d138-cli22/` with independent operational controls.

Findings:

1. `use_runtime(vendored_runtime_commit())` selects locked Runtime `ab1e…`, not manifest Runtime `f103…`; mixed tuple is blocking.
2. Supported launcher accepts duplicate manifest keys last-write-wins; malformed keys are refused.

Validation:

- Private controls: 10/10 passed.
- Parser, exact 22 selectors/marker, argv quoting, per-ID artifacts, positive exit-17/one-call, malformed refusal, poisoned zero-call: passed.
- Ruff, Python compile, `bash -n`, `git diff --check`: passed.
- Source check: expected exit 1, `NOT_READY`.
- No central request, collection, body/provider, install, or full suite run.

The shared Agent checkout had moved to pending U4a merge `41ad…`; it was not silently retargeted.

Evidence written to the required five files under `.../evidence/`. Commit message and `DONE` marker created.