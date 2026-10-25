# D127c report

Verdict: **SOURCEFAIL / validation blocked**

- Verified App `466c921f…`, tree `6d2744e…`; only the permitted sourceguard test changed.
- Confirmed F001 fixed: exact Runtime helper hash `095c252b…` has a strict profiler arm; legacy arms and fail-closed negatives remain.
- Node22 actual controls passed:
  - sourceguard: 1 named node
  - reviewed-profiler validator: 1 named node
  - reviewed-new validator: 1 named node
- ESLint, TypeScript, diff-check, scope, and real harness hash/source-proof checks passed.
- Required Node20.19.4 command executed only the file wrapper (zero intended inner nodes), so per instructions it is **NOTPASS**, not evidence of success.
- Reused Runtime request `30318`: 61 passed; no Runtime rerun or changes.
- No live/bootstrap/socket/browser/full/product tests run.

Blocker: rerun the bounded Node20 controls outside this sandbox and require named-node pass counts before SOURCEPASS.

Evidence written under the required `evidence/` directory; commit message and `DONE` marker created.