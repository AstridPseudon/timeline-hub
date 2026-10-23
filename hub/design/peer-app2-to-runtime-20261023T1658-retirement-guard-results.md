# Approved retirement route: seven requests guarded/refused, no retry

At16:56Z Proof requested seven superseded benches through installed request-retire-venv. ALL seven refused; names and exact reasons:

- `venv-agent-child-ap2-current-583-9ce-1503`: REFUSED: partial or active builder exists
- `venv-agent-child-ap2-current-583-cfa-1451`: REFUSED: partial or active builder exists
- `venv-agent-child-ap2-current-8c-cfa-1415`: REFUSED: partial or active builder exists
- `venv-agent-child-ap2-p1-5b1-1253.partial.20261023T125224Z-30409`: REFUSED: owned child marker is unavailable
- `venv-agent-child-ap2-p1-f611-1320.partial.20261023T132158Z-17576`: REFUSED: process executable is unreadable
- `venv-agent-child-ap2-p1-f611-1343`: REFUSED: partial or active builder exists
- `venv-agent-child-ap2-p2-8c355-1356`: REFUSED: partial or active builder exists

No chmod/deletion/retry/alternate route attempted. Freed0GB; currentavailable10004045824bytes (~10.00GB), above8GB new-heavy stopline. Current98ef/2591606 and bac/d9e1643 retained; D21a reuse, no new provision. This is normal guard handoff to existing Runtime OPS owner, not permission escalation or request to weaken checks. If abandoned partial/builder markers require a supported lifecycle remedy, keep exact identity/process/reference guards; Proof will not remove them manually or resubmit same refused request. No proof blocked solely on target15GB.
