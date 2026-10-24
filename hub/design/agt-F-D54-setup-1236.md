## D54 setup package report

- Created [agt-F-D54-setup-1236.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D54-setup-1236/evidence/agt-F-D54-setup-1236.json).
- Classified all 45 exact `Agent/Farm profile setup` nodes as `non-core` + `env`.
- Preserved original node IDs, status/order, source membership, summary offsets, traceback offsets, and reconciliation.
- Counts: 45 errors; 36 retained tracebacks; 9 summary-only.
- Regression: 0 proven, 0 unproven, 45 not-applicable. No upstream comparison was invented.
- Six package groups are disjoint and sum to 276.
- Wrote commit message and created `DONE`.

Validation:

- `python3 -m json.tool ...` — PASS
- Evidence parity/count assertions — PASS
- `git diff --check` — PASS
- No tests, reruns, probes, installs, network, or product edits performed.

Unverified next step: rerun the exact 45 nodes with the qualified `agent-remotion-v3-819acf-1110` profile.