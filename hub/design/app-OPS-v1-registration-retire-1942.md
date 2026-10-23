# App OPS v1 registration retirement

- Scope: `scratchpad/orch/tests/suites.conf` only.
- Removed: 36 verified-unreferenced v1 references (10 retired comments, 26 rows).
- Retained: all current v2 rows, including P1, remotion environment/child registrations, current Agent8130/Runtime2c4 consumers, and P2/P3/source/proof/quick/node/full rows.
- Evidence: final bytes equal the complete pre-write snapshot with exactly the approved 36 lines removed; all 229 remaining commands pass shlex parsing and `bash -n`.
- No deletion route, compactor invocation, service run, browser run, or product-code change was performed.

