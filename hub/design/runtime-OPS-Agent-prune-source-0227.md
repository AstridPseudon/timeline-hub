## Report

Created durable packet at [diagnostics/ops-prune-agent-0227](/home/user/work/wt/rt-OPS-prune-agent-source-0227/diagnostics/ops-prune-agent-0227).

- Exact snapshot preserved; SHA-256: `8708f05c…c8833`
- Baseline/candidate are byte-identical; no safe source comment qualified.
- `agent-remotion-0013`: unreferenced env-only artifact; no registration row to comment.
- `composition14-255b6856`, `main95bd`, `published14-091aa23e`: HELD due active/gate/template references.
- Product source, live config, registrations, envs, runtimes, and branches unchanged.
- Disk freed: `0 GB`.

Validation:

`PYTHONDONTWRITEBYTECODE=1 python3 diagnostics/ops-prune-agent-0227/validate_packet.py` — PASS

JSON parsing, exact env SHA checks, private patch replay, unique active-key census, and packet `git diff --check` — PASS.

No product tests were run; this is a source-only operational packet.