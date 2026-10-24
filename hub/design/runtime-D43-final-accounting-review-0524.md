## Result: PASS

Exact integrated identity:

- Runtime `1d9ddba546f8fb1300f55ff62607ed492719cbaa`, tree `f56c396c4495547680b46e832565278d2c375e69`
- `faf6…` is ancestral “before,” not a live pre-run head.
- Reviewed commits: `66657fda4`, `778878be0`; exactly two over integration.
- Fixture blob `1182259ea4bbb8f62ef3443f7db3f6a5e3bb50c4` matches reviewed `778878be0`.
- `faf6..HEAD` changes only the headless test. `2b49..HEAD` changes only headless and occupancy tests; all other files match.

Evidence:

- Retained ordinary run: `13 passed in 3.44s`, exit 0, against Agent `9cd3dbe865a941c052bda04ae0d61306d18f8f26`, tree `57f0231da0d7904ecd8778169973d6384e0ae141`.
- Independent 0518 run: `13 passed in 3.70s`, exit 0.
- Static AST counts: baseline 67 predicates; reviewed/integrated fixture 84 predicates across 10 tests, preserving the +17 migration assertions.
- Offline retry envelopes and scoped reads were byte-identical; SHA `d271bb…e3`.
- Runtime caller and C0v2 shapes unchanged; no overlay or capture plugin credited.
- Worktree clean; `git diff --check` passed.

Exact original-36 accounting:

- 10 current headless original IDs closed.
- 15 occupancy IDs retained from `faf6` + Agent `9f2da582…` evidence; the additional 16th occupancy case is excluded.
- 11 prior closures retained: manifest 1, response migration 2, receipt/idempotency 2, speed 6.
- 3 passing headless extras were excluded.
- No Agent source-copy or all-consumer-head closures credited.

Final count: **36 closed / 0 open / 0 unaccounted**.

No tests, providers, HTTP, full suite, journey, or duplicate qualification were run by this worker. Final freeze and authorized full rerun remain required. The prior failed command/capture-finalizer packet loss remains disclosed and is not treated as a product failure.