# Agent lead: work list (orchestrator, updated 2026-10-20T21:20Z). Read this every hour. Agent is HOMED on your machine since 21:19Z.
NOTE: report progress in your hourly lead line, not by message; message only for blockers, escalation categories, tool bugs or direct questions (LEAD.md "Communication").
GOAL: Agent's M2 rows turn DELETED, and gates 1 and 3 (Agent half) have real proof suites.
STANDING RESPONSIBILITIES: services alive with a Monitor ALWAYS armed; 5-7 live workers; disk >10 GB (sweep-tmp, compact-scratch, recycle); merges via bin/request-merge; integration pushed by hub-sync (fast-forward only); Viewing merge requests into agent reviewed promptly; manager acks its INBOX within 45 min; lead line hourly in hub/status/agent-lead.md.
WORK LIST NOW (report each as done / blocked):
1. Workers to 5+ within 30 min (Luna high; Sol only with HARD).
2. Historical-audio and registered-completion positives, then DELETE the accepted-journal consumers, legacy SDK saves and sheet merge (15:12Z audit redirect).
3. Parallel gate track: one worker on gate 1 (tests/editing_conformance across CLI/Python/sheet) and gate 3 Agent half (renderer stopped: commit, reload, undo; honest preview unavailability).
4. The one agt worker still finishing on main: when its branch is on hub/tl/<worker>, review and merge it here.
5. Upstream main for agent: refresh-main is now YOUR machine's job (bin/refresh-main --check daily; merge-forward via a worker on conflict).
9. (21:27Z) MAIN DRIFT: upstream agent main is 147 commits ahead. The manager dispatches ONE merge-forward worker today (--merge-parent the upstream tip; regenerate generated files with the repo tooling; tests move with upstream, never dropped), merges it, then reruns the affected gates. Report the merge sha. If a published contract or pin changes, tell me.
6. (22:03Z, deep audit) Finish the Scene and audio consumers. Keep admission-only evidence clearly separate from completed workflows; don't count a test-only admission as a finished workflow.
DONE WHEN: every Agent ledger row is DELETED or KEEP with evidence, gates 1 and 3 (Agent) are green on current main, and the manager reports M2 exit.
