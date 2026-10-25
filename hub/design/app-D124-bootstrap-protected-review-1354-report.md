# D124 independent protected review

**Verdict: FAIL**

Candidate `4b4e0558ef3853bc999dd65c0df4580ad5704eff`, tree `8e4c8ca6d96a8d39fdad7d4618f940880f8ab46e`; base `af5fe0a2748ce6df65fb36ce9cd435fc1df0502a`, tree `2afa38ba9e8ebfcefb23c81dbc1af3b1b9eabe0c`.

Only the two authorized test files changed. Frozen upstream `3881e9440` contains the server test but not the P2 bootstrap test at the requested path.

Findings:

- `assertRetention` does not enforce bounded relationships. Mutated `events_retained=999999` and `output.bytes=999999` were accepted.
- Phase status/count contradictions and negative timestamps are accepted; `UNKNOWN` with count `1` and `start_ms=-1` both passed validation.
- Sampling accepts `sample_share=2`; privacy checking only rejects selected key names, allowing private marker values in schema strings.

Tests:

- Normal helper `a17a…76a4`: 2 passed, 0 failed.
- Reviewed helper `6c9d…0760`, activated through the supported D66 path/hash hook with correct basename: 2 passed, 0 failed.
- ESLint affected files: passed.
- `tsc -p tsconfig.app.json --noEmit`: passed.
- `tsc -p tsconfig.node.json --noEmit`: passed.
- `git diff --check`: passed.

The fake-runtime POST throw route preserves `500 fake_internal` and server survival. Candidate-specific author `facts.json` and `commands-results.md` were absent; results above are independently verified. No candidate fixes were made.