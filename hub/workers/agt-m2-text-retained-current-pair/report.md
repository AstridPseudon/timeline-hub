Prepared the current S2+text candidate against Runtime `129493b2` (`a51267ec` descendant). Both original legacy positives passed with `--runxfail` before marker removal.

- Native service: **21 passed**
- Agent: **450 passed**, 1 integration-only deselected
- Schema/native: **54 passed**
- Current neighbors: **245 passed**
- Runtime: **199 passed**; artifacts: **3 passed**
- Generation checks, Ruff and diff check passed.

Exact commands, identities and decisions: [report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-text-retained-current-pair/notes/report.md). [Candidate handoff](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-text-retained-current-handoff.md).

Destructive GC remains unverified: Runtime exposes append-only CAS and reachability checks. Public release and App cutover remain held pending official release and actual journeys.

`commit-msg` and `DONE` written.