## Report

Branch: `tl/rt-OPS-suites-prune-return-0215`

Durable packet: [diagnostics/ops-suites-prune-0215](/home/user/work/wt/rt-OPS-suites-prune-return-0215/diagnostics/ops-suites-prune-0215)

- Baseline: `f64e1f4b…a89c1d0`
- Candidate: `fdb9e9e9…d69cfc81f`
- Patch: `38769a80…3fd74d5`
- Manifest: `de3c9b06…d035349`
- Validator: `afce1a96…cd70f9b`

Six annotated rows:

1. `agent/custody-root-cause-exact7d-trace`
2. `agent/custody-root-cause-exact7d-trace-clean`
3. `agent/custody-root-cause-exact7d-original-order`
4. `agent/custody-root-cause-exact7d-guard-context`
5. `agent/venv-agent-child-s2-c13-c13-full`
6. `agent/full-remotion13-s2-integration`

Validation command:

`PYTHONDONTWRITEBYTECODE=1 python3 diagnostics/ops-suites-prune-0215/validate_packet.py` — PASS.

Also passed JSON/syntax, unique active-key, private patch dry-run/apply/replay, non-target byte equality, five protected env hashes, and whitespace diffcheck.

Active rows: `106 → 100`. No actual disk freed: `0 GB`; no live edits, retirement, deletion, or operational action occurred.

Protected current/final names remain untouched: `agent-remotion-current`, `agent-remotion-v3-819acf-1110`. Agent remote snapshot remains missing; `agent-remotion-0013`, `composition14-255b6856`, `main95bd`, and `published14-091aa23e` remain unclassified.

Commit message and `DONE` marker created.