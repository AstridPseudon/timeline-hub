Implemented test-only inventory count restoration.

- Exact counts: 1 read without Remotion; 2 reads with current12 Remotion, preserving identity/restart/empty checks.
- Appended call-site explanation to `design/agent-baseline-109-cutlist.md`.
- No production changes.

Tests:

- Bootstrap identity file: **69 passed**
- Remotion registry neighbors: **11 passed**
- Named `remotion-0012-nodes`: **80 passed**
- Broader local run had 6 unrelated sandbox socket failures.

Wrote `commit-msg`, `report.md`, and `DONE`.