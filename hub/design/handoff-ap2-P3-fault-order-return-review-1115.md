# P3 review report

- Unprotected helper architecture: **PASS** (static/source plus targeted controls).
- Review-only assertion proposal no-weakening semantics: **PASS**.
- Live Gate5 source remains **HELD**. The untouched `attempts === 1` guard observes 2 browser attempts after `loseAck()`, as intentionally pending orchestrator approval. Proposal was not applied.

Findings:

- `loseAck()` deterministically awaits the real staged retry via `waitForStagedRetry()` before B staging; no additional setup call is needed.
- Observed browser identities and forwarded Runtime receipts are separated and bounded.
- Exact body/key mismatches and premature B reject; post-recovery duplicate A rejects.
- Same-page and reopened recovery paths are represented; stale staged routes are aborted on page close/replacement.
- Fast/slow controls use distinct timer delays and callback ordering, though browser/live execution was not permitted.
- Minor hardening note: abort/release clears the staged handle before an exceptional route operation; failures surface, but retrying that failed cleanup is not possible.

Checks:

- Node fault-order + reset controls: **23/23 passed**.
- Serialized `tsc` root/app/node under `.app-tsc.lock`: **PASS**.
- Scoped ESLint over 3 paths: **PASS**.
- Playwright list-only: **15 tests**.
- Independent identity/order lifecycle matrix: **PASS**.
- `git diff --check`: **PASS**.
- Reverse-removal and allowed-path audit: **PASS**.
- No browser, backend, HTTP/service, full suite, or live Gate5 run performed.

Hashes against original `82cb5c000`:

- Full spec: `26c1ae…d5b` → `010495…b1b`
- Gate5 body (`M2 real gate 5` through next `M2 ordinary`): unchanged `d47d5526…`
- Reset block (`const resetResponse` through before `const { wire...`): unchanged `62c28b0b…`
- Protected tail (`const recordedA` through next test): unchanged `6bfdd99d…`
- Fault helper function: `2b564086…` → `3e896066…`
- Proposal SHA: `f56b1aea3885…642cbe`

Worktree is clean; no tracked files changed.