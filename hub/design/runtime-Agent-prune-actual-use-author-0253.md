## Report

Created [diagnostics/ops-prune-agent-0253](/home/user/work/wt/rt-OPS-prune-actual-use-0253/diagnostics/ops-prune-agent-0253).

- Private patch retires only Composition14 generic `full`/`targeted` aliases (rows 21, 23).
- Composition14 gate/provision rows remain held.
- Main95bd (10 rows) and published14 (4 rows) remain held as frozen proof/final scope.
- Agent-remotion-0013 has no active rows, but env removal is **UNKNOWN** without remote liveness/lease evidence; no env deletion proposed.
- Active unique keys: 141 → 139.
- Exact snapshot, env hashes, protected current/v3 bytes, and ABA row (`811` bytes, SHA-256 `962906…d102`) verified.
- No live changes, retirement requests, probes, deletions, or disk-freed claim.

Validation:

- `python3 diagnostics/ops-prune-agent-0253/validate_packet.py` — PASS
- `PYTHONPYCACHEPREFIX=... python3 -m py_compile .../validate_packet.py` — PASS
- JSON parsing and private patch replay — PASS
- Packet `git diff --check` — PASS

Commit message and `DONE` marker written.