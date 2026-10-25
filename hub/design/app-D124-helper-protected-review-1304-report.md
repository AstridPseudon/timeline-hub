# D124 protected review report

Verdict: **FAIL**.

Candidate scope is correct: only the two requested test/helper files changed.

Findings:

- `arrival` is emitted at `_dispatch` entry, not actual HTTP arrival (`p2_commit_phase_capture.py:876-879`). This relabels dispatch and invalidates `request_wall_ms`/sampler denominator claims.
- App D66 currently derives the helper from `RUNTIME_CHECKOUT`; it has no explicit reviewed helper path/hash. Therefore normal attachment is blocked while production Runtime remains immutable at `5e9ad`.
- `observer_cpu_ms` is capture-wide but duplicated into each request summary without an overhead scope.

Evidence:

- Central targeted tests: **18 passed in 3.28s**
- Ruff: passed
- Mypy with shared test path and `--follow-imports=skip --ignore-missing-imports`: passed
- Compile and `git diff --check`: passed
- Node 20 normal `sitecustomize` hook: sink created successfully, no HTTP request
- Privacy poison-marker check: passed; route sanitized and idempotency key hashed
- Production Runtime `/home/user/work/runtime`: clean at `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`
- Helper SHA256: `13883f6f1611b2a9df8dbb5c5c4f4355a0b04864b256e6457bb135017a4b09d6`

Evidence files and exact helper copy are under the worker evidence directory. No source fixes were made. Full-body/P2 GO remains unverified and blocked pending a supported D66 reviewed-helper path/hash route.