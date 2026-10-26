# Validation

Read-only checks only:

- `bash -n` passed for the immutable 0735 controller, cut, pristine, tiny
  control, and positive-stub scripts.
- Python stdlib AST parsing passed for `binding-source.py` and
  `check-source.py`; JSON parsing passed for the 0735 source manifest and
  admission derivation. The author checker itself was not rerun.
- The 17 SAFE 0735 evidence originals match the 0817 publication manifest by
  SHA-256. The 0735 retained-original census contains 45 paths; all 45 are
  absent. No missing raw/control bytes were copied.
- Current clean tuples were read-only checked: Agent
  `ecdc242ed9b673f641759ecf029f95e89a2c6f92` / tree
  `d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735`, Runtime
  `95d98f038320d5d46bd679ac000ab3e15825c935` / tree
  `78df31d62c5b9ba4c84dee4ea346e43a767718c1`, App
  `82e9e13ddf1d7ec6c736521b2eb091dca9877598` / tree
  `6a6e49eb4461b5ca1a7fa1247653bc794f26d710`, and this Composition
  `6a2d1c22ec800229812f4d756d7198aece8111ed` / tree
  `57f68e1fad9c84ce0c0a2fa10f9a2f8defb1a847`.
- Current Agent/Runtime/App/Composition worktrees were clean. The central
  App-visible service config has Agent `full`, `targeted`, and `conformance`
  rows but no `agent-core-full`; this was not interpreted as Agent absence.
- Static route reading covered `request-test`, `dispatcher-daemon`,
  `test-run`, `wait-test`, `bench_store.py`, `suites.conf`, the 0735
  controller/recipes/consumer, the production D73 launcher, and C0
  `contract/commit-v2.md`.
- A worker-owned sampler ran at approximately 5-second cadence from
  `2026-10-26T08:31:03.181Z` through `08:31:08.192Z`, minimum available
  bytes `4,920,274,944`, above the 4,000,000,000 stop. TERM was delivered,
  wait returned `143`, and the sampler was reaped; see
  `sampler-lifecycle.json` and `disk-trace.txt`.

Not run by instruction: the 0735 checker, product tests, targeted tests,
full suites, request-test, test-run, wait-test, dispatcher, service/body,
CAS/registry/queue operations, installs, or live collection. These are
unverified, not passes.

