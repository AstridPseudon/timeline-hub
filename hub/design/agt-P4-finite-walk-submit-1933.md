## Report — D73 P4

Prepared the pinned tuple and exact checkout receipts:

- Agent `3b2db4bdf9014de013338521dd038ebdecd25f02`
- Runtime `e89eb8c7dfa8cb2c451653ab200dbf77df28b173`
- App `e771ce1426022d1a10bab93323d40222c5ce9c3d`
- Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`

Original test hash: `8e336b1ce059770f63e3026e0ee9fc0a3f29bd6e557fbba4725138065c453753`.

Preflights:

- Positive pinned dry preflight: exit `17`, harmless stub called exactly once.
- Poisoned wrong-SHA preflight: exit `1`, stub called zero times.

Submitted exactly one request:

```text
request-test integration:agent p4-current-becfe-http-3legs --no-cache
```

Service ID: `agent-p4-current-becfe-http-3legs-1024193607-5907`

Result: terminal harness failure, exit `2`, before pytest launched. The registered row initially lacked its closing shell quote. I repaired only the two owned rows via the authorized CAS route; outside rows remained byte-identical. No retry was submitted.

No three test outcomes or durations are claimed because the body never ran. Pinned toolchain facts were validated in dry preflight: Python venv-agent, Node `v20.19.4`, Composition `0.0.14`, schema digest `867f…`.

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-finite-walk-submit-1933/evidence/`

Worktree is clean; no product or test files changed. Task is blocked and recorded in [BLOCKED](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-finite-walk-submit-1933/BLOCKED).