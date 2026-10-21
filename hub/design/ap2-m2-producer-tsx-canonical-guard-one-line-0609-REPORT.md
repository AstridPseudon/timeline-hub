# App M2 producer TSX canonical guard — 0609

## Result

The immutable 0600 custody gate was copied to the worker record and changed by
one line only. The source preflight was requested once against the exact source
target and failed; startup was therefore not requested, per the stop-on-failure
rule.

## One-line diff

```diff
-test "$(realpath "$TSX_BIN")" = "$TSX_CLI"
+test "$(realpath "$TSX_BIN")" = "$(realpath "$TSX_CLI")"
```

The executable, CLI, loader, package, wrapper, source, authority, probe, and
required shared `node_modules` link checks remain bound and unchanged. No App
source, probe, realm, authority, dependency, or live caller file changed.

## Hashes

- Immutable 0600 custody gate: `0e39303a1deebadeaeeaf1b7336e71c2ee9f55107452d86094ed74b2a2678282`
- Corrected custody gate: `0ffea3e0ed4f78c5ebdd73d090ed9fd919a9430e3cfe7696ae9cd4847e638287`
- Source: `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7` / tree `fd16d32fd3487e56c9fe1ff16582dba240f63b77`
- Wrapper: `329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352`
- Probe: `4beb7c22dfa06e04d28253dbab02f76ff2a9953f0accd4b12247514e4f0608f6`
- TSX executable/CLI: `8729ecfb90d9d568939e4190e6f1d3317c946583b7d37a776e0c23a21c021cf8`
- TSX loader: `0b1c5b86192772fe9257710e739959cee5947c11ae1f93b61abfaa9b80c6def1`
- TSX package: `6e764b21991c21595441f82387c1451ccd10a3e7a3f0973cc5e3649a12dea7d2`
- Agent authority: `8130a401bf44a518d5a40ae274d398b8c560be55` / tree `236c3e57e0265c52b81ba8085de3193026176bff`
- Runtime authority: `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / tree `7ab412cc4bcbe517efcfa806e092336390312e18`

## Proof and tests

- `sh -n producer-startup-final-custody-gate.sh`: PASS.
- Offline custody proof: intended shared symlink layout PASS; wrong TSX
  target/path refusal PASS; corrected gate digest binding PASS; bytes differing
  from the immutable digest refusal PASS; immutable source gate unchanged PASS.
- Direct gate from the exact source worktree:
  `sh .../producer-startup-final-custody-gate.sh preflight`: PASS, including
  the existing 10-check public13 preflight.
- Central source preflight, requested once with exact target
  `ap2-m2-producer-realm-physical-path-diagnosis-0538`:
  `ap2-m2-producer-realm-physical-path-diagnosis-0538-ap2-m2-producer-tsx-canonical-guard-one-line-0609-preflight-1021061341-23173`
  — FAIL, exit 1, zero reported test counts. The service saw the required App
  tree `fd16d32f`; its log was empty, so the central-only failure cause is not
  further identified.
- Startup result: not requested because preflight failed; result ID/count:
  none / 0. Dormant actual was registered but not run.

## Registration and next step

Registered literal gate-hash-bound suites in `tests/suites.conf` for preflight,
startup, and dormant actual. No retry and no `integration:app` request were
made. The next step is to diagnose the central runner’s unexplained failure,
then request startup once only after a fresh successful preflight.
